"""Module MT4/MT5 pour exécuter les ordres"""
from typing import Optional, Dict, List
from loguru import logger
import config

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False
    logger.warning("⚠️ MetaTrader5 non disponible (normal sur Linux)")

class MT4Manager:
    """
    Gère la connexion et les ordres MT4/MT5
    """
    
    def __init__(self):
        self.is_connected = False
        self.account = None
        self.server = None
        self.positions = {}  # Dict des positions ouvertes
        
    def connect(self, login: int, password: str, server: str) -> bool:
        """
        Connexion à MT4/MT5
        
        Args:
            login: Numéro de compte MT4/MT5
            password: Mot de passe
            server: Serveur broker (ex: 'GlobalPrime-Demo')
            
        Returns:
            True si succès, False sinon
        """
        if not MT5_AVAILABLE:
            logger.error("❌ MetaTrader5 n'est pas installé")
            return False
        
        try:
            logger.info(f"Connexion à MT4: {login} sur {server}")
            
            # Initialiser MT5
            if not mt5.initialize():
                logger.error(f"❌ Échec d'initialisation MT5: {mt5.last_error()}")
                return False
            
            # Se connecter au compte
            authorized = mt5.login(login, password, server)
            
            if authorized:
                self.account = login
                self.server = server
                self.is_connected = True
                
                account_info = mt5.account_info()
                if account_info:
                    logger.success(f"✅ Connecté à MT4: {account_info.name} | Balance: {account_info.balance}$")
                
                return True
            else:
                logger.error(f"❌ Échec de connexion: {mt5.last_error()}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Exception lors de la connexion MT4: {e}")
            return False
    
    def disconnect(self):
        """Déconnexion de MT4/MT5"""
        if MT5_AVAILABLE and self.is_connected:
            mt5.shutdown()
            self.is_connected = False
            logger.info("🚪 Déconnexion MT4")
    
    def place_order(self, signal: Dict, lot_size: float) -> Optional[int]:
        """
        Place un ordre Market sur MT4/MT5
        
        Args:
            signal: Dictionnaire avec les infos du signal
            lot_size: Taille du lot
            
        Returns:
            Ticket de l'ordre si succès, None sinon
        """
        if not MT5_AVAILABLE or not self.is_connected:
            logger.error("❌ MT4 non connecté")
            return None
        
        try:
            symbol = signal['symbol']
            order_type = mt5.ORDER_TYPE_BUY if signal['type'] == 'BUY' else mt5.ORDER_TYPE_SELL
            
            # Vérifier que le symbole existe
            symbol_info = mt5.symbol_info(symbol)
            if symbol_info is None:
                logger.error(f"❌ Symbole {symbol} introuvable")
                return None
            
            # S'assurer que le symbole est visible
            if not symbol_info.visible:
                if not mt5.symbol_select(symbol, True):
                    logger.error(f"❌ Impossible de sélectionner {symbol}")
                    return None
            
            # Prix actuel
            tick = mt5.symbol_info_tick(symbol)
            if tick is None:
                logger.error(f"❌ Impossible d'obtenir le prix pour {symbol}")
                return None
            
            price = tick.ask if order_type == mt5.ORDER_TYPE_BUY else tick.bid
            
            # Préparer la requête
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": lot_size,
                "type": order_type,
                "price": price,
                "deviation": config.MAX_SLIPPAGE,
                "magic": config.MAGIC_NUMBER,
                "comment": "TRADABOT",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }
            
            # Ajouter SL et TP si fournis
            if signal.get('stop_loss'):
                request['sl'] = signal['stop_loss']
            if signal.get('take_profit1'):  # Utiliser TP1 par défaut
                request['tp'] = signal['take_profit1']
            
            # Envoyer l'ordre
            result = mt5.order_send(request)
            
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                logger.error(f"❌ Erreur ordre: {result.comment}")
                return None
            
            # Sauvegarder la position
            self.positions[result.order] = {
                'ticket': result.order,
                'symbol': symbol,
                'type': signal['type'],
                'lot_size': lot_size,
                'entry_price': result.price,
                'stop_loss': signal.get('stop_loss'),
                'take_profit1': signal.get('take_profit1'),
                'take_profit2': signal.get('take_profit2'),
                'breakeven_active': False,
                'signal': signal
            }
            
            logger.success(f"✅ Ordre exécuté: {signal['type']} {symbol} @{result.price} | Ticket: {result.order}")
            return result.order
            
        except Exception as e:
            logger.error(f"❌ Exception lors du placement d'ordre: {e}")
            return None
    
    def move_to_breakeven(self, ticket: int) -> bool:
        """
        Déplace le SL au point d'entrée (breakeven)
        
        Args:
            ticket: Numéro du ticket de la position
            
        Returns:
            True si succès, False sinon
        """
        if not MT5_AVAILABLE or not self.is_connected:
            return False
        
        try:
            # Récupérer la position
            position = mt5.positions_get(ticket=ticket)
            
            if not position:
                logger.warning(f"⚠️ Position {ticket} introuvable")
                return False
            
            position = position[0]
            
            # Modifier le SL au prix d'entrée
            request = {
                "action": mt5.TRADE_ACTION_SLTP,
                "position": ticket,
                "symbol": position.symbol,
                "sl": position.price_open,
                "tp": position.tp,
            }
            
            result = mt5.order_send(request)
            
            if result.retcode == mt5.TRADE_RETCODE_DONE:
                if ticket in self.positions:
                    self.positions[ticket]['breakeven_active'] = True
                    self.positions[ticket]['stop_loss'] = position.price_open
                
                logger.success(f"🔒 Breakeven activé pour {position.symbol} (ticket {ticket})")
                return True
            else:
                logger.error(f"❌ Échec breakeven: {result.comment}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Exception breakeven: {e}")
            return False
    
    def get_account_info(self) -> Optional[Dict]:
        """Retourne les informations du compte"""
        if not MT5_AVAILABLE or not self.is_connected:
            return None
        
        try:
            account_info = mt5.account_info()
            if account_info:
                return {
                    'balance': account_info.balance,
                    'equity': account_info.equity,
                    'profit': account_info.profit,
                    'margin': account_info.margin,
                    'margin_free': account_info.margin_free
                }
        except Exception as e:
            logger.error(f"❌ Erreur récupération info compte: {e}")
        
        return None
    
    def get_open_positions(self) -> List[Dict]:
        """Retourne toutes les positions ouvertes"""
        if not MT5_AVAILABLE or not self.is_connected:
            return []
        
        try:
            positions = mt5.positions_get()
            if positions is None:
                return []
            
            result = []
            for pos in positions:
                result.append({
                    'ticket': pos.ticket,
                    'symbol': pos.symbol,
                    'type': 'BUY' if pos.type == mt5.ORDER_TYPE_BUY else 'SELL',
                    'volume': pos.volume,
                    'price_open': pos.price_open,
                    'price_current': pos.price_current,
                    'sl': pos.sl,
                    'tp': pos.tp,
                    'profit': pos.profit
                })
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Erreur récupération positions: {e}")
            return []
    
    def check_tp_reached(self, ticket: int, tp_price: float) -> bool:
        """
        Vérifie si un Take Profit a été atteint
        
        Args:
            ticket: Numéro du ticket de la position
            tp_price: Prix du Take Profit à vérifier
            
        Returns:
            True si TP atteint, False sinon
        """
        if not MT5_AVAILABLE or not self.is_connected:
            return False
        
        try:
            # Récupérer la position
            position = mt5.positions_get(ticket=ticket)
            
            if not position:
                return False
            
            position = position[0]
            price_current = position.price_current
            
            # Vérifier selon le type de trade
            if position.type == mt5.ORDER_TYPE_BUY:
                # Pour BUY: prix actuel >= TP
                return price_current >= tp_price
            else:
                # Pour SELL: prix actuel <= TP
                return price_current <= tp_price
                
        except Exception as e:
            logger.error(f"❌ Erreur vérification TP: {e}")
            return False
    
    def close_partial_position(self, ticket: int, volume_to_close: float) -> bool:
        """
        Ferme partiellement une position (pour TP multiples)
        
        Args:
            ticket: Numéro du ticket de la position
            volume_to_close: Volume à fermer
            
        Returns:
            True si succès, False sinon
        """
        if not MT5_AVAILABLE or not self.is_connected:
            return False
        
        try:
            # Récupérer la position
            position = mt5.positions_get(ticket=ticket)
            
            if not position:
                logger.warning(f"⚠️ Position {ticket} introuvable")
                return False
            
            position = position[0]
            
            # Vérifier que le volume est valide
            if volume_to_close > position.volume:
                volume_to_close = position.volume
            
            # Type d'ordre inverse pour fermer
            close_type = mt5.ORDER_TYPE_SELL if position.type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY
            
            # Prix actuel
            tick = mt5.symbol_info_tick(position.symbol)
            if tick is None:
                logger.error(f"❌ Impossible d'obtenir le prix pour {position.symbol}")
                return False
            
            price = tick.bid if close_type == mt5.ORDER_TYPE_SELL else tick.ask
            
            # Préparer la requête de fermeture partielle
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": position.symbol,
                "volume": volume_to_close,
                "type": close_type,
                "position": ticket,
                "price": price,
                "deviation": config.MAX_SLIPPAGE,
                "magic": config.MAGIC_NUMBER,
                "comment": "TRADABOT TP",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }
            
            # Envoyer l'ordre
            result = mt5.order_send(request)
            
            if result.retcode == mt5.TRADE_RETCODE_DONE:
                logger.success(f"✅ Fermeture partielle: {volume_to_close} lot(s) de {position.symbol} (ticket {ticket})")
                return True
            else:
                logger.error(f"❌ Échec fermeture partielle: {result.comment}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Exception fermeture partielle: {e}")
            return False
