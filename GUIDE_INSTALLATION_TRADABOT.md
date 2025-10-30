# 🔧 GUIDE D'INSTALLATION DU CONNECTEUR TRADABOT - VERSION AMÉLIORÉE

## ⚠️ PROBLÈME RÉSOLU

Le problème d'écran noir était dû au fait que le connecteur essayait de démarrer sans configuration valide. La nouvelle version corrige ce problème avec:

1. **Installation simplifiée** avec `INSTALLER.bat`
2. **Configuration automatique** via fichier JSON
3. **Messages d'erreur clairs** au lieu d'un écran noir
4. **Instructions pas-à-pas** pour guider l'utilisateur

## 📋 NOUVELLE PROCÉDURE D'INSTALLATION

### Étape 1: Télécharger le Connecteur
1. Connectez-vous sur https://tradalife.com/tradabot-web
2. Cliquez sur "📥 Télécharger le Connecteur"
3. Extrayez le fichier ZIP dans un dossier (ex: `C:\TRADABOT`)

### Étape 2: Installation des Dépendances
1. **Double-cliquez sur `INSTALLER.bat`**
2. Le script vérifiera Python et installera automatiquement:
   - MetaTrader5 (pour la connexion MT4/MT5)
   - Requests (pour communiquer avec le serveur)
3. Si Python n'est pas installé, le script vous guidera

### Étape 3: Configuration
1. Allez sur https://tradalife.com/tradabot-web
2. Configurez vos paramètres dans l'onglet "⚙️ Configuration":
   - Login MT4
   - Mot de passe MT4
   - Serveur MT4
   - Canaux actifs (Forex, Crypto, Gold, etc.)
   - Tailles de lots
3. Cliquez sur "💾 Sauvegarder la Configuration"
4. Cliquez sur "📥 Télécharger tradabot_config.json"
5. **Placez le fichier `tradabot_config.json` dans le dossier du connecteur**

### Étape 4: Lancement
1. **Ouvrez MetaTrader 4 ou 5** et connectez-vous
2. **Double-cliquez sur `LANCER_TRADABOT.bat`**
3. Le connecteur se lancera et affichera:
   - ✅ Configuration chargée
   - ✅ Connecté à MT5
   - 📊 Attente de signaux...

## 🆕 AMÉLIORATIONS

### Avant (Version Ancienne)
❌ Écran noir qui apparaît et disparaît
❌ Pas de message d'erreur
❌ Difficile de comprendre le problème
❌ Configuration avec variables d'environnement complexes

### Maintenant (Nouvelle Version)
✅ Messages clairs à chaque étape
✅ Installation automatique des dépendances
✅ Configuration via fichier JSON simple
✅ Instructions intégrées dans les scripts
✅ Détection automatique des problèmes
✅ Interface de configuration web

## 🎯 CONTENU DU PACKAGE

Le nouveau package contient:

```
TRADABOT_CONNECTOR/
├── INSTALLER.bat              ← Double-cliquez en premier
├── LANCER_TRADABOT.bat        ← Lancez après configuration
├── TradabotConnector.exe      ← Programme principal
├── connector_launcher.py      ← Lanceur avec vérifications
├── connector.py               ← Code source
├── requirements.txt           ← Liste des dépendances
└── README.txt                 ← Instructions complètes
```

## 🐛 RÉSOLUTION DES PROBLÈMES COURANTS

### Problème: "Python n'est pas installé"
**Solution:**
1. Téléchargez Python sur https://www.python.org/downloads/
2. ⚠️ **COCHEZ "Add Python to PATH"** pendant l'installation
3. Redémarrez votre ordinateur
4. Relancez `INSTALLER.bat`

### Problème: "Configuration manquante"
**Solution:**
1. Allez sur https://tradalife.com/tradabot-web
2. Configurez vos paramètres
3. Téléchargez `tradabot_config.json`
4. Placez-le dans le dossier du connecteur

### Problème: "Échec connexion MT5"
**Solution:**
- Vérifiez que MetaTrader est ouvert
- Vérifiez vos identifiants (login, mot de passe, serveur)
- Assurez-vous d'avoir une connexion internet
- Le serveur doit correspondre exactement à celui de votre compte

### Problème: "Token d'authentification manquant"
**Solution:**
- Re-téléchargez le fichier `tradabot_config.json` depuis le site
- Assurez-vous qu'il est bien dans le dossier du connecteur
- Ne modifiez pas le contenu du fichier manuellement

## 📊 VÉRIFICATION DU FONCTIONNEMENT

Quand tout fonctionne correctement, vous devriez voir:

```
✅ Configuration chargée
🔗 Backend: https://edushop-portal.emergent.host

🚀 Démarrage TRADABOT Connector...
✅ Configuration chargée
✅ Connecté à MT5 - Compte: 12345678
   Balance: 10000.00 USD
   Leverage: 1:500
✅ TRADABOT Connector actif
📊 Attente de signaux...
```

## 💡 CONSEILS IMPORTANTS

1. **Ne fermez pas la fenêtre** du connecteur pendant le trading
2. **Gardez MetaTrader ouvert** et connecté
3. **Vérifiez régulièrement** le fichier `tradabot_connector.log`
4. **Utilisez un VPS** si vous ne pouvez pas laisser votre PC allumé 24/7
5. **Testez d'abord** avec de petits lots

## 📞 SUPPORT

Si vous rencontrez toujours des problèmes:
- Telegram: @tradalife_support
- Email: support@tradalife.com
- Consultez le fichier `tradabot_connector.log` pour plus de détails

---

**Version:** 2.0 (Améliorée)
**Date:** Janvier 2025
**Compatibilité:** Windows 7/8/10/11
