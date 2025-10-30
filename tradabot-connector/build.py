"""
Script pour compiler TRADABOT Connector en .exe Windows
Utilise PyInstaller
"""
import PyInstaller.__main__
import os
import shutil
import zipfile

print("🔨 Compilation de TRADABOT Connector...")

# Nettoyer les anciens builds
if os.path.exists('dist'):
    shutil.rmtree('dist')
if os.path.exists('build'):
    shutil.rmtree('build')

# Configuration PyInstaller
PyInstaller.__main__.run([
    'connector.py',
    '--onefile',
    '--name=TradabotConnector',
    '--clean',
    '--noconfirm',
    '--console',  # Avec console pour voir les logs
])

print("✅ Compilation terminée!")

# Créer le ZIP avec tous les fichiers nécessaires
print("📦 Création du package...")
with zipfile.ZipFile('TRADABOT_CONNECTOR_BUILD.zip', 'w') as zipf:
    # Ajouter l'exécutable
    if os.path.exists('dist/TradabotConnector.exe'):
        zipf.write('dist/TradabotConnector.exe', 'TradabotConnector.exe')
    
    # Ajouter les scripts
    zipf.write('INSTALLER.bat', 'INSTALLER.bat')
    zipf.write('LANCER_TRADABOT.bat', 'LANCER_TRADABOT.bat')
    zipf.write('connector_launcher.py', 'connector_launcher.py')
    zipf.write('connector.py', 'connector.py')
    
    # Ajouter requirements.txt
    zipf.write('requirements.txt', 'requirements.txt')
    
    # Créer et ajouter un README
    readme_content = """
═══════════════════════════════════════════════════════════════════════════
                    🤖 TRADABOT CONNECTEUR MT4/MT5
═══════════════════════════════════════════════════════════════════════════

INSTALLATION:
1. Extrayez tous les fichiers dans un dossier
2. Double-cliquez sur "INSTALLER.bat"
3. Suivez les instructions à l'écran

CONFIGURATION:
1. Allez sur https://tradalife.com/tradabot-web
2. Configurez vos paramètres MT4/MT5
3. Téléchargez le fichier "tradabot_config.json"
4. Placez-le dans le dossier du connecteur

LANCEMENT:
1. Double-cliquez sur "LANCER_TRADABOT.bat"
2. Le connecteur se connectera automatiquement à MT4/MT5
3. Les signaux seront exécutés automatiquement

⚠️  IMPORTANT:
- Le connecteur doit rester en exécution pendant le trading
- MetaTrader 4/5 doit être installé sur votre PC
- Une connexion internet stable est requise

SUPPORT:
Pour toute question, contactez-nous sur Telegram ou par email.

═══════════════════════════════════════════════════════════════════════════
"""
    zipf.writestr('README.txt', readme_content)

print("✅ Package créé: TRADABOT_CONNECTOR_BUILD.zip")
print("")
print("📦 Contenu du package:")
print("   - TradabotConnector.exe (exécutable)")
print("   - INSTALLER.bat (installation des dépendances)")
print("   - LANCER_TRADABOT.bat (lanceur)")
print("   - connector_launcher.py (lanceur Python)")
print("   - connector.py (code source)")
print("   - requirements.txt (dépendances)")
print("   - README.txt (instructions)")
print("")
print("🎯 Le package est prêt à être distribué!")

