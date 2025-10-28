"""
TRADABOT - Version Test Linux (Sans MT4/MT5)
Cette version permet de tester l'interface et la connexion sans MetaTrader5
"""
import sys
import asyncio
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QTabWidget, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import requests
from datetime import datetime

# Import des modules locaux
from auth_manager import AuthManager
import config

class SimpleTradaBotApp(QMainWindow):
    """Version simplifiée pour tests Linux"""
    
    def __init__(self):
        super().__init__()
        
        self.auth_manager = AuthManager()
        self.is_logged_in = False
        
        self.init_ui()
        self.try_auto_login()
    
    def init_ui(self):
        """Initialise l'interface"""
        self.setWindowTitle(f"{config.APP_NAME} v{config.APP_VERSION} - TEST LINUX")
        self.setGeometry(100, 100, 800, 600)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Header
        header = QLabel(f"🤖 {config.APP_NAME} - Version Test")
        header_font = QFont()
        header_font.setPointSize(20)
        header_font.setBold(True)
        header.setFont(header_font)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(header)
        
        # Status
        self.status_label = QLabel("⚫ Déconnecté")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.status_label)
        
        # Tabs
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # Login tab
        self.tab_login = self.create_login_tab()
        self.tabs.addTab(self.tab_login, "🔐 Connexion")
        
        # Info tab
        self.tab_info = self.create_info_tab()
        self.tabs.addTab(self.tab_info, "ℹ️ Informations")
        
        # Logs tab
        self.logs_text = QTextEdit()
        self.logs_text.setReadOnly(True)
        self.tabs.addTab(self.logs_text, "📋 Logs")
        
        # Style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a1a;
            }
            QWidget {
                background-color: #1a1a1a;
                color: #ffffff;
            }
            QPushButton {
                background-color: #3a8fd9;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2e7bc4;
            }
            QPushButton:disabled {
                background-color: #555555;
            }
            QLineEdit, QTextEdit {
                background-color: #3a3a3a;
                border: 1px solid #555555;
                padding: 8px;
                border-radius: 3px;
            }
            QTabWidget::pane {
                border: 1px solid #3a3a3a;
                background-color: #2a2a2a;
            }
            QTabBar::tab {
                background-color: #2a2a2a;
                color: #ffffff;
                padding: 10px 20px;
            }
            QTabBar::tab:selected {
                background-color: #3a8fd9;
            }
        """)
    
    def create_login_tab(self):
        """Onglet de connexion"""
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        layout.addStretch()
        
        # Form
        form_widget = QWidget()
        form_layout = QVBoxLayout()
        form_widget.setLayout(form_layout)
        
        email_label = QLabel("📧 Email:")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("votre@email.com")
        
        password_label = QLabel("🔒 Mot de passe:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Mot de passe")
        
        form_layout.addWidget(email_label)
        form_layout.addWidget(self.email_input)
        form_layout.addWidget(password_label)
        form_layout.addWidget(self.password_input)
        
        layout.addWidget(form_widget)
        
        # Buttons
        self.login_btn = QPushButton("🚀 SE CONNECTER")
        self.login_btn.clicked.connect(self.handle_login)
        layout.addWidget(self.login_btn)
        
        self.logout_btn = QPushButton("🚪 SE DÉCONNECTER")
        self.logout_btn.clicked.connect(self.handle_logout)
        self.logout_btn.hide()
        layout.addWidget(self.logout_btn)
        
        layout.addStretch()
        
        return tab
    
    def create_info_tab(self):
        """Onglet d'informations"""
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        info = QTextEdit()
        info.setReadOnly(True)
        info.setHtml(f"""
        <h2 style="color: #3a8fd9;">TRADABOT - Version Test Linux</h2>
        <p><strong>Version:</strong> {config.APP_VERSION}</p>
        <p><strong>Backend:</strong> {config.API_BASE_URL}</p>
        
        <h3 style="color: #3a8fd9;">⚠️ Version de Test</h3>
        <p>Cette version est limitée pour les tests sur Linux:</p>
        <ul>
            <li>✅ Authentification tradalife.com</li>
            <li>✅ Vérification accès TRADABOT</li>
            <li>✅ Interface graphique</li>
            <li>❌ MetaTrader 4/5 (Windows uniquement)</li>
            <li>❌ Surveillance Telegram (nécessite async loop)</li>
            <li>❌ Exécution trades</li>
        </ul>
        
        <h3 style="color: #3a8fd9;">📦 Build Complet</h3>
        <p>Pour la version complète avec toutes les fonctionnalités:</p>
        <ol>
            <li>Transférer le package sur Windows</li>
            <li>Exécuter: install.bat</li>
            <li>Exécuter: build.bat</li>
            <li>Lancer: dist/TRADABOT.exe</li>
        </ol>
        
        <h3 style="color: #3a8fd9;">📡 Canaux Telegram Configurés</h3>
        <ul>
            <li><strong>Forex:</strong> {config.TELEGRAM_CHANNELS['forex']}</li>
            <li><strong>Crypto:</strong> {config.TELEGRAM_CHANNELS['crypto']}</li>
            <li><strong>Gold:</strong> {config.TELEGRAM_CHANNELS['gold']}</li>
            <li><strong>Indices:</strong> {config.TELEGRAM_CHANNELS['indices']}</li>
            <li><strong>Actions:</strong> {config.TELEGRAM_CHANNELS['actions']}</li>
            <li><strong>Commodités:</strong> {config.TELEGRAM_CHANNELS['commodites']}</li>
        </ul>
        
        <h3 style="color: #3a8fd9;">🔐 Accès Admin</h3>
        <p><strong>Email:</strong> yafoy2310@gmail.com</p>
        <p><strong>Accès:</strong> Gratuit et illimité</p>
        """)
        
        layout.addWidget(info)
        
        return tab
    
    def try_auto_login(self):
        """Tente connexion automatique"""
        if self.auth_manager.load_token():
            self.log("✅ Connexion automatique réussie")
            self.on_login_success()
    
    def handle_login(self):
        """Connexion"""
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        
        if not email or not password:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs")
            return
        
        self.log(f"Connexion en cours pour {email}...")
        self.login_btn.setEnabled(False)
        
        if self.auth_manager.login(email, password):
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
        """Appelé après connexion"""
        self.is_logged_in = True
        self.log("✅ Connexion réussie")
        self.status_label.setText("🟢 Connecté")
        
        self.login_btn.hide()
        self.logout_btn.show()
        self.email_input.setEnabled(False)
        self.password_input.setEnabled(False)
        
        # Afficher infos utilisateur
        user_info = self.auth_manager.get_user_info()
        if user_info:
            self.log(f"👤 Utilisateur: {user_info.get('email')}")
            self.log(f"🔑 Rôle: {user_info.get('role', 'user')}")
    
    def handle_logout(self):
        """Déconnexion"""
        self.auth_manager.logout()
        self.is_logged_in = False
        
        self.login_btn.show()
        self.logout_btn.hide()
        self.email_input.setEnabled(True)
        self.password_input.setEnabled(True)
        self.email_input.clear()
        self.password_input.clear()
        self.status_label.setText("⚫ Déconnecté")
        
        self.log("🚪 Déconnecté")
    
    def log(self, message: str):
        """Ajoute un log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.logs_text.append(log_entry)


def main():
    """Point d'entrée"""
    print("=" * 50)
    print("  TRADABOT - Version Test Linux")
    print("=" * 50)
    print("")
    print("⚠️  Cette version est limitée (pas de MT4/MT5)")
    print("📦 Pour la version complète, build sur Windows")
    print("")
    
    app = QApplication(sys.argv)
    app.setApplicationName(config.APP_NAME)
    app.setApplicationVersion(config.APP_VERSION)
    
    window = SimpleTradaBotApp()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
