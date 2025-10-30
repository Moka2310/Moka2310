# 🤖 TRADABOT CONNECTEUR MT4/MT5

Connecteur local pour exécuter automatiquement les signaux TRADABOT sur MetaTrader 4/5.

## 📋 Prérequis

- Windows 7/8/10/11
- Python 3.7 ou supérieur
- MetaTrader 4 ou MetaTrader 5 installé
- Connexion internet stable
- Compte TRADABOT payé (300$ CAD)

## 🚀 Installation Rapide

### Étape 1: Extraire les fichiers
1. Téléchargez le package ZIP depuis votre espace membre
2. Extrayez tous les fichiers dans un dossier (par exemple: `C:\TRADABOT`)

### Étape 2: Installation
1. Double-cliquez sur `INSTALLER.bat`
2. Suivez les instructions à l'écran
3. Le script installera automatiquement toutes les dépendances nécessaires

### Étape 3: Configuration
1. Connectez-vous sur https://tradalife.com/tradabot-web
2. Allez dans la section "Configuration"
3. Remplissez vos informations MT4/MT5:
   - Login
   - Mot de passe
   - Serveur
4. Sélectionnez les canaux que vous souhaitez suivre
5. Ajustez les tailles de lots pour chaque actif
6. Cliquez sur "Télécharger la Configuration"
7. Placez le fichier `tradabot_config.json` dans le dossier du connecteur

### Étape 4: Lancement
1. Assurez-vous que MetaTrader est ouvert et connecté
2. Double-cliquez sur `LANCER_TRADABOT.bat`
3. Le connecteur se lancera et commencera à surveiller les signaux

## ⚙️ Configuration Manuelle

Si vous préférez créer le fichier de configuration manuellement:

```json
{
  "authToken": "VOTRE_TOKEN_ICI",
  "backendUrl": "https://edushop-portal.emergent.host",
  "mt4Login": "12345678",
  "mt4Password": "VotreMotDePasse",
  "mt4Server": "ICMarkets-Live",
  "channels": {
    "forex": true,
    "crypto": true,
    "gold": true,
    "indices": true,
    "commodites": true
  },
  "lots": {
    "forex": 0.01,
    "crypto": 0.01,
    "gold": 0.01,
    "indices": 0.01,
    "commodites": 0.01
  },
  "breakevenEnabled": true
}
```

Sauvegardez ce fichier sous le nom `tradabot_config.json`.

## 🎯 Fonctionnalités

- ✅ **Exécution automatique**: Les signaux sont copiés automatiquement sur MT4/MT5
- ✅ **Breakeven automatique**: Le SL se déplace au point d'entrée après +15 pips
- ✅ **Multi-canaux**: Forex, Crypto, Gold, Indices, Commodités
- ✅ **Lots personnalisables**: Ajustez la taille selon votre capital
- ✅ **Monitoring en temps réel**: Suivez vos trades depuis le site web

## ⚠️ Important

- **Le connecteur doit rester en exécution** pendant les heures de trading
- Ne fermez pas la fenêtre du connecteur
- Gardez MetaTrader ouvert et connecté
- Utilisez un VPS Windows si vous ne pouvez pas laisser votre PC allumé 24/7

## 🐛 Dépannage

### Le connecteur ne démarre pas
- Vérifiez que Python est installé: `python --version`
- Réexécutez `INSTALLER.bat`
- Vérifiez que le fichier `tradabot_config.json` est présent

### Erreur de connexion MT4/MT5
- Vérifiez que MetaTrader est ouvert
- Vérifiez vos identifiants (login, mot de passe, serveur)
- Assurez-vous d'avoir une connexion internet

### Les signaux ne s'exécutent pas
- Vérifiez que les canaux sont activés dans votre configuration
- Vérifiez que le bot est en mode "Running" sur le site web
- Consultez les logs dans `tradabot_connector.log`

### Python n'est pas installé
1. Téléchargez Python depuis https://www.python.org/downloads/
2. **IMPORTANT**: Cochez "Add Python to PATH" pendant l'installation
3. Redémarrez votre ordinateur
4. Réexécutez `INSTALLER.bat`

## 📊 Logs

Les logs sont enregistrés dans `tradabot_connector.log`. Consultez ce fichier pour voir:
- Les signaux reçus
- Les ordres exécutés
- Les erreurs éventuelles
- L'état de la connexion MT4/MT5

## 📞 Support

Pour toute question ou problème:
- Telegram: @tradalife_support
- Email: support@tradalife.com
- Site web: https://tradalife.com

## 📝 Notes

- Version: 1.0.0
- Compatible: Windows 7/8/10/11
- Dernière mise à jour: Janvier 2025
