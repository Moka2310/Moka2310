"""Module de parsing des signaux Telegram"""
import re
from typing import Optional, Dict
from loguru import logger

class SignalParser:
    """
    Parse les signaux de trading depuis les canaux Telegram
    Format attendu: "BUY XAUUSD @4043, TP1: 4047, TP2: 4055, SL: 4030"
    """
    
    @staticmethod
    def parse_signal(message_text: str) -> Optional[Dict]:
        """
        Parse un message Telegram pour extraire les informations de trading
        
        Args:
            message_text: Texte du message Telegram
            
        Returns:
            Dict avec les informations du signal ou None si non valide
        """
        try:
            # Nettoyer le texte
            text = message_text.strip().upper()
            
            # Détecter le type d'ordre (BUY ou SELL)
            order_type = None
            if 'BUY' in text:
                order_type = 'BUY'
            elif 'SELL' in text:
                order_type = 'SELL'
            
            if not order_type:
                return None
            
            # Extraire le symbole (ex: XAUUSD, EURUSD, BTCUSD)
            symbol_pattern = r'([A-Z]{3,10})'
            symbols = re.findall(symbol_pattern, text)
            
            # Filtrer les symboles connus
            known_symbols = ['XAUUSD', 'EURUSD', 'GBPUSD', 'USDJPY', 'BTCUSD', 'ETHUSD', 
                           'US30', 'NAS100', 'SPX500', 'USOIL', 'UKOIL']
            
            symbol = None
            for s in symbols:
                if s in known_symbols or len(s) == 6:  # Paires forex
                    symbol = s
                    break
            
            if not symbol:
                logger.warning(f"Symbole non détecté dans: {text[:50]}")
                return None
            
            # Extraire le prix d'entrée
            entry_pattern = r'@\s*([0-9]+\.?[0-9]*|[0-9]{1,3},[0-9]{3})'
            entry_match = re.search(entry_pattern, text)
            entry_price = float(entry_match.group(1).replace(',', '')) if entry_match else None
            
            # Extraire SL (Stop Loss)
            sl_pattern = r'SL:?\s*([0-9]+\.?[0-9]*|[0-9]{1,3},[0-9]{3})'
            sl_match = re.search(sl_pattern, text)
            stop_loss = float(sl_match.group(1).replace(',', '')) if sl_match else None
            
            # Extraire TP1 (Take Profit 1)
            tp1_pattern = r'TP1?:?\s*([0-9]+\.?[0-9]*|[0-9]{1,3},[0-9]{3})'
            tp1_match = re.search(tp1_pattern, text)
            take_profit1 = float(tp1_match.group(1).replace(',', '')) if tp1_match else None
            
            # Extraire TP2 (Take Profit 2)
            tp2_pattern = r'TP2:?\s*([0-9]+\.?[0-9]*|[0-9]{1,3},[0-9]{3})'
            tp2_match = re.search(tp2_pattern, text)
            take_profit2 = float(tp2_match.group(1).replace(',', '')) if tp2_match else None
            
            # Détecter le breakeven
            breakeven = 'BREAKEVEN' in text
            
            # Construire le signal
            signal = {
                'type': order_type,
                'symbol': symbol,
                'entry_price': entry_price,
                'stop_loss': stop_loss,
                'take_profit1': take_profit1,
                'take_profit2': take_profit2,
                'breakeven': breakeven,
                'raw_message': message_text
            }
            
            # Valider que les informations essentielles sont présentes
            if signal['type'] and signal['symbol'] and signal['entry_price']:
                logger.success(f"✅ Signal parsé: {order_type} {symbol} @{entry_price}")
                return signal
            else:
                logger.warning(f"⚠️ Signal incomplet: {text[:50]}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Erreur de parsing: {e}")
            return None
    
    @staticmethod
    def is_valid_signal(signal: Dict) -> bool:
        """
        Vérifie qu'un signal est valide et complet
        
        Args:
            signal: Dictionnaire contenant les informations du signal
            
        Returns:
            True si valide, False sinon
        """
        required_fields = ['type', 'symbol', 'entry_price']
        return all(signal.get(field) for field in required_fields)
    
    @staticmethod
    def calculate_lot_size(symbol: str, config: Dict) -> float:
        """
        Calcule la taille du lot selon le symbole et la configuration
        
        Args:
            symbol: Symbole du trade (XAUUSD, EURUSD, etc.)
            config: Configuration utilisateur avec les lots par catégorie
            
        Returns:
            Taille du lot à utiliser
        """
        # Mapper les symboles aux catégories
        if 'XAU' in symbol or 'GOLD' in symbol:
            return config.get('lotGold', 0.01)
        elif 'BTC' in symbol or 'ETH' in symbol or 'CRYPTO' in symbol:
            return config.get('lotCrypto', 0.01)
        elif any(x in symbol for x in ['US30', 'NAS100', 'SPX500', 'DAX', 'FTSE']):
            return config.get('lotIndices', 0.01)
        elif 'OIL' in symbol or 'WTI' in symbol:
            return config.get('lotCommodites', 0.01)
        elif any(x in symbol for x in ['AAPL', 'TSLA', 'GOOGL', 'AMZN']):
            return config.get('lotActions', 0.01)
        else:  # Forex par défaut
            return config.get('lotForex', 0.01)
