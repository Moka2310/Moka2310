@echo off
chcp 65001 >nul
title TRADABOT - Compilation du Connecteur
color 0B

echo.
echo ════════════════════════════════════════════════════════════
echo 🔨 TRADABOT - Compilation du Connecteur
echo ════════════════════════════════════════════════════════════
echo.
echo Ce script va créer TradabotConnector.exe automatiquement
echo Durée: 5-10 minutes
echo.
pause

echo.
echo [1/5] Vérification de Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ❌ ERREUR: Python n'est pas installé!
    echo.
    echo Installez Python depuis: https://www.python.org/downloads/
    echo N'oubliez pas de cocher "Add Python to PATH"!
    echo.
    pause
    exit /b 1
)
echo ✅ Python trouvé!

echo.
echo [2/5] Installation de PyInstaller...
pip install --quiet pyinstaller
if %errorlevel% neq 0 (
    echo ❌ Erreur installation PyInstaller
    pause
    exit /b 1
)
echo ✅ PyInstaller installé!

echo.
echo [3/5] Installation des dépendances...
pip install --quiet MetaTrader5 requests
if %errorlevel% neq 0 (
    echo ❌ Erreur installation dépendances
    pause
    exit /b 1
)
echo ✅ Dépendances installées!

echo.
echo [4/5] Compilation du connecteur...
echo (Cela peut prendre 5-10 minutes)
echo.

pyinstaller --onefile --windowed --name TradabotConnector --icon=icon.ico connector.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ Erreur lors de la compilation
    pause
    exit /b 1
)

echo.
echo [5/5] Vérification...
if exist "dist\TradabotConnector.exe" (
    echo ✅ TradabotConnector.exe créé avec succès!
) else (
    echo ❌ Le fichier n'a pas été créé
    pause
    exit /b 1
)

echo.
echo ════════════════════════════════════════════════════════════
echo ✅ COMPILATION TERMINÉE!
echo ════════════════════════════════════════════════════════════
echo.
echo 📦 Le fichier est ici: dist\TradabotConnector.exe
echo.
echo 🎯 PROCHAINES ÉTAPES:
echo 1. Testez TradabotConnector.exe sur votre PC
echo 2. Mettez-le sur votre serveur pour le téléchargement
echo 3. Vos clients pourront le télécharger depuis le site
echo.
pause
