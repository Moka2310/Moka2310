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
    '--name=TRADABOT_CONNECTOR',
    '--clean',
    '--noconfirm',
])

print("✅ Compilation terminée!")

# Créer le ZIP avec tous les fichiers nécessaires
print("📦 Création du package...")
with zipfile.ZipFile('TRADABOT_CONNECTOR_BUILD.zip', 'w') as zipf:
    zipf.write('dist/TRADABOT_CONNECTOR.exe', 'TRADABOT_CONNECTOR.exe')
    zipf.write('.env.example', '.env.example')
    zipf.write('README.md', 'README.md')
    zipf.write('LANCER_TRADABOT.bat', 'LANCER_TRADABOT.bat')

print("✅ Package créé: TRADABOT_CONNECTOR_BUILD.zip")
