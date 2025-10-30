@echo off
chcp 65001 >nul
title TRADABOT - Connecteur
color 0B

:START
cls
echo.
echo ════════════════════════════════════════════════════════════════════════════
echo                    🤖 TRADABOT CONNECTEUR MT4/MT5
echo ════════════════════════════════════════════════════════════════════════════
echo.
echo  Ce connecteur permet d'exécuter automatiquement les signaux TRADABOT
echo  sur votre plateforme MetaTrader 4 ou MetaTrader 5.
echo.
echo ════════════════════════════════════════════════════════════════════════════
echo.

REM Vérifier si le fichier de config existe
if not exist "tradabot_config.json" (
    echo ⚠️  CONFIGURATION MANQUANTE
    echo.
    echo Vous devez d'abord configurer le connecteur depuis le site web:
    echo.
    echo    1. Allez sur: https://edushop-portal.emergent.host/tradabot-web
    echo    2. Connectez-vous avec votre compte
    echo    3. Configurez vos paramètres MT4/MT5
    echo    4. Téléchargez le fichier de configuration
    echo    5. Placez le fichier "tradabot_config.json" dans ce dossier
    echo.
    echo ════════════════════════════════════════════════════════════════════════════
    echo.
    
    choice /C OA /M "O = Ouvrir le site, A = Annuler"
    if errorlevel 2 goto END
    if errorlevel 1 (
        start https://edushop-portal.emergent.host/tradabot-web
        echo.
        echo ℹ️  Après avoir téléchargé et placé le fichier, relancez ce programme.
        echo.
        timeout /t 5
        goto END
    )
)

REM Vérifier si MetaTrader5 est installé
python -c "import MetaTrader5" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Dépendances manquantes!
    echo.
    echo Veuillez d'abord exécuter INSTALLER.bat
    echo.
    pause
    goto END
)

echo ✅ Configuration trouvée
echo ✅ Dépendances OK
echo.
echo ════════════════════════════════════════════════════════════════════════════
echo                          🚀 DÉMARRAGE DU CONNECTEUR
echo ════════════════════════════════════════════════════════════════════════════
echo.
echo Le connecteur va maintenant se connecter à MT4/MT5 et attendre les signaux...
echo.
echo ⚠️  NE FERMEZ PAS CETTE FENÊTRE pendant le trading
echo    Le connecteur doit rester actif pour exécuter les signaux
echo.
echo Pour arrêter le connecteur, appuyez sur CTRL+C
echo.
echo ════════════════════════════════════════════════════════════════════════════
echo.
timeout /t 3

REM Lancer le connecteur
python connector_launcher.py

:END
echo.
echo ════════════════════════════════════════════════════════════════════════════
echo                          👋 À BIENTÔT!
echo ════════════════════════════════════════════════════════════════════════════
echo.
pause
