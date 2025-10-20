#!/bin/bash
echo "=========================================="
echo "🌍 MISE À JOUR DES TRADUCTIONS"
echo "=========================================="
echo ""
echo "Ajout des traductions anglaises aux témoignages..."
echo ""

curl -X POST https://tradalife.com/api/admin/update-testimonial-translations \
  -H "Content-Type: application/json" \
  -d '{"secret_key": "tradalife-admin-promote-2025"}'

echo ""
echo ""
echo "=========================================="
echo "✅ Terminé !"
echo "=========================================="
