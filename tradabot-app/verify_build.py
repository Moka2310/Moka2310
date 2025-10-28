"""
Script de vérification pré-build
Vérifie que tous les fichiers nécessaires sont présents
"""
import os
import sys
from pathlib import Path

def check_file(file_path, description):
    """Vérifie qu'un fichier existe"""
    if os.path.exists(file_path):
        size = os.path.getsize(file_path)
        print(f"✅ {description}: {size/1024:.1f} KB")
        return True
    else:
        print(f"❌ {description}: MANQUANT!")
        return False

def check_module(module_name):
    """Vérifie qu'un module Python est installé"""
    try:
        __import__(module_name)
        print(f"✅ Module {module_name}: Installé")
        return True
    except ImportError:
        print(f"❌ Module {module_name}: MANQUANT!")
        return False

print("="*60)
print("🔍 VÉRIFICATION PRÉ-BUILD TRADABOT")
print("="*60)
print()

all_ok = True

# Vérifier Python
print("📌 Version Python:")
print(f"   Python {sys.version}")
print()

# Vérifier les fichiers source
print("📌 Fichiers source:")
files_to_check = [
    ("app.py", "Application principale"),
    ("auth_manager.py", "Gestionnaire auth"),
    ("telegram_monitor.py", "Monitor Telegram"),
    ("signal_parser.py", "Parser signaux"),
    ("mt4_manager.py", "Gestionnaire MT4"),
    ("broker_servers.py", "Liste serveurs brokers"),
    ("config.py", "Configuration"),
    ("requirements.txt", "Dépendances"),
    ("build_windows.py", "Script de build"),
]

for file_name, description in files_to_check:
    if not check_file(file_name, description):
        all_ok = False

print()

# Vérifier les modules Python
print("📌 Modules Python requis:")
modules_to_check = [
    "PyQt6",
    "telegram",
    "requests",
    "loguru",
    "cryptography",
    "PyInstaller"
]

for module in modules_to_check:
    if not check_module(module):
        all_ok = False

print()

# Vérifier MetaTrader5 (optionnel sur Linux)
if sys.platform == "win32":
    print("📌 Module MetaTrader5 (Windows seulement):")
    check_module("MetaTrader5")
    print()
else:
    print("⚠️  Système non-Windows détecté")
    print("   MetaTrader5 sera vérifié lors du build sur Windows")
    print()

# Résumé
print("="*60)
if all_ok:
    print("✅ TOUTES LES VÉRIFICATIONS RÉUSSIES!")
    print()
    print("🚀 Prêt pour le build!")
    print()
    print("Prochaines étapes:")
    print("  1. Transférer sur Windows (si pas déjà fait)")
    print("  2. Exécuter: python build_windows.py")
    print("  3. Tester: dist/TRADABOT.exe")
else:
    print("❌ CERTAINES VÉRIFICATIONS ONT ÉCHOUÉ")
    print()
    print("Actions à faire:")
    print("  1. Installer les modules manquants:")
    print("     pip install -r requirements.txt")
    print("  2. Vérifier les fichiers manquants")
    print("  3. Relancer cette vérification")
print("="*60)

# Code de sortie
sys.exit(0 if all_ok else 1)
