@echo off
chcp 65001 >nul
title TRADABOT - Installation Automatique
color 0A
mode con: cols=90 lines=35

cls
echo.
echo ════════════════════════════════════════════════════════════════════════════════════
echo                    🚀 TRADABOT - INSTALLATION AUTOMATIQUE
echo ════════════════════════════════════════════════════════════════════════════════════
echo.
echo  Ce script va installer TOUT ce qu'il faut pour faire fonctionner TRADABOT
echo.
echo ════════════════════════════════════════════════════════════════════════════════════
echo.
pause

echo.
echo [1/4] Vérification de Python...
echo.

python --version 2>nul
if %errorlevel% neq 0 (
    echo ❌ Python n'est pas installé!
    echo.
    echo 📥 Je vais ouvrir la page de téléchargement de Python...
    echo.
    echo ⚠️  IMPORTANT: Pendant l'installation de Python:
    echo     1. COCHEZ "Add Python to PATH"
    echo     2. Installez avec les paramètres par défaut
    echo     3. Redémarrez votre PC après l'installation
    echo     4. Relancez ce script
    echo.
    pause
    start https://www.python.org/downloads/
    exit /b 1
)

echo ✅ Python est installé
python --version
echo.

echo [2/4] Installation de MetaTrader5...
echo.
pip install --quiet --upgrade MetaTrader5
if %errorlevel% neq 0 (
    echo ❌ Erreur installation MetaTrader5
    echo.
    echo Essai avec pip3...
    pip3 install --quiet --upgrade MetaTrader5
)
echo ✅ MetaTrader5 installé
echo.

echo [3/4] Installation de requests...
echo.
pip install --quiet --upgrade requests
if %errorlevel% neq 0 (
    pip3 install --quiet --upgrade requests
)
echo ✅ Requests installé
echo.

echo [4/4] Création du raccourci...
echo.

REM Créer un fichier de configuration vide s'il n'existe pas
if not exist "config.json" (
    echo { > config.json
    echo   "firstRun": true >> config.json
    echo } >> config.json
)

echo ✅ Installation terminée!
echo.

echo ════════════════════════════════════════════════════════════════════════════════════
echo                              ✅ INSTALLATION TERMINÉE!
echo ════════════════════════════════════════════════════════════════════════════════════
echo.
echo 🎯 PROCHAINES ÉTAPES:
echo.
echo    1. Allez sur https://tradalife.com/tradabot-web
echo    2. Connectez-vous avec votre compte
echo    3. Configurez vos paramètres MT4/MT5
echo    4. Téléchargez votre fichier "tradabot_config.json"
echo    5. Placez le fichier dans CE dossier
echo    6. Double-cliquez sur "DEMARRER_TRADABOT.bat"
echo.
echo ════════════════════════════════════════════════════════════════════════════════════
echo.

choice /C ON /M "Voulez-vous ouvrir le site maintenant"
if errorlevel 2 goto FIN
if errorlevel 1 start https://edushop-portal.emergent.host/tradabot-web

:FIN
echo.
echo Appuyez sur une touche pour fermer...
pause >nul
