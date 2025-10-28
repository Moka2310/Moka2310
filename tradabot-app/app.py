"""
TRADABOT - Application Desktop de Trading Automatique
Interface graphique PyQt6
"""
import sys
import asyncio
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QTabWidget, QCheckBox,
    QSpinBox, QDoubleSpinBox, QGroupBox, QMessageBox, QTableWidget,
    QTableWidgetItem, QHeaderView, QFormLayout
)
from PyQt6.QtCore import QTimer, Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QTextCursor, QIcon, QColor
from loguru import logger
import requests
from datetime import datetime

# Import des modules locaux
from auth_manager import AuthManager
from telegram_monitor import TelegramMonitor
from mt4_manager import MT4Manager
from signal_parser import SignalParser
from broker_servers import get_servers_by_broker, get_all_servers_list
import config

# Configuration du logger
logger.add(
    config.LOGS_DIR / "tradabot_{time}.log",
    rotation="1 day",
    retention="7 days",
    level="INFO"
)


class TelegramThread(QThread):
    """Thread pour exécuter le monitor Telegram de manière asynchrone"""
    signal_received = pyqtSignal(dict)
    status_changed = pyqtSignal(str)
    
    def __init__(self, bot_token: str):
        super().__init__()
        self.bot_token = bot_token
        self.monitor = None
        self.is_running = False
        self.enabled_channels = {}
        
    async def signal_callback(self, signal: dict):
        """Callback appelé quand un signal est reçu"""
        self.signal_received.emit(signal)
    
    def run(self):
        """Démarre le loop asyncio pour Telegram"""
        try:
            # Créer un nouveau event loop pour ce thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Créer le monitor
            self.monitor = TelegramMonitor(self.bot_token, self.signal_callback)
            self.monitor.set_enabled_channels(self.enabled_channels)
            
            # Démarrer
            self.is_running = True
            self.status_changed.emit("running")
            loop.run_until_complete(self.monitor.start())
            
            # Garder le thread actif
            while self.is_running:
                loop.run_until_complete(asyncio.sleep(1))
                
        except Exception as e:
            logger.error(f"Erreur dans TelegramThread: {e}")
            self.status_changed.emit(f"error: {e}")
        finally:
            self.is_running = False
            if self.monitor:
                loop.run_until_complete(self.monitor.stop())
            loop.close()
    
    def stop(self):
        """Arrête le thread"""
        self.is_running = False
        self.status_changed.emit("stopped")


class TradaBotApp(QMainWindow):
    """Application principale TRADABOT"""
    
    def __init__(self):
        super().__init__()
        
        # Managers
        self.auth_manager = AuthManager()
        self.mt4_manager = MT4Manager()
        self.telegram_thread = None
        
        # État
        self.is_logged_in = False
        self.is_trading_active = False
        self.user_config = {}
        self.signals_history = []
        
        # Timers
        self.access_check_timer = QTimer()
        self.config_sync_timer = QTimer()
        self.position_check_timer = QTimer()
        
        # Interface
        self.init_ui()
        
        # Essayer de charger le token sauvegardé
        self.try_auto_login()
    
    def init_ui(self):
        """Initialise l'interface graphique"""
        self.setWindowTitle(f"{config.APP_NAME} v{config.APP_VERSION}")
        self.setGeometry(100, 100, 1200, 800)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Header avec logo et status
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Tabs
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # Onglets
        self.tab_login = self.create_login_tab()
        self.tab_config = self.create_config_tab()
        self.tab_signals = self.create_signals_tab()
        self.tab_positions = self.create_positions_tab()
        self.tab_logs = self.create_logs_tab()
        
        self.tabs.addTab(self.tab_login, "🔐 Connexion")
        self.tabs.addTab(self.tab_config, "⚙️ Configuration")
        self.tabs.addTab(self.tab_signals, "📡 Signaux")
        self.tabs.addTab(self.tab_positions, "💼 Positions")
        self.tabs.addTab(self.tab_logs, "📋 Logs")
        
        # Désactiver les onglets jusqu'à connexion
        self.set_tabs_enabled(False)
        
        # Style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a1a;
            }
            QWidget {
                background-color: #1a1a1a;
                color: #ffffff;
                font-size: 14px;
            }
            QTabWidget::pane {
                border: 1px solid #3a3a3a;
                background-color: #2a2a2a;
            }
            QTabBar::tab {
                background-color: #2a2a2a;
                color: #ffffff;
                padding: 10px 20px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #3a8fd9;
            }
            QPushButton {
                background-color: #3a8fd9;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2e7bc4;
            }
            QPushButton:disabled {
                background-color: #555555;
                color: #999999;
            }
            QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox {
                background-color: #3a3a3a;
                border: 1px solid #555555;
                padding: 8px;
                border-radius: 3px;
                color: #ffffff;
            }
            QGroupBox {
                border: 2px solid #3a8fd9;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: bold;
            }
            QGroupBox::title {
                color: #3a8fd9;
            }
            QCheckBox {
                spacing: 5px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
            }
            QTableWidget {
                background-color: #2a2a2a;
                alternate-background-color: #3a3a3a;
                gridline-color: #555555;
            }
            QHeaderView::section {
                background-color: #3a8fd9;
                color: white;
                padding: 5px;
                border: none;
                font-weight: bold;
            }
        """)
    
    def create_header(self):
        """Crée le header avec statut"""
        header = QWidget()
        layout = QHBoxLayout()
        header.setLayout(layout)
        
        # Logo/Titre
        title = QLabel(f"🤖 {config.APP_NAME}")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        layout.addStretch()
        
        # Status
        self.status_label = QLabel("⚫ Déconnecté")
        status_font = QFont()
        status_font.setPointSize(12)
        self.status_label.setFont(status_font)
        layout.addWidget(self.status_label)
        
        return header
    
    def create_login_tab(self):
        """Onglet de connexion"""
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        layout.addStretch()
        
        # Formulaire de connexion
        form_widget = QWidget()
        form_layout = QFormLayout()
        form_widget.setLayout(form_layout)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("votre@email.com")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Mot de passe")
        
        form_layout.addRow("📧 Email:", self.email_input)
        form_layout.addRow("🔒 Mot de passe:", self.password_input)
        
        layout.addWidget(form_widget)
        
        # Bouton connexion
        self.login_btn = QPushButton("🚀 SE CONNECTER")
        self.login_btn.clicked.connect(self.handle_login)
        layout.addWidget(self.login_btn)
        
        # Bouton déconnexion
        self.logout_btn = QPushButton("🚪 SE DÉCONNECTER")
        self.logout_btn.clicked.connect(self.handle_logout)
        self.logout_btn.hide()
        layout.addWidget(self.logout_btn)
        
        layout.addStretch()
        
        return tab
    
    def create_config_tab(self):
        """Onglet de configuration"""
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        # MT4 Configuration
        mt4_group = QGroupBox("🎯 Configuration MT4/MT5")
        mt4_layout = QFormLayout()
        mt4_group.setLayout(mt4_layout)
        
        self.mt4_login = QLineEdit()
        self.mt4_password = QLineEdit()
        self.mt4_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.mt4_server = QLineEdit()
        
        mt4_layout.addRow("Login:", self.mt4_login)
        mt4_layout.addRow("Password:", self.mt4_password)
        mt4_layout.addRow("Server:", self.mt4_server)
        
        self.mt4_connect_btn = QPushButton("🔗 CONNECTER MT4")
        self.mt4_connect_btn.clicked.connect(self.handle_mt4_connect)
        mt4_layout.addRow(self.mt4_connect_btn)
        
        layout.addWidget(mt4_group)
        
        # Canaux Telegram
        channels_group = QGroupBox("📡 Canaux Telegram à Surveiller")
        channels_layout = QVBoxLayout()
        channels_group.setLayout(channels_layout)
        
        self.channel_forex_cb = QCheckBox("Forex")
        self.channel_crypto_cb = QCheckBox("Crypto")
        self.channel_gold_cb = QCheckBox("Gold")
        self.channel_indices_cb = QCheckBox("Indices")
        self.channel_actions_cb = QCheckBox("Actions")
        self.channel_commodites_cb = QCheckBox("Commodités")
        
        channels_layout.addWidget(self.channel_forex_cb)
        channels_layout.addWidget(self.channel_crypto_cb)
        channels_layout.addWidget(self.channel_gold_cb)
        channels_layout.addWidget(self.channel_indices_cb)
        channels_layout.addWidget(self.channel_actions_cb)
        channels_layout.addWidget(self.channel_commodites_cb)
        
        layout.addWidget(channels_group)
        
        # Configuration des Lots
        lots_group = QGroupBox("💰 Configuration des Lots")
        lots_layout = QFormLayout()
        lots_group.setLayout(lots_layout)
        
        self.lot_forex = QDoubleSpinBox()
        self.lot_forex.setDecimals(2)
        self.lot_forex.setMinimum(0.01)
        self.lot_forex.setMaximum(100.0)
        self.lot_forex.setSingleStep(0.01)
        self.lot_forex.setValue(0.01)
        
        self.lot_crypto = QDoubleSpinBox()
        self.lot_crypto.setDecimals(2)
        self.lot_crypto.setMinimum(0.01)
        self.lot_crypto.setMaximum(100.0)
        self.lot_crypto.setSingleStep(0.01)
        self.lot_crypto.setValue(0.01)
        
        self.lot_gold = QDoubleSpinBox()
        self.lot_gold.setDecimals(2)
        self.lot_gold.setMinimum(0.01)
        self.lot_gold.setMaximum(100.0)
        self.lot_gold.setSingleStep(0.01)
        self.lot_gold.setValue(0.01)
        
        lots_layout.addRow("Forex:", self.lot_forex)
        lots_layout.addRow("Crypto:", self.lot_crypto)
        lots_layout.addRow("Gold:", self.lot_gold)
        
        layout.addWidget(lots_group)
        
        # Boutons
        btn_layout = QHBoxLayout()
        
        self.save_config_btn = QPushButton("💾 Sauvegarder Configuration")
        self.save_config_btn.clicked.connect(self.save_configuration)
        btn_layout.addWidget(self.save_config_btn)
        
        self.start_trading_btn = QPushButton("▶️ DÉMARRER LE BOT")
        self.start_trading_btn.clicked.connect(self.start_trading)
        btn_layout.addWidget(self.start_trading_btn)
        
        self.stop_trading_btn = QPushButton("⏹️ ARRÊTER LE BOT")
        self.stop_trading_btn.clicked.connect(self.stop_trading)
        self.stop_trading_btn.setEnabled(False)
        btn_layout.addWidget(self.stop_trading_btn)
        
        layout.addLayout(btn_layout)
        layout.addStretch()
        
        return tab
    
    def create_signals_tab(self):
        """Onglet des signaux reçus"""
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        # Table des signaux
        self.signals_table = QTableWidget()
        self.signals_table.setColumnCount(7)
        self.signals_table.setHorizontalHeaderLabels([
            "Heure", "Canal", "Type", "Symbole", "Prix", "SL", "TP"
        ])
        self.signals_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.signals_table)
        
        return tab
    
    def create_positions_tab(self):
        """Onglet des positions ouvertes"""
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        # Bouton rafraîchir
        refresh_btn = QPushButton("🔄 Rafraîchir")
        refresh_btn.clicked.connect(self.refresh_positions)
        layout.addWidget(refresh_btn)
        
        # Table des positions
        self.positions_table = QTableWidget()
        self.positions_table.setColumnCount(8)
        self.positions_table.setHorizontalHeaderLabels([
            "Ticket", "Symbole", "Type", "Volume", "Prix d'entrée", "SL", "TP", "Profit"
        ])
        self.positions_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.positions_table)
        
        # Info compte
        self.account_info_label = QLabel("Balance: - | Équité: - | Profit: -")
        layout.addWidget(self.account_info_label)
        
        return tab
    
    def create_logs_tab(self):
        """Onglet des logs"""
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        # Zone de texte pour les logs
        self.logs_text = QTextEdit()
        self.logs_text.setReadOnly(True)
        layout.addWidget(self.logs_text)
        
        # Bouton clear
        clear_btn = QPushButton("🗑️ Effacer les logs")
        clear_btn.clicked.connect(self.logs_text.clear)
        layout.addWidget(clear_btn)
        
        return tab
    
    def set_tabs_enabled(self, enabled: bool):
        """Active/désactive les onglets selon l'état de connexion"""
        self.tabs.setTabEnabled(1, enabled)  # Config
        self.tabs.setTabEnabled(2, enabled)  # Signaux
        self.tabs.setTabEnabled(3, enabled)  # Positions
        self.tabs.setTabEnabled(4, enabled)  # Logs
    
    def try_auto_login(self):
        """Tente une connexion automatique avec token sauvegardé"""
        if self.auth_manager.load_token():
            self.log("✅ Connexion automatique réussie")
            self.on_login_success()
    
    def handle_login(self):
        """Gère la connexion"""
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        
        if not email or not password:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs")
            return
        
        self.log(f"Connexion en cours pour {email}...")
        self.login_btn.setEnabled(False)
        
        # Connexion
        if self.auth_manager.login(email, password):
            # Vérifier l'accès TRADABOT
            if self.auth_manager.verify_access():
                self.on_login_success()
            else:
                QMessageBox.critical(
                    self,
                    "Accès Refusé",
                    "Vous n'avez pas accès à TRADABOT.\nContactez un administrateur."
                )
                self.auth_manager.logout()
                self.login_btn.setEnabled(True)
        else:
            QMessageBox.critical(self, "Erreur", "Email ou mot de passe incorrect")
            self.login_btn.setEnabled(True)
    
    def on_login_success(self):
        """Appelé après connexion réussie"""
        self.is_logged_in = True
        self.log("✅ Connexion réussie")
        self.status_label.setText("🟢 Connecté")
        
        # UI
        self.login_btn.hide()
        self.logout_btn.show()
        self.email_input.setEnabled(False)
        self.password_input.setEnabled(False)
        self.set_tabs_enabled(True)
        self.tabs.setCurrentIndex(1)  # Aller à Config
        
        # Charger la configuration
        self.load_user_config()
        
        # Démarrer les timers de vérification
        self.access_check_timer.timeout.connect(self.check_access)
        self.access_check_timer.start(config.ACCESS_CHECK_INTERVAL * 1000)
        
        self.config_sync_timer.timeout.connect(self.sync_config)
        self.config_sync_timer.start(config.CONFIG_SYNC_INTERVAL * 1000)
    
    def handle_logout(self):
        """Gère la déconnexion"""
        # Arrêter le trading si actif
        if self.is_trading_active:
            self.stop_trading()
        
        # Déconnexion
        self.auth_manager.logout()
        self.is_logged_in = False
        
        # UI
        self.login_btn.show()
        self.logout_btn.hide()
        self.email_input.setEnabled(True)
        self.password_input.setEnabled(True)
        self.email_input.clear()
        self.password_input.clear()
        self.set_tabs_enabled(False)
        self.tabs.setCurrentIndex(0)
        self.status_label.setText("⚫ Déconnecté")
        
        # Arrêter les timers
        self.access_check_timer.stop()
        self.config_sync_timer.stop()
        
        self.log("🚪 Déconnecté")
    
    def load_user_config(self):
        """Charge la configuration utilisateur depuis l'API"""
        try:
            response = requests.get(
                config.API_TRADABOT_CONFIG,
                headers=self.auth_manager.get_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                self.user_config = response.json()
                self.apply_config_to_ui()
                self.log("✅ Configuration chargée")
            else:
                self.log(f"⚠️ Impossible de charger la config: {response.status_code}")
                
        except Exception as e:
            self.log(f"❌ Erreur chargement config: {e}")
    
    def apply_config_to_ui(self):
        """Applique la configuration à l'UI"""
        cfg = self.user_config
        
        # Canaux
        self.channel_forex_cb.setChecked(cfg.get('channelForexEnabled', False))
        self.channel_crypto_cb.setChecked(cfg.get('channelCryptoEnabled', False))
        self.channel_gold_cb.setChecked(cfg.get('channelGoldEnabled', False))
        self.channel_indices_cb.setChecked(cfg.get('channelIndicesEnabled', False))
        self.channel_actions_cb.setChecked(cfg.get('channelActionsEnabled', False))
        self.channel_commodites_cb.setChecked(cfg.get('channelCommoditesEnabled', False))
        
        # Lots
        self.lot_forex.setValue(cfg.get('lotForex', 0.01))
        self.lot_crypto.setValue(cfg.get('lotCrypto', 0.01))
        self.lot_gold.setValue(cfg.get('lotGold', 0.01))
    
    def save_configuration(self):
        """Sauvegarde la configuration sur le backend"""
        try:
            config_data = {
                'channelForexEnabled': self.channel_forex_cb.isChecked(),
                'channelCryptoEnabled': self.channel_crypto_cb.isChecked(),
                'channelGoldEnabled': self.channel_gold_cb.isChecked(),
                'channelIndicesEnabled': self.channel_indices_cb.isChecked(),
                'channelActionsEnabled': self.channel_actions_cb.isChecked(),
                'channelCommoditesEnabled': self.channel_commodites_cb.isChecked(),
                'lotForex': self.lot_forex.value(),
                'lotCrypto': self.lot_crypto.value(),
                'lotGold': self.lot_gold.value(),
                'lotIndices': 0.01,
                'lotActions': 0.01,
                'lotCommodites': 0.01,
                'breakevenEnabled': True
            }
            
            response = requests.post(
                config.API_TRADABOT_CONFIG,
                json=config_data,
                headers=self.auth_manager.get_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                self.user_config = config_data
                QMessageBox.information(self, "Succès", "Configuration sauvegardée ✅")
                self.log("✅ Configuration sauvegardée")
            else:
                QMessageBox.warning(self, "Erreur", f"Échec sauvegarde: {response.status_code}")
                
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur: {e}")
            self.log(f"❌ Erreur sauvegarde config: {e}")
    
    def handle_mt4_connect(self):
        """Connexion à MT4"""
        login = self.mt4_login.text().strip()
        password = self.mt4_password.text().strip()
        server = self.mt4_server.text().strip()
        
        if not login or not password or not server:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs MT4")
            return
        
        try:
            login_num = int(login)
            if self.mt4_manager.connect(login_num, password, server):
                QMessageBox.information(self, "Succès", "✅ Connecté à MT4")
                self.log(f"✅ MT4 connecté: {login}")
                self.mt4_connect_btn.setText("🔗 CONNECTÉ")
                self.mt4_connect_btn.setEnabled(False)
            else:
                QMessageBox.critical(self, "Erreur", "Échec connexion MT4")
        except ValueError:
            QMessageBox.warning(self, "Erreur", "Login MT4 doit être un nombre")
    
    def start_trading(self):
        """Démarre le bot de trading"""
        if not self.mt4_manager.is_connected:
            QMessageBox.warning(self, "Erreur", "Connectez-vous d'abord à MT4")
            return
        
        # Récupérer le token Telegram depuis le backend
        telegram_token = "8406540414:AAG-IlyhG5eL0BjSkvaJhZ2qCrngRETCHpc"
        
        # Créer et démarrer le thread Telegram
        self.telegram_thread = TelegramThread(telegram_token)
        self.telegram_thread.signal_received.connect(self.on_signal_received)
        self.telegram_thread.status_changed.connect(self.on_telegram_status_changed)
        
        # Configuration des canaux
        self.telegram_thread.enabled_channels = {
            'channelForexEnabled': self.channel_forex_cb.isChecked(),
            'channelCryptoEnabled': self.channel_crypto_cb.isChecked(),
            'channelGoldEnabled': self.channel_gold_cb.isChecked(),
            'channelIndicesEnabled': self.channel_indices_cb.isChecked(),
            'channelActionsEnabled': self.channel_actions_cb.isChecked(),
            'channelCommoditesEnabled': self.channel_commodites_cb.isChecked()
        }
        
        self.telegram_thread.start()
        
        # UI
        self.is_trading_active = True
        self.start_trading_btn.setEnabled(False)
        self.stop_trading_btn.setEnabled(True)
        self.status_label.setText("🟢 Bot Actif")
        
        # Démarrer le timer de vérification des positions
        self.position_check_timer.timeout.connect(self.check_positions_for_breakeven)
        self.position_check_timer.start(config.POSITION_CHECK_INTERVAL * 1000)
        
        self.log("🚀 BOT DÉMARRÉ - Surveillance active")
    
    def stop_trading(self):
        """Arrête le bot"""
        if self.telegram_thread:
            self.telegram_thread.stop()
            self.telegram_thread.wait()
            self.telegram_thread = None
        
        self.position_check_timer.stop()
        
        # UI
        self.is_trading_active = False
        self.start_trading_btn.setEnabled(True)
        self.stop_trading_btn.setEnabled(False)
        self.status_label.setText("🟡 Bot Arrêté")
        
        self.log("⏹️ BOT ARRÊTÉ")
    
    def on_signal_received(self, signal: dict):
        """Appelé quand un signal Telegram est reçu"""
        self.log(f"📡 Signal reçu: {signal['type']} {signal['symbol']}")
        
        # Ajouter à l'historique
        self.signals_history.append(signal)
        
        # Ajouter à la table
        row = self.signals_table.rowCount()
        self.signals_table.insertRow(row)
        
        time_str = datetime.now().strftime("%H:%M:%S")
        self.signals_table.setItem(row, 0, QTableWidgetItem(time_str))
        self.signals_table.setItem(row, 1, QTableWidgetItem(signal.get('channel', '')))
        self.signals_table.setItem(row, 2, QTableWidgetItem(signal['type']))
        self.signals_table.setItem(row, 3, QTableWidgetItem(signal['symbol']))
        self.signals_table.setItem(row, 4, QTableWidgetItem(str(signal.get('entry_price', ''))))
        self.signals_table.setItem(row, 5, QTableWidgetItem(str(signal.get('stop_loss', ''))))
        self.signals_table.setItem(row, 6, QTableWidgetItem(str(signal.get('take_profit1', ''))))
        
        # Exécuter le trade
        self.execute_trade(signal)
    
    def execute_trade(self, signal: dict):
        """Exécute un trade basé sur le signal"""
        try:
            # Calculer la taille du lot
            parser = SignalParser()
            lot_size = parser.calculate_lot_size(signal['symbol'], self.user_config)
            
            # Placer l'ordre
            ticket = self.mt4_manager.place_order(signal, lot_size)
            
            if ticket:
                self.log(f"✅ Trade exécuté: {signal['type']} {signal['symbol']} | Ticket: {ticket}")
            else:
                self.log(f"❌ Échec exécution trade: {signal['symbol']}")
                
        except Exception as e:
            self.log(f"❌ Erreur exécution trade: {e}")
    
    def on_telegram_status_changed(self, status: str):
        """Appelé quand le statut Telegram change"""
        if status == "running":
            self.log("✅ Monitor Telegram actif")
        elif status == "stopped":
            self.log("⏹️ Monitor Telegram arrêté")
        elif status.startswith("error"):
            self.log(f"❌ Erreur Telegram: {status}")
    
    def check_positions_for_breakeven(self):
        """Vérifie les positions pour activer le breakeven"""
        if not self.user_config.get('breakevenEnabled', False):
            return
        
        for ticket, pos_info in list(self.mt4_manager.positions.items()):
            # Skip si breakeven déjà actif
            if pos_info['breakeven_active']:
                continue
            
            # Vérifier si TP1 est atteint
            tp1_price = pos_info.get('take_profit1')
            if tp1_price:
                if self.mt4_manager.check_tp_reached(ticket, tp1_price):
                    self.log(f"🎯 TP1 atteint pour {pos_info['symbol']} (ticket {ticket})")
                    
                    # Fermer 50% de la position à TP1 si TP2 existe
                    if pos_info.get('take_profit2'):
                        half_volume = pos_info['lot_size'] / 2
                        if self.mt4_manager.close_partial_position(ticket, half_volume):
                            self.log(f"💰 50% fermé à TP1 pour {pos_info['symbol']}")
                    
                    # Activer le breakeven
                    if self.mt4_manager.move_to_breakeven(ticket):
                        self.log(f"🔒 Breakeven activé pour {pos_info['symbol']} (ticket {ticket})")
                        pos_info['breakeven_active'] = True
    
    def refresh_positions(self):
        """Rafraîchit l'affichage des positions"""
        positions = self.mt4_manager.get_open_positions()
        
        # Clear table
        self.positions_table.setRowCount(0)
        
        # Remplir avec les positions
        for pos in positions:
            row = self.positions_table.rowCount()
            self.positions_table.insertRow(row)
            
            self.positions_table.setItem(row, 0, QTableWidgetItem(str(pos['ticket'])))
            self.positions_table.setItem(row, 1, QTableWidgetItem(pos['symbol']))
            self.positions_table.setItem(row, 2, QTableWidgetItem(pos['type']))
            self.positions_table.setItem(row, 3, QTableWidgetItem(str(pos['volume'])))
            self.positions_table.setItem(row, 4, QTableWidgetItem(str(pos['price_open'])))
            self.positions_table.setItem(row, 5, QTableWidgetItem(str(pos['sl'])))
            self.positions_table.setItem(row, 6, QTableWidgetItem(str(pos['tp'])))
            
            # Colorer le profit
            profit_item = QTableWidgetItem(f"{pos['profit']:.2f} $")
            if pos['profit'] > 0:
                profit_item.setForeground(QColor(0, 255, 0))
            elif pos['profit'] < 0:
                profit_item.setForeground(QColor(255, 0, 0))
            self.positions_table.setItem(row, 7, profit_item)
        
        # Mettre à jour les infos du compte
        account_info = self.mt4_manager.get_account_info()
        if account_info:
            self.account_info_label.setText(
                f"Balance: {account_info['balance']:.2f} $ | "
                f"Équité: {account_info['equity']:.2f} $ | "
                f"Profit: {account_info['profit']:.2f} $"
            )
        
        self.log(f"🔄 {len(positions)} position(s) affichée(s)")
    
    def check_access(self):
        """Vérifie périodiquement l'accès TRADABOT"""
        if not self.auth_manager.verify_access():
            QMessageBox.critical(
                self,
                "Accès Révoqué",
                "Votre accès à TRADABOT a été révoqué.\nL'application va se déconnecter."
            )
            self.handle_logout()
    
    def sync_config(self):
        """Synchronise la configuration avec le backend"""
        self.load_user_config()
    
    def log(self, message: str):
        """Ajoute un message au log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        
        self.logs_text.append(log_entry)
        
        # Auto-scroll
        cursor = self.logs_text.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.logs_text.setTextCursor(cursor)
        
        # Logger aussi dans le fichier
        logger.info(message)
    
    def closeEvent(self, event):
        """Gère la fermeture de l'application"""
        if self.is_trading_active:
            reply = QMessageBox.question(
                self,
                "Confirmer",
                "Le bot est actif. Voulez-vous vraiment quitter?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.No:
                event.ignore()
                return
            
            self.stop_trading()
        
        # Déconnexion MT4
        if self.mt4_manager.is_connected:
            self.mt4_manager.disconnect()
        
        event.accept()


def main():
    """Point d'entrée de l'application"""
    app = QApplication(sys.argv)
    app.setApplicationName(config.APP_NAME)
    app.setApplicationVersion(config.APP_VERSION)
    
    window = TradaBotApp()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
