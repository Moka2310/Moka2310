@echo off
REM ============================================
REM TRADABOT - Script d'Installation Windows
REM ============================================

echo.
echo ========================================
echo   TRADABOT - Installation Windows
echo ========================================
echo.

REM Vérifier Python
echo [1/5] Verification de Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe ou pas dans le PATH
    echo.
    echo Telechargez Python 3.11+ depuis: https://www.python.org/downloads/
    echo N'oubliez pas de cocher "Add Python to PATH" lors de l'installation
    pause
    exit /b 1
)
echo [OK] Python est installe

REM Vérifier pip
echo [2/5] Verification de pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] pip n'est pas installe
    pause
    exit /b 1
)
echo [OK] pip est installe

REM Créer environnement virtuel (optionnel mais recommandé)
echo [3/5] Creation de l'environnement virtuel...
if not exist "venv" (
    python -m venv venv
    echo [OK] Environnement virtuel cree
) else (
    echo [OK] Environnement virtuel existe deja
)

REM Activer l'environnement virtuel
call venv\Scripts\activate.bat

REM Installer les dépendances
echo [4/5] Installation des dependances...
echo Cela peut prendre 2-5 minutes...
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERREUR] Echec de l'installation des dependances
    pause
    exit /b 1
)
echo [OK] Dependances installees

REM Installer PyInstaller
echo [5/5] Installation de PyInstaller...
pip install pyinstaller
if errorlevel 1 (
    echo [ERREUR] Echec de l'installation de PyInstaller
    pause
    exit /b 1
)
echo [OK] PyInstaller installe

echo.
echo ========================================
echo   Installation terminee avec succes!
echo ========================================
echo.
echo Prochaines etapes:
echo   1. Executer: build.bat
echo   2. L'executable sera dans: dist\TRADABOT.exe
echo.
pause
