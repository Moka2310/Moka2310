# 🤖 TRADABOT - GUIDE ULTRA SIMPLE

## 📥 INSTALLATION EN 3 ÉTAPES

### ÉTAPE 1: Installer Python et les dépendances
1. **Double-cliquez sur `INSTALLATION_SIMPLE.bat`**
2. Suivez les instructions
3. Si Python n'est pas installé, le script ouvrira la page de téléchargement
   - ⚠️ **IMPORTANT**: Cochez "Add Python to PATH" pendant l'installation!
4. Redémarrez votre PC après l'installation de Python
5. Relancez `INSTALLATION_SIMPLE.bat`

### ÉTAPE 2: Télécharger votre configuration
1. Allez sur **https://tradalife.com/tradabot-web**
2. Connectez-vous
3. Configurez vos paramètres MT4/MT5
4. Cliquez sur **"Télécharger tradabot_config.json"**
5. **Placez le fichier dans le dossier TRADABOT** (à côté des autres fichiers)

### ÉTAPE 3: Lancer le bot
1. **Ouvrez MetaTrader 4 ou 5** et connectez-vous
2. **Double-cliquez sur `DEMARRER_TRADABOT.bat`**
3. C'est tout! Le bot est actif ✅

## 📁 CONTENU DU DOSSIER

```
TRADABOT/
├── INSTALLATION_SIMPLE.bat      ← Double-cliquez EN PREMIER
├── DEMARRER_TRADABOT.bat        ← Double-cliquez pour lancer
├── tradabot_simple.py           ← Le programme (Python)
├── tradabot_config.json         ← À télécharger depuis le site
└── README_SIMPLE.txt            ← Ce fichier
```

## ✅ VÉRIFICATION

Quand tout fonctionne, vous verrez:

```
🤖 TRADABOT CONNECTEUR - Chargement...
✅ MetaTrader5 chargé
✅ Requests chargé
✅ Configuration chargée
✅ Utilisateur: votre@email.com
✅ Serveur: ICMarkets-Live

🔗 CONNEXION À METATRADER...
✅ MT5 initialisé
✅ CONNECTÉ À MT5!
   Compte: 12345678
   Balance: 10000.00 USD
   Levier: 1:500

🚀 TRADABOT ACTIF - EN ATTENTE DE SIGNAUX
```

## ❌ PROBLÈMES COURANTS

### "Python n'est pas installé"
1. Téléchargez Python: https://www.python.org/downloads/
2. **COCHEZ "Add Python to PATH"** pendant l'installation
3. Redémarrez votre PC
4. Relancez `INSTALLATION_SIMPLE.bat`

### "Configuration manquante"
1. Allez sur https://tradalife.com/tradabot-web
2. Téléchargez `tradabot_config.json`
3. Placez-le dans le dossier TRADABOT

### "Échec connexion MT5"
- Vérifiez que MetaTrader est OUVERT
- Vérifiez vos identifiants (login, mot de passe, serveur)
- Re-configurez depuis le site si nécessaire

### Le programme se ferme immédiatement
- Vérifiez que Python est bien installé: ouvrez CMD et tapez `python --version`
- Relancez `INSTALLATION_SIMPLE.bat`
- Assurez-vous que le fichier `tradabot_config.json` est présent

## ⚠️ IMPORTANT

- **Ne fermez pas la fenêtre** du bot pendant le trading
- **Gardez MetaTrader ouvert** et connecté
- **Connexion internet stable** requise
- **Utilisez un VPS** si vous ne pouvez pas laisser votre PC allumé 24/7

## 📞 BESOIN D'AIDE?

- **Telegram**: @tradalife_support
- **Email**: support@tradalife.com
- **Site**: https://tradalife.com

## 📝 NOTES

- Version: 2.0 (Simplifiée)
- Compatible: Windows 7/8/10/11
- Nécessite: Python 3.7+, MetaTrader 4/5

---

**C'est tout! Vraiment simple! 🚀**
