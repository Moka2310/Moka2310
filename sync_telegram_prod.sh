#!/bin/bash
echo "=========================================="
echo "🔄 SYNCHRONISATION TELEGRAM PRODUCTION"
echo "=========================================="
echo ""
echo "Synchronisation du nombre de membres..."
echo ""

curl -X POST https://tradalife.com/api/telegram/sync-members

echo ""
echo ""
echo "=========================================="
echo "✅ Terminé !"
echo "=========================================="
