@echo off
REM ============================================
REM TRADABOT - Script de Build Windows
REM ============================================

echo.
echo ========================================
echo   TRADABOT - Build de l'executable
echo ========================================
echo.

REM Activer l'environnement virtuel si il existe
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo [OK] Environnement virtuel active
)

REM Vérifier que PyInstaller est installé
echo [1/3] Verification de PyInstaller...
pyinstaller --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] PyInstaller n'est pas installe
    echo Executez d'abord: install.bat
    pause
    exit /b 1
)
echo [OK] PyInstaller est installe

REM Nettoyer les builds précédents
echo [2/3] Nettoyage des builds precedents...
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist
if exist "*.spec" del /q *.spec
echo [OK] Nettoyage termine

REM Lancer le build
echo [3/3] Build en cours...
echo Cela peut prendre 5-10 minutes...
echo.

python build_windows.py

if errorlevel 1 (
    echo.
    echo [ERREUR] Le build a echoue
    echo Verifiez les erreurs ci-dessus
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Build termine avec succes!
echo ========================================
echo.
echo L'executable se trouve dans: dist\TRADABOT.exe
echo Taille attendue: 50-80 MB
echo.
echo Prochaines etapes:
echo   1. Tester: dist\TRADABOT.exe
echo   2. Distribuer aux utilisateurs
echo.

REM Afficher la taille du fichier
if exist "dist\TRADABOT.exe" (
    echo Taille du fichier:
    dir dist\TRADABOT.exe | find "TRADABOT.exe"
    echo.
)

pause
