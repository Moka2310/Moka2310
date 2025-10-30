@echo off
chcp 65001 >nul
title TRADABOT - Installation
color 0E
mode con: cols=80 lines=30

echo.
echo ════════════════════════════════════════════════════════════════════════════
echo                    🎯 TRADABOT CONNECTEUR - INSTALLATION
echo ════════════════════════════════════════════════════════════════════════════
echo.
echo  Bienvenue dans l'installateur du Connecteur TRADABOT!
echo  Ce connecteur permet d'exécuter automatiquement les signaux sur MT4/MT5.
echo.
echo ════════════════════════════════════════════════════════════════════════════
echo.
pause

echo.
echo [ÉTAPE 1/3] Vérification de l'installation...
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python n'est pas installé sur votre système.
    echo.
    echo 📥 Voulez-vous ouvrir la page de téléchargement de Python?
    echo.
    choice /C ON /M "O = Oui, N = Non"
    if errorlevel 2 goto NOPYTHON
    if errorlevel 1 (
        start https://www.python.org/downloads/
        echo.
        echo ⏸️  Après avoir installé Python, relancez cet installateur.
        echo    ⚠️  IMPORTANT: Cochez "Add Python to PATH" pendant l'installation!
        echo.
        pause
        exit /b 1
    )
    :NOPYTHON
    echo.
    echo ℹ️  Installation annulée.
    pause
    exit /b 1
)

echo ✅ Python est installé
echo.

echo [ÉTAPE 2/3] Installation des dépendances...
echo.
echo ⏳ Installation de MetaTrader5...
pip install --quiet MetaTrader5
if %errorlevel% neq 0 (
    echo ❌ Erreur lors de l'installation de MetaTrader5
    echo.
    pause
    exit /b 1
)

echo ⏳ Installation de requests...
pip install --quiet requests
if %errorlevel% neq 0 (
    echo ❌ Erreur lors de l'installation de requests
    echo.
    pause
    exit /b 1
)

echo ✅ Dépendances installées avec succès!
echo.

echo [ÉTAPE 3/3] Configuration...
echo.

REM Créer le dossier de configuration s'il n'existe pas
if not exist "%USERPROFILE%\.tradabot" mkdir "%USERPROFILE%\.tradabot"

REM Créer un fichier .env.example s'il n'existe pas
if not exist ".env" (
    echo # Configuration TRADABOT Connecteur > .env
    echo # >> .env
    echo # IMPORTANT: Configurez ces valeurs depuis l'interface web >> .env
    echo # Ne modifiez pas ce fichier manuellement >> .env
    echo. >> .env
    echo AUTH_TOKEN= >> .env
    echo BACKEND_URL=https://edushop-portal.emergent.host >> .env
)

echo ✅ Configuration créée
echo.

echo ════════════════════════════════════════════════════════════════════════════
echo                        ✅ INSTALLATION TERMINÉE!
echo ════════════════════════════════════════════════════════════════════════════
echo.
echo 🎯 PROCHAINES ÉTAPES:
echo.
echo    1. Connectez-vous sur https://tradalife.com/tradabot-web
echo    2. Configurez vos paramètres MT4/MT5 et canaux
echo    3. Téléchargez votre fichier de configuration personnalisé
echo    4. Placez le fichier dans ce dossier
echo    5. Double-cliquez sur "LANCER_TRADABOT.bat"
echo.
echo ⚠️  IMPORTANT: Le connecteur doit rester en exécution pendant le trading
echo.
echo ════════════════════════════════════════════════════════════════════════════
echo.
pause

REM Demander si l'utilisateur veut ouvrir le site
echo.
echo 🌐 Voulez-vous ouvrir le site de configuration maintenant?
echo.
choice /C ON /M "O = Oui, N = Non"
if errorlevel 1 (
    start https://edushop-portal.emergent.host/tradabot-web
)

echo.
echo Merci d'utiliser TRADABOT! 🚀
echo.
timeout /t 3 >nul
