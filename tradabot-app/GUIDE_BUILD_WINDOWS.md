# 🔨 GUIDE COMPLET - BUILD TRADABOT WINDOWS

## 📋 Table des Matières
1. [Prérequis](#prérequis)
2. [Installation](#installation)
3. [Build de l'exécutable](#build-de-lexécutable)
4. [Distribution](#distribution)
5. [Dépannage](#dépannage)

---

## 🎯 Prérequis

### Système d'exploitation
- **Windows 10** ou **Windows 11** (64-bit)
- **Minimum 4 GB RAM**
- **500 MB d'espace disque libre**

### Logiciels nécessaires

#### 1. Python 3.11+
Télécharger depuis: https://www.python.org/downloads/

**Installation:**
1. Télécharger Python 3.11 ou supérieur
2. ✅ **IMPORTANT**: Cocher "Add Python to PATH" durant l'installation
3. Installer en mode admin

**Vérification:**
```cmd
python --version
```
Devrait afficher: `Python 3.11.x` ou supérieur

#### 2. MetaTrader 5 (pour le développement/test)
Télécharger depuis: https://www.metatrader5.com/

**Note**: L'utilisateur final aura besoin de MT4 ou MT5 installé.

---

## 📦 Installation

### Étape 1: Ouvrir PowerShell ou CMD en mode Administrateur

**PowerShell:**
- Clic droit sur le menu Démarrer
- Sélectionner "Windows PowerShell (Admin)"

**CMD:**
- Chercher "cmd" dans le menu Démarrer
- Clic droit → "Exécuter en tant qu'administrateur"

### Étape 2: Naviguer vers le dossier tradabot-app

```cmd
cd C:\chemin\vers\app\tradabot-app
```

Remplacer `C:\chemin\vers\app` par le chemin réel.

### Étape 3: Créer un environnement virtuel (optionnel mais recommandé)

```cmd
python -m venv venv
venv\Scripts\activate
```

Vous devriez voir `(venv)` au début de votre ligne de commande.

### Étape 4: Installer les dépendances

```cmd
pip install --upgrade pip
pip install -r requirements.txt
```

**Temps estimé:** 5-10 minutes (selon votre connexion internet)

**⚠️ Si erreur avec PyQt6:**
```cmd
pip install --upgrade pip setuptools wheel
pip install PyQt6 --no-cache-dir
pip install -r requirements.txt
```

---

## 🔨 Build de l'exécutable

### Méthode 1: Script automatique (RECOMMANDÉ)

```cmd
python build_windows.py
```

Le script va:
1. 🧹 Nettoyer les anciens builds
2. 🔨 Compiler l'application
3. 📦 Créer l'exécutable dans `/dist/TRADABOT.exe`

**Temps estimé:** 5-15 minutes

**Sortie attendue:**
```
============================================================
🔨 BUILD TRADABOT - Application Desktop Windows
============================================================

🧹 Nettoyage des anciens builds...
✅ Nettoyage terminé

🔨 Lancement de PyInstaller...
[... processus de compilation ...]

============================================================
✅ BUILD RÉUSSI!
============================================================

📦 Exécutable créé: dist/TRADABOT.exe
💾 Taille: XX.X MB
```

### Méthode 2: Script batch (3 clics)

Voir `BUILD_3_CLICS.md` pour une méthode ultra-simplifiée.

### Méthode 3: Commande manuelle PyInstaller

```cmd
pyinstaller app.py ^
  --name=TRADABOT ^
  --onefile ^
  --windowed ^
  --clean ^
  --add-data="config.py;." ^
  --add-data="broker_servers.py;." ^
  --hidden-import=telegram ^
  --hidden-import=PyQt6 ^
  --collect-all=telegram ^
  --collect-all=PyQt6 ^
  --optimize=2 ^
  --strip ^
  --uac-admin
```

---

## 📤 Distribution

### Fichier à distribuer

**Emplacement:** `/tradabot-app/dist/TRADABOT.exe`

**Taille:** Entre 80 MB et 150 MB (selon les optimisations)

### Créer un package complet

1. **Créer un dossier de distribution:**
   ```
   TRADABOT_v1.0/
   ├── TRADABOT.exe
   ├── README.txt (instructions utilisateur)
   └── LICENCE.txt (optionnel)
   ```

2. **Compresser en ZIP:**
   - Clic droit sur le dossier
   - "Envoyer vers" → "Dossier compressé (ZIP)"

3. **Nom suggéré:**
   `TRADABOT_v1.0_Windows.zip`

### Instructions pour l'utilisateur final

Créer un fichier `README.txt`:

```
═══════════════════════════════════════════════════════════
🤖 TRADABOT - Bot de Trading Automatique
═══════════════════════════════════════════════════════════

VERSION: 1.0
DATE: Octobre 2025

📋 PRÉREQUIS
─────────────
✅ Windows 10/11 (64-bit)
✅ MetaTrader 4 OU MetaTrader 5 installé
✅ Compte de trading (Démo ou Réel)
✅ Compte tradalife.com avec accès TRADABOT

📦 INSTALLATION
─────────────
1. Extraire TRADABOT.exe dans un dossier de votre choix
2. Double-cliquer sur TRADABOT.exe
3. Accepter les droits administrateur si demandé

🚀 PREMIÈRE UTILISATION
─────────────
1. Lancer TRADABOT.exe
2. Onglet "Connexion"
   - Email: votre@email.com (compte tradalife)
   - Mot de passe: votre mot de passe
3. Cliquer "Se connecter"
4. Onglet "Configuration"
   - Remplir Login MT4/MT5
   - Remplir Mot de passe MT4/MT5
   - Sélectionner votre Serveur (ex: XM.COM-Real)
   - Cliquer "Connecter MT4"
5. Activer les canaux Telegram souhaités
6. Définir les lots pour chaque catégorie
7. Cliquer "Sauvegarder Configuration"
8. Cliquer "DÉMARRER LE BOT" ▶️

✅ Le bot surveille maintenant les signaux Telegram!

🎯 COMMENT TROUVER VOS INFOS MT4
─────────────
1. Ouvrir MetaTrader 4 ou 5
2. Menu → Outils → Options
3. Onglet "Serveur"
4. Noter:
   - Login (numéro)
   - Serveur (nom exact)

📞 SUPPORT
─────────────
Email: support@tradalife.com
Site: https://www.tradalife.com

═══════════════════════════════════════════════════════════
```

---

## 🔧 Dépannage

### Problème 1: "Python n'est pas reconnu"

**Cause:** Python n'est pas dans le PATH

**Solution:**
1. Réinstaller Python
2. ✅ Cocher "Add Python to PATH"
3. OU ajouter manuellement au PATH

### Problème 2: "PyInstaller n'est pas reconnu"

**Cause:** PyInstaller pas installé ou venv pas activé

**Solution:**
```cmd
pip install pyinstaller
```

### Problème 3: Erreur durant le build

**Message:** `ModuleNotFoundError: No module named 'XXX'`

**Solution:**
```cmd
pip install XXX
# OU
pip install -r requirements.txt --force-reinstall
```

### Problème 4: .exe ne se lance pas

**Causes possibles:**
- Antivirus bloque l'exécution
- Fichier corrompu
- Dépendances manquantes

**Solutions:**
1. **Antivirus:**
   - Ajouter TRADABOT.exe aux exceptions
   - Temporairement désactiver l'antivirus

2. **Rebuild:**
   ```cmd
   python build_windows.py
   ```

3. **Test en mode console:**
   Modifier `build_windows.py`:
   ```python
   # Changer
   "--windowed",  # Pas de console
   # En
   # "--windowed",  # Activer la console pour debug
   ```

### Problème 5: .exe trop volumineux (>200 MB)

**Solution - Optimisation:**

Modifier `build_windows.py`:
```python
# Ajouter ces options
"--exclude-module=matplotlib",
"--exclude-module=numpy",
"--exclude-module=pandas",
"--exclude-module=scipy",
```

Rebuild:
```cmd
python build_windows.py
```

### Problème 6: MetaTrader5 module error

**Message:** `ImportError: DLL load failed`

**Solution:**
```cmd
pip uninstall MetaTrader5
pip install MetaTrader5 --no-cache-dir
```

### Problème 7: Erreur PyQt6

**Message:** `ModuleNotFoundError: No module named 'PyQt6.sip'`

**Solution:**
```cmd
pip install PyQt6-sip
pip install PyQt6 --force-reinstall
```

---

## 📊 Checklist Avant Distribution

Avant de distribuer l'exécutable:

- [ ] ✅ Build réussi sans erreurs
- [ ] ✅ .exe créé dans `/dist/`
- [ ] ✅ Taille du fichier raisonnable (<150 MB)
- [ ] ✅ Test de lancement sur Windows propre
- [ ] ✅ Connexion API fonctionne
- [ ] ✅ Interface s'affiche correctement
- [ ] ✅ README.txt créé
- [ ] ✅ Package ZIP créé
- [ ] ✅ Nom de fichier clair (TRADABOT_v1.0_Windows.zip)

---

## 📝 Notes Importantes

### Signature de code (optionnel)

Pour éviter les avertissements Windows "Éditeur inconnu":
- Acheter un certificat de signature de code
- Signer l'exécutable avec `signtool.exe`

**Coût:** ~200-500$ par an

### Antivirus

Les antivirus peuvent signaler les .exe PyInstaller comme suspects (faux positifs).

**Solutions:**
1. Soumettre à VirusTotal pour analyse
2. Contacter les éditeurs d'antivirus
3. Signer le code (voir ci-dessus)

### Mises à jour

Pour publier une mise à jour:
1. Modifier le code
2. Changer `APP_VERSION` dans `config.py`
3. Rebuild avec `build_windows.py`
4. Distribuer le nouveau .exe

---

## 🎉 Félicitations!

Vous avez maintenant:
✅ Compilé TRADABOT en exécutable Windows
✅ Package prêt à distribuer
✅ Documentation utilisateur

**Prochaine étape:** Tests complets sur environnement Windows réel!

---

**Version du guide:** 1.0  
**Date:** Octobre 2025  
**Contact:** support@tradalife.com
