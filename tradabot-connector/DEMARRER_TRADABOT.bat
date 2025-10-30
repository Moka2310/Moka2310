@echo off
chcp 65001 >nul
title TRADABOT - Démarrage
color 0B
mode con: cols=90 lines=40

:DEBUT
cls
echo.
echo ════════════════════════════════════════════════════════════════════════════════════
echo                         🤖 TRADABOT CONNECTEUR MT4/MT5
echo ════════════════════════════════════════════════════════════════════════════════════
echo.

REM Vérifier Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python n'est pas installé!
    echo.
    echo Veuillez d'abord lancer: INSTALLATION_SIMPLE.bat
    echo.
    pause
    exit /b 1
)

REM Vérifier MetaTrader5
python -c "import MetaTrader5" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ MetaTrader5 n'est pas installé!
    echo.
    echo Veuillez d'abord lancer: INSTALLATION_SIMPLE.bat
    echo.
    pause
    exit /b 1
)

REM Vérifier le fichier de config
if not exist "tradabot_config.json" (
    echo ⚠️  Configuration manquante!
    echo.
    echo Vous devez télécharger votre fichier de configuration depuis le site:
    echo.
    echo    1. Allez sur https://tradalife.com/tradabot-web
    echo    2. Configurez vos paramètres
    echo    3. Cliquez sur "Télécharger tradabot_config.json"
    echo    4. Placez le fichier dans ce dossier
    echo.
    
    choice /C ON /M "Voulez-vous ouvrir le site maintenant"
    if errorlevel 1 (
        if errorlevel 2 goto FIN
        start https://edushop-portal.emergent.host/tradabot-web
        echo.
        echo Après avoir téléchargé le fichier, relancez ce programme.
        timeout /t 3
        goto FIN
    )
)

echo ✅ Python OK
echo ✅ MetaTrader5 OK
echo ✅ Configuration OK
echo.
echo ════════════════════════════════════════════════════════════════════════════════════
echo                              🚀 DÉMARRAGE DU BOT
echo ════════════════════════════════════════════════════════════════════════════════════
echo.
echo ⚠️  IMPORTANT:
echo    - MetaTrader 4/5 doit être OUVERT
echo    - Ne fermez PAS cette fenêtre pendant le trading
echo    - Pour arrêter: fermez cette fenêtre ou Ctrl+C
echo.
echo ════════════════════════════════════════════════════════════════════════════════════
echo.
timeout /t 2 >nul

REM Lancer le bot
python tradabot_simple.py

:FIN
echo.
echo ════════════════════════════════════════════════════════════════════════════════════
echo                                   👋 AU REVOIR
echo ════════════════════════════════════════════════════════════════════════════════════
echo.
timeout /t 3
