# 🤖 TRADABOT Desktop Application

Bot de copy trading MT4 pour TRADALIFE

## 📋 Installation

### Windows:
```bash
pip install -r requirements.txt
python main.py
```

### Mac:
```bash
pip3 install -r requirements.txt
python3 main.py
```

## 🚀 Utilisation

1. Lancez l'application
2. Connectez-vous avec vos identifiants tradalife.com
3. Configurez vos paramètres MT4
4. Sélectionnez les canaux à surveiller
5. Cliquez sur "Démarrer le Bot"

## 📦 Packaging

### Windows .exe:
```bash
pyinstaller --onefile --windowed --name TRADABOT --icon=icon.ico main.py
```

### Mac .app:
```bash
pyinstaller --onefile --windowed --name TRADABOT --icon=icon.icns main.py
```

## 🔧 Configuration

La configuration est automatiquement synchronisée depuis tradalife.com

## 📝 Logs

Les logs sont sauvegardés dans le dossier `logs/`

## ⚠️ Important

- Nécessite un compte MT4/MT5 actif
- Nécessite l'achat de TRADABOT (300$ CAD) sur tradalife.com
- Connexion internet stable requise

## 🆘 Support

En cas de problème: support@tradalife.com
