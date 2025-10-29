@echo off
chcp 65001 >nul
title TRADABOT - Installation Automatique
color 0A

echo.
echo ════════════════════════════════════════════════════════════
echo 🤖 TRADABOT - Installation Automatique
echo ════════════════════════════════════════════════════════════
echo.
echo Ce script va installer TRADABOT automatiquement.
echo Durée estimée: 15-20 minutes
echo.
pause

echo.
echo [1/5] Vérification de Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ❌ ERREUR: Python n'est pas installé!
    echo.
    echo SOLUTION:
    echo 1. Téléchargez Python ici: https://www.python.org/downloads/
    echo 2. Installez-le en COCHANT "Add Python to PATH"
    echo 3. Redémarrez ce script
    echo.
    pause
    exit /b 1
)
echo ✅ Python est installé!

echo.
echo [2/5] Vérification de pip...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip n'est pas disponible
    pause
    exit /b 1
)
echo ✅ pip est disponible!

echo.
echo [3/5] Installation des dépendances...
echo (Cela peut prendre 5-10 minutes)
echo.
pip install --upgrade pip
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo ❌ Erreur lors de l'installation des dépendances
    echo.
    pause
    exit /b 1
)
echo ✅ Dépendances installées!

echo.
echo [4/5] Construction de l'application TRADABOT...
echo (Cela peut prendre 10-15 minutes)
echo.
python build_windows.py
if %errorlevel% neq 0 (
    echo.
    echo ❌ Erreur lors de la construction
    echo.
    pause
    exit /b 1
)

echo.
echo [5/5] Vérification du fichier créé...
if exist "dist\TRADABOT.exe" (
    echo ✅ TRADABOT.exe créé avec succès!
) else (
    echo ❌ Le fichier TRADABOT.exe n'a pas été créé
    pause
    exit /b 1
)

echo.
echo ════════════════════════════════════════════════════════════
echo ✅ INSTALLATION TERMINÉE!
echo ════════════════════════════════════════════════════════════
echo.
echo 📦 L'application est ici: dist\TRADABOT.exe
echo.
echo 🚀 PROCHAINES ÉTAPES:
echo 1. Allez dans le dossier "dist"
echo 2. Double-cliquez sur TRADABOT.exe
echo 3. Connectez-vous avec votre compte tradalife.com
echo 4. Configurez votre compte MT4/MT5
echo 5. Démarrez le bot!
echo.
echo Voulez-vous lancer TRADABOT maintenant? (O/N)
set /p launch="Votre choix: "

if /i "%launch%"=="O" (
    echo.
    echo 🚀 Lancement de TRADABOT...
    start "" "dist\TRADABOT.exe"
    echo.
    echo ✅ TRADABOT lancé!
    timeout /t 3 >nul
    exit
)

echo.
echo Appuyez sur une touche pour fermer...
pause >nul
