"""
Script de build pour créer l'exécutable Windows de TRADABOT
Utilise PyInstaller pour packager l'application
"""
import PyInstaller.__main__
import os
import shutil
from pathlib import Path

# Chemins
SCRIPT_DIR = Path(__file__).parent
APP_NAME = "TRADABOT"
MAIN_SCRIPT = str(SCRIPT_DIR / "app.py")
DIST_DIR = str(SCRIPT_DIR / "dist")
BUILD_DIR = str(SCRIPT_DIR / "build")
ICON_PATH = str(SCRIPT_DIR / "icon.ico") if (SCRIPT_DIR / "icon.ico").exists() else None

print("=" * 60)
print(f"🔨 BUILD TRADABOT - Application Desktop Windows")
print("=" * 60)
print()

# Nettoyer les anciens builds
print("🧹 Nettoyage des anciens builds...")
if os.path.exists(DIST_DIR):
    shutil.rmtree(DIST_DIR)
if os.path.exists(BUILD_DIR):
    shutil.rmtree(BUILD_DIR)
if os.path.exists(SCRIPT_DIR / f"{APP_NAME}.spec"):
    os.remove(SCRIPT_DIR / f"{APP_NAME}.spec")

print("✅ Nettoyage terminé\n")

# Arguments PyInstaller
pyinstaller_args = [
    MAIN_SCRIPT,
    f"--name={APP_NAME}",
    "--onefile",  # Un seul fichier .exe
    "--windowed",  # Pas de console (interface graphique)
    "--clean",
    f"--distpath={DIST_DIR}",
    f"--buildpath={BUILD_DIR}",
    
    # Ajouter les fichiers de configuration
    "--add-data=config.py;.",
    "--add-data=broker_servers.py;.",
    
    # Hidden imports pour éviter les erreurs
    "--hidden-import=telegram",
    "--hidden-import=telegram.ext",
    "--hidden-import=PyQt6",
    "--hidden-import=PyQt6.QtWidgets",
    "--hidden-import=PyQt6.QtCore",
    "--hidden-import=PyQt6.QtGui",
    "--hidden-import=loguru",
    "--hidden-import=requests",
    "--hidden-import=passlib",
    "--hidden-import=motor",
    "--hidden-import=motor.motor_asyncio",
    
    # Collecter tous les packages
    "--collect-all=telegram",
    "--collect-all=PyQt6",
    
    # Optimisations
    "--optimize=2",
    "--strip",  # Réduire la taille
    
    # Nom du fichier
    "--uac-admin",  # Demander droits admin si nécessaire
]

# Ajouter l'icône si elle existe
if ICON_PATH and os.path.exists(ICON_PATH):
    pyinstaller_args.append(f"--icon={ICON_PATH}")
    print(f"🎨 Icône trouvée: {ICON_PATH}\n")
else:
    print("⚠️  Pas d'icône trouvée (icon.ico)\n")

print("🔨 Lancement de PyInstaller...")
print()

try:
    # Lancer PyInstaller
    PyInstaller.__main__.run(pyinstaller_args)
    
    print()
    print("=" * 60)
    print("✅ BUILD RÉUSSI!")
    print("=" * 60)
    print()
    print(f"📦 Exécutable créé: {DIST_DIR}/{APP_NAME}.exe")
    print()
    
    # Afficher la taille du fichier
    exe_path = Path(DIST_DIR) / f"{APP_NAME}.exe"
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"💾 Taille: {size_mb:.1f} MB")
    
    print()
    print("📋 PROCHAINES ÉTAPES:")
    print("  1. Testez l'exécutable sur Windows")
    print("  2. Installez MetaTrader 4 ou 5 si pas déjà fait")
    print("  3. Lancez TRADABOT.exe")
    print("  4. Connectez-vous avec votre compte tradalife.com")
    print("  5. Configurez votre compte MT4/MT5")
    print("  6. Démarrez le bot!")
    print()
    
except Exception as e:
    print()
    print("=" * 60)
    print("❌ ERREUR LORS DU BUILD")
    print("=" * 60)
    print()
    print(f"Erreur: {e}")
    print()
    print("Vérifiez que toutes les dépendances sont installées:")
    print("  pip install -r requirements.txt")
    print()
    raise

print("=" * 60)
