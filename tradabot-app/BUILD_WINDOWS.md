# 📦 TRADABOT - Guide de Build Windows

Ce guide explique comment créer l'exécutable TRADABOT.exe pour Windows.

## ⚠️ Important

**Le build DOIT être fait sur une machine Windows** car MetaTrader5 n'est disponible que pour Windows.

## 🔧 Prérequis

1. **Windows 10/11** (64-bit)
2. **Python 3.11 ou supérieur**
   - Télécharger: https://www.python.org/downloads/
   - ✅ Cocher "Add Python to PATH" lors de l'installation
3. **MetaTrader 4 ou 5** installé
4. **Git** (optionnel, pour cloner le repo)

## 📝 Étapes de Build

### Étape 1: Préparer l'environnement

Ouvrir PowerShell ou CMD en tant qu'administrateur:

```bash
# Vérifier Python
python --version

# Devrait afficher: Python 3.11.x ou supérieur
```

### Étape 2: Récupérer le code source

Option A - Avec Git:
```bash
git clone https://github.com/tradalife/tradabot-app.git
cd tradabot-app
```

Option B - Sans Git:
1. Télécharger le ZIP du repository
2. Extraire dans un dossier (ex: `C:\tradabot-app`)
3. Ouvrir CMD dans ce dossier

### Étape 3: Créer un environnement virtuel (recommandé)

```bash
# Créer l'environnement
python -m venv venv

# Activer l'environnement
venv\Scripts\activate

# Vous devriez voir (venv) dans votre prompt
```

### Étape 4: Installer les dépendances

```bash
# Mettre à jour pip
python -m pip install --upgrade pip

# Installer les dépendances
pip install -r requirements.txt

# Installer PyInstaller
pip install pyinstaller
```

### Étape 5: Tester l'application

Avant de faire le build, tester que tout fonctionne:

```bash
python app.py
```

L'application devrait se lancer avec l'interface graphique.
Fermer l'application si elle fonctionne.

### Étape 6: Créer l'exécutable

Option A - Avec le script automatique:
```bash
python build_windows.py
```

Option B - Manuellement:
```bash
pyinstaller --onefile --windowed --name=TRADABOT ^
  --hidden-import=PyQt6 ^
  --hidden-import=telegram ^
  --hidden-import=MetaTrader5 ^
  --hidden-import=loguru ^
  --hidden-import=cryptography ^
  --hidden-import=requests ^
  app.py
```

⏳ **Le build peut prendre 5-10 minutes** selon votre machine.

### Étape 7: Récupérer l'exécutable

L'exécutable se trouve dans:
```
dist/TRADABOT.exe
```

**Taille attendue**: ~50-80 MB (contient Python et toutes les dépendances)

### Étape 8: Tester l'exécutable

```bash
cd dist
TRADABOT.exe
```

L'application devrait se lancer sans problème.

## 📦 Distribution

### Fichier à distribuer:
- `TRADABOT.exe` (dans le dossier `dist/`)

### Instructions pour l'utilisateur final:

1. **Télécharger** TRADABOT.exe
2. **Placer** dans un dossier (ex: `C:\TRADABOT\`)
3. **Double-cliquer** pour lancer
4. **Première utilisation**:
   - Entrer email/password tradalife.com
   - Configurer MT4/MT5
   - Démarrer le bot

**Note**: Windows Defender peut afficher un avertissement la première fois.
C'est normal pour les applications non signées. Cliquer sur "Plus d'infos" puis "Exécuter quand même".

## 🔐 Signature de Code (Optionnel - Production)

Pour éviter l'avertissement Windows Defender, signer le .exe avec un certificat:

```bash
# Nécessite un certificat de signature de code
signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com TRADABOT.exe
```

**Coût**: ~300-500$ USD/an pour un certificat de signature.

## 🐛 Problèmes Courants

### Erreur: "Python was not found"
**Solution**: Réinstaller Python et cocher "Add Python to PATH"

### Erreur: "No module named 'PyQt6'"
**Solution**: Réinstaller les dépendances:
```bash
pip install -r requirements.txt
```

### Erreur lors du build: "Failed to execute script"
**Solution**: Vérifier que toutes les dépendances sont installées:
```bash
pip list
```

### .exe ne se lance pas
**Solution**: Tester en ligne de commande pour voir les erreurs:
```bash
cd dist
TRADABOT.exe
```

### Erreur: "MetaTrader5 module not found"
**Solution**: Le build doit être fait sur Windows avec MT4/MT5 installé:
```bash
# Installer MetaTrader5
pip install MetaTrader5
```

## 📊 Optimisation de la Taille

L'exécutable fait ~50-80 MB. Pour réduire:

### Option 1: Compression UPX
```bash
# Installer UPX
# Télécharger: https://github.com/upx/upx/releases

# Compresser l'exe
upx --best TRADABOT.exe

# Réduction: ~30-40%
```

### Option 2: Exclure des modules
Modifier `build_windows.py` pour exclure des modules inutiles:
```python
'--exclude-module=matplotlib',
'--exclude-module=scipy',
```

## 🚀 Build Automatisé (CI/CD)

Pour automatiser le build avec GitHub Actions:

```yaml
# .github/workflows/build-windows.yml
name: Build Windows
on: [push]
jobs:
  build:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pip install pyinstaller
      - run: python build_windows.py
      - uses: actions/upload-artifact@v2
        with:
          name: TRADABOT-Windows
          path: dist/TRADABOT.exe
```

## 📝 Checklist Finale

Avant de distribuer l'exécutable:

- [ ] Tester sur Windows 10
- [ ] Tester sur Windows 11
- [ ] Tester la connexion tradalife.com
- [ ] Tester la connexion MT4/MT5
- [ ] Tester la réception de signaux Telegram
- [ ] Tester l'exécution d'un trade
- [ ] Tester le breakeven automatique
- [ ] Vérifier les logs
- [ ] Tester la déconnexion/reconnexion
- [ ] Tester avec un compte sans accès TRADABOT

## 📞 Support Build

En cas de problème lors du build:
- **Email**: yafoy2310@gmail.com
- **Documentation PyInstaller**: https://pyinstaller.org/en/stable/

## 🎯 Prochaines Étapes

Une fois le build réussi:

1. **Upload** sur le serveur tradalife.com
2. **Créer** une page de téléchargement
3. **Documenter** pour les utilisateurs
4. **Support** utilisateur

Bonne chance! 🚀
