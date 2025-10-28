# 🤖 TRADABOT - Application Desktop de Trading Automatique

Application desktop Windows pour le trading automatisé basé sur les signaux Telegram des canaux VIP de Tradalife.

## 📋 Fonctionnalités

- ✅ **Authentification** avec compte tradalife.com
- ✅ **Surveillance automatique** de 6 canaux Telegram VIP
- ✅ **Parsing intelligent** des signaux de trading
- ✅ **Exécution automatique** des trades sur MT4/MT5
- ✅ **Configuration des lots** par catégorie (Forex, Crypto, Gold, etc.)
- ✅ **Breakeven automatique** quand TP1 est atteint
- ✅ **Interface graphique** intuitive et moderne
- ✅ **Logs complets** de toutes les opérations
- ✅ **Gestion des positions** en temps réel

## 🎯 Canaux Telegram Surveillés

1. **Forex** (-1002425540174)
2. **Crypto** (-1002279973041)
3. **Gold** (-1002355600472)
4. **Indices** (-1002339785500)
5. **Actions** (-1002376632406)
6. **Commodités** (-1002368060694)

## 🔧 Prérequis

### Sur Windows (utilisateur final)
- Windows 10/11 (64-bit)
- MetaTrader 4 ou MetaTrader 5 installé
- Compte de trading actif (démo ou réel)
- Compte tradalife.com avec accès TRADABOT

### Pour le développement
- Python 3.11+
- Toutes les dépendances dans `requirements.txt`
- Environnement Windows (pour MetaTrader5)

## 📦 Installation (Développeur)

```bash
# Cloner le dossier
cd tradabot-app

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
python app.py
```

## 🏗️ Build de l'exécutable Windows

**⚠️ Important: Le build doit être fait sur une machine Windows**

```bash
# 1. Sur une machine Windows avec Python installé
pip install -r requirements.txt

# 2. Installer PyInstaller
pip install pyinstaller

# 3. Exécuter le script de build
python build_windows.py

# 4. L'exécutable sera dans dist/TRADABOT.exe
```

### Build Manuel (alternative)

```bash
pyinstaller --onefile --windowed --name=TRADABOT \
  --hidden-import=PyQt6 \
  --hidden-import=telegram \
  --hidden-import=MetaTrader5 \
  --hidden-import=loguru \
  --hidden-import=cryptography \
  --hidden-import=requests \
  app.py
```

## 🚀 Utilisation

### 1️⃣ Première Connexion

1. Lancer `TRADABOT.exe`
2. Entrer vos identifiants tradalife.com
3. Le système vérifie automatiquement votre accès TRADABOT

### 2️⃣ Configuration MT4/MT5

1. Aller dans l'onglet **Configuration**
2. Entrer vos identifiants MT4/MT5:
   - **Login**: Numéro de compte
   - **Password**: Mot de passe
   - **Server**: Serveur du broker (ex: `GlobalPrime-Demo`)
3. Cliquer sur **CONNECTER MT4**

### 3️⃣ Configuration des Canaux

1. Cocher les canaux Telegram à surveiller
2. Définir la taille des lots pour chaque catégorie:
   - Forex: 0.01 (par défaut)
   - Crypto: 0.01 (par défaut)
   - Gold: 0.01 (par défaut)

### 4️⃣ Démarrer le Bot

1. Cliquer sur **DÉMARRER LE BOT**
2. Le bot surveille les canaux et exécute automatiquement les trades
3. Voir les signaux dans l'onglet **Signaux**
4. Suivre les positions dans l'onglet **Positions**

### 5️⃣ Arrêter le Bot

- Cliquer sur **ARRÊTER LE BOT** à tout moment
- Les positions ouvertes restent actives dans MT4

## 📊 Format des Signaux Telegram

Le bot reconnaît les formats suivants:

```
BUY XAUUSD @2045.50, TP1: 2050.00, TP2: 2055.00, SL: 2040.00
SELL EURUSD @1.0850, TP: 1.0820, SL: 1.0870
BUY BTCUSD @45000, TP1: 46000, TP2: 47000, SL: 44000, BREAKEVEN
```

**Informations extraites:**
- Type d'ordre: `BUY` ou `SELL`
- Symbole: `XAUUSD`, `EURUSD`, `BTCUSD`, etc.
- Prix d'entrée: `@2045.50`
- Stop Loss: `SL: 2040.00`
- Take Profit 1: `TP1: 2050.00`
- Take Profit 2: `TP2: 2055.00` (optionnel)
- Breakeven: détecté automatiquement

## 🔐 Sécurité

- **Token chiffré**: Le token de connexion est stocké de manière sécurisée (crypté avec Fernet)
- **Vérification d'accès**: L'application vérifie périodiquement l'accès TRADABOT
- **Pas de stockage de mot de passe MT4**: Les identifiants MT4 doivent être ressaisis à chaque lancement

## 🏗️ Architecture

```
tradabot-app/
├── app.py                  # Application principale (GUI PyQt6)
├── auth_manager.py         # Gestion authentification
├── telegram_monitor.py     # Surveillance canaux Telegram
├── mt4_manager.py          # Connexion et ordres MT4/MT5
├── signal_parser.py        # Parsing des signaux
├── config.py               # Configuration
├── requirements.txt        # Dépendances Python
├── build_windows.py        # Script de build
├── README.md               # Ce fichier
├── data/                   # Données locales (token, config)
└── logs/                   # Logs de l'application
```

## 🔄 Fonctionnement Technique

### Authentification
1. Connexion via API `/api/auth/login`
2. Vérification accès via `/api/tradabot/access`
3. Token sauvegardé localement (chiffré)

### Surveillance Telegram
1. Connexion au Bot Telegram avec le token
2. Écoute des messages des canaux configurés
3. Parsing automatique des signaux

### Exécution des Trades
1. Signal reçu → Parsing
2. Calcul du lot selon la configuration
3. Envoi ordre à MT4/MT5 via API MetaTrader5
4. Suivi de la position pour breakeven

### Breakeven Automatique
- Quand TP1 est atteint, le SL est déplacé au prix d'entrée
- Vérification toutes les secondes (configurable)

## 🐛 Dépannage

### Erreur "MetaTrader5 non disponible"
- ✅ Solution: Installer MetaTrader 4 ou 5 sur Windows

### Erreur "Accès TRADABOT refusé"
- ✅ Vérifier que votre compte a accès (contactez admin)
- ✅ Admin email: `yafoy2310@gmail.com` a accès gratuit

### Le bot ne reçoit pas les signaux
- ✅ Vérifier que les canaux sont cochés
- ✅ Vérifier la connexion internet
- ✅ Voir les logs dans l'onglet **Logs**

### Ordre non exécuté sur MT4
- ✅ Vérifier la connexion MT4 (login/password/server)
- ✅ Vérifier que le symbole existe dans MT4
- ✅ Vérifier la taille du lot (minimum broker)

## 📞 Support

- **Website**: https://tradalife.com
- **Email Admin**: yafoy2310@gmail.com
- **Backend API**: https://mt4-dropdown.preview.emergentagent.com

## 📝 Changelog

### Version 1.0.0 (2025-01-XX)
- ✅ Version initiale
- ✅ Authentification tradalife.com
- ✅ Surveillance 6 canaux Telegram
- ✅ Intégration MT4/MT5
- ✅ Configuration lots par catégorie
- ✅ Breakeven automatique
- ✅ Interface PyQt6

## 🔜 Roadmap

- [ ] Support Mac OS (si possible)
- [ ] Multi-comptes MT4/MT5
- [ ] Statistiques avancées
- [ ] Export des trades (CSV, Excel)
- [ ] Notifications push
- [ ] Mode démo (sans exécution réelle)

## 📄 Licence

© 2025 Tradalife. Tous droits réservés.
Cette application est réservée aux membres ayant accès TRADABOT.
