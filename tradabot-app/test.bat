@echo off
REM ============================================
REM TRADABOT - Script de Test Rapide
REM ============================================

echo.
echo ========================================
echo   TRADABOT - Test de l'executable
echo ========================================
echo.

if not exist "dist\TRADABOT.exe" (
    echo [ERREUR] TRADABOT.exe n'existe pas
    echo Executez d'abord: build.bat
    pause
    exit /b 1
)

echo [OK] Executable trouve: dist\TRADABOT.exe
echo.
echo Taille du fichier:
dir dist\TRADABOT.exe | find "TRADABOT.exe"
echo.
echo Lancement de TRADABOT...
echo.

cd dist
start TRADABOT.exe
cd ..

echo.
echo L'application devrait s'ouvrir dans une nouvelle fenetre
echo.
echo Verifications a faire:
echo   1. Fenetre s'ouvre sans erreur
echo   2. Interface graphique visible
echo   3. Onglet Connexion accessible
echo   4. Peut se connecter avec email/password
echo.
pause
