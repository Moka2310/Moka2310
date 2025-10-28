# Build script pour créer l'exécutable Windows
# À exécuter sur une machine Windows

"""
TRADABOT - Script de Build Windows
Crée un exécutable .exe standalone

Instructions:
1. Installer Python 3.11+ sur Windows
2. Installer les dépendances: pip install -r requirements.txt
3. Installer PyInstaller: pip install pyinstaller
4. Exécuter ce script: python build_windows.py
5. L'exécutable sera dans le dossier 'dist'
"""

import PyInstaller.__main__
import os
from pathlib import Path

# Configuration
APP_NAME = "TRADABOT"
MAIN_SCRIPT = "app.py"
ICON_FILE = "icon.ico"  # Si vous avez un icône

# Construire la commande PyInstaller
pyinstaller_args = [
    MAIN_SCRIPT,
    f'--name={APP_NAME}',
    '--onefile',  # Un seul fichier .exe
    '--windowed',  # Pas de console
    '--clean',
    
    # Inclure les dépendances
    '--hidden-import=PyQt6',
    '--hidden-import=telegram',
    '--hidden-import=MetaTrader5',
    '--hidden-import=loguru',
    '--hidden-import=cryptography',
    '--hidden-import=requests',
    
    # Inclure les fichiers de données
    '--add-data=config.py;.',
    '--add-data=auth_manager.py;.',
    '--add-data=telegram_monitor.py;.',
    '--add-data=mt4_manager.py;.',
    '--add-data=signal_parser.py;.',
    
    # Optimisations
    '--optimize=2',
]

# Ajouter l'icône si disponible
if os.path.exists(ICON_FILE):
    pyinstaller_args.append(f'--icon={ICON_FILE}')

# Exécuter PyInstaller
print("🔨 Construction de l'exécutable Windows...")
print(f"📦 Application: {APP_NAME}")
print("⏳ Cela peut prendre quelques minutes...\n")

PyInstaller.__main__.run(pyinstaller_args)

print("\n✅ Build terminé!")
print(f"📂 Exécutable disponible dans: dist/{APP_NAME}.exe")
print("\n📝 Instructions de distribution:")
print("   1. Copiez le fichier .exe")
print("   2. L'utilisateur doit avoir MetaTrader 4/5 installé")
print("   3. Premier lancement: connexion avec email/password tradalife.com")
