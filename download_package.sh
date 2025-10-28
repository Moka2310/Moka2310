#!/bin/bash

# ============================================
# TRADABOT - Script de Téléchargement Package
# ============================================

echo ""
echo "========================================"
echo "   TRADABOT - Téléchargement Package"
echo "========================================"
echo ""

PACKAGE_PATH="/app/TRADABOT_Package.zip"

# Vérifier que le package existe
if [ ! -f "$PACKAGE_PATH" ]; then
    echo "❌ ERREUR: Package non trouvé: $PACKAGE_PATH"
    echo ""
    echo "Création du package..."
    cd /app
    zip -r TRADABOT_Package.zip tradabot-app/ -x "*.pyc" "*__pycache__*" "*.log"
    echo "✅ Package créé"
fi

# Afficher les infos
echo "📦 Package: $PACKAGE_PATH"
echo "📏 Taille: $(ls -lh $PACKAGE_PATH | awk '{print $5}')"
echo ""

echo "Options de téléchargement:"
echo ""
echo "1️⃣  Via navigateur:"
echo "    Ouvrir: https://mt4-dropdown.preview.emergentagent.com"
echo "    Télécharger: /app/TRADABOT_Package.zip"
echo ""
echo "2️⃣  Via SCP (depuis votre PC Windows avec WSL):"
echo "    scp root@autotrader-hub-12:/app/TRADABOT_Package.zip C:/TRADABOT/"
echo ""
echo "3️⃣  Via wget (depuis Windows WSL):"
echo "    wget https://mt4-dropdown.preview.emergentagent.com/TRADABOT_Package.zip"
echo ""
echo "4️⃣  Via curl:"
echo "    curl -O https://mt4-dropdown.preview.emergentagent.com/TRADABOT_Package.zip"
echo ""

echo "📖 Documentation complète: /app/TRADABOT_PACKAGE_README.md"
echo ""
echo "Une fois sur Windows:"
echo "  1. Extraire le ZIP"
echo "  2. Double-cliquer: install.bat"
echo "  3. Double-cliquer: build.bat"
echo "  4. Récupérer: dist/TRADABOT.exe"
echo ""
echo "========================================"
