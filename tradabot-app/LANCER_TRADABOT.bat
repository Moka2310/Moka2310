@echo off
chcp 65001 >nul
title TRADABOT - Lanceur Simple
color 0A

echo.
echo ════════════════════════════════════════════════════════════
echo 🤖 TRADABOT - Lanceur Simple
echo ════════════════════════════════════════════════════════════
echo.
echo Installation et lancement automatique...
echo Première fois: 5-10 minutes
echo Prochaines fois: Lancement instantané!
echo.

echo [1/2] Installation des dépendances...
pip install --quiet --upgrade pip 2>nul
pip install --quiet PyQt6 requests loguru passlib cryptography 2>nul

if %errorlevel% neq 0 (
    echo.
    echo ⚠️  Installation des dépendances en cours...
    pip install PyQt6 requests loguru passlib cryptography
)

echo ✅ Dépendances installées!

echo.
echo [2/2] Lancement de TRADABOT...
echo.

python app.py

if %errorlevel% neq 0 (
    echo.
    echo ════════════════════════════════════════════════════════════
    echo ❌ ERREUR
    echo ════════════════════════════════════════════════════════════
    echo.
    echo Une erreur s'est produite.
    echo Vérifiez que Python est bien installé: python --version
    echo.
    pause
    exit /b 1
)
