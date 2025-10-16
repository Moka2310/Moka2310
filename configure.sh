#!/bin/bash

echo "============================================"
echo "🚀 Configuration Tradalife - Script d'aide"
echo "============================================"
echo ""

echo "📍 Fichier de configuration: /app/backend/.env"
echo ""
echo "Que voulez-vous faire ?"
echo ""
echo "1) Voir la configuration actuelle"
echo "2) Configurer Stripe"
echo "3) Configurer PayPal"
echo "4) Configurer Gmail"
echo "5) Redémarrer l'application"
echo "6) Voir les logs du backend"
echo "7) Accéder à MongoDB"
echo "8) Créer un utilisateur admin"
echo "9) Sauvegarder la base de données"
echo "0) Quitter"
echo ""
read -p "Votre choix (0-9): " choice

case $choice in
    1)
        echo ""
        echo "📄 Configuration actuelle:"
        echo ""
        cat /app/backend/.env
        echo ""
        ;;
    2)
        echo ""
        echo "🔑 Configuration Stripe"
        echo ""
        echo "Allez sur: https://dashboard.stripe.com/apikeys"
        echo ""
        read -p "Entrez votre STRIPE_SECRET_KEY ($STRIPE_SECRET_KEY): " stripe_key
        
        if [ ! -z "$stripe_key" ]; then
            sed -i "s/^STRIPE_SECRET_KEY=.*/STRIPE_SECRET_KEY=$stripe_key/" /app/backend/.env
            echo "✅ Stripe configuré !"
            echo ""
            echo "⚠️  N'oubliez pas de configurer aussi la clé publique dans /app/frontend/.env"
            echo "    REACT_APP_STRIPE_PUBLISHABLE_KEY=pk_live_..."
        fi
        ;;
    3)
        echo ""
        echo "💳 Configuration PayPal"
        echo ""
        echo "Allez sur: https://developer.paypal.com/dashboard"
        echo ""
        read -p "Mode (sandbox ou live): " paypal_mode
        read -p "Client ID: " paypal_client_id
        read -p "Secret: " paypal_secret
        
        if [ ! -z "$paypal_client_id" ]; then
            sed -i "s/^PAYPAL_MODE=.*/PAYPAL_MODE=$paypal_mode/" /app/backend/.env
            sed -i "s/^PAYPAL_CLIENT_ID=.*/PAYPAL_CLIENT_ID=$paypal_client_id/" /app/backend/.env
            sed -i "s/^PAYPAL_CLIENT_SECRET=.*/PAYPAL_CLIENT_SECRET=$paypal_secret/" /app/backend/.env
            echo "✅ PayPal configuré !"
        fi
        ;;
    4)
        echo ""
        echo "📧 Configuration Gmail"
        echo ""
        echo "1. Activez la validation en 2 étapes: https://myaccount.google.com/security"
        echo "2. Créez un mot de passe d'application: https://myaccount.google.com/apppasswords"
        echo ""
        read -p "Votre email Gmail: " gmail_email
        read -p "Mot de passe d'application (16 caractères): " gmail_password
        
        if [ ! -z "$gmail_email" ]; then
            sed -i "s/^GMAIL_EMAIL=.*/GMAIL_EMAIL=$gmail_email/" /app/backend/.env
            sed -i "s/^GMAIL_APP_PASSWORD=.*/GMAIL_APP_PASSWORD=$gmail_password/" /app/backend/.env
            echo "✅ Gmail configuré !"
        fi
        ;;
    5)
        echo ""
        echo "🔄 Redémarrage de l'application..."
        sudo supervisorctl restart backend
        sudo supervisorctl restart frontend
        sleep 2
        echo "✅ Application redémarrée !"
        echo ""
        echo "Vérifier les logs avec: tail -f /var/log/supervisor/backend.out.log"
        ;;
    6)
        echo ""
        echo "📋 Logs du backend (Ctrl+C pour quitter):"
        echo ""
        tail -f /var/log/supervisor/backend.err.log
        ;;
    7)
        echo ""
        echo "🗄️  Connexion à MongoDB..."
        echo ""
        echo "Commandes utiles:"
        echo "  use tradalife              - Utiliser la base Tradalife"
        echo "  db.formations.find()       - Voir les formations"
        echo "  db.users.find()            - Voir les utilisateurs"
        echo "  db.purchases.find()        - Voir les achats"
        echo "  exit                       - Quitter MongoDB"
        echo ""
        mongosh
        ;;
    8)
        echo ""
        echo "👤 Création d'un utilisateur admin"
        echo ""
        read -p "Email de l'utilisateur à promouvoir en admin: " admin_email
        
        if [ ! -z "$admin_email" ]; then
            mongosh --quiet --eval "
                use tradalife;
                var result = db.users.updateOne(
                    { email: '$admin_email' },
                    { \$set: { role: 'admin' } }
                );
                if (result.modifiedCount > 0) {
                    print('✅ Utilisateur $admin_email promu en admin !');
                } else {
                    print('❌ Utilisateur non trouvé. Vérifiez l\'email.');
                }
            "
        fi
        ;;
    9)
        echo ""
        echo "💾 Sauvegarde de la base de données..."
        backup_dir="/app/backups/$(date +%Y%m%d_%H%M%S)"
        mkdir -p $backup_dir
        mongodump --db tradalife --out $backup_dir
        echo "✅ Sauvegarde créée dans: $backup_dir"
        ;;
    0)
        echo "Au revoir !"
        exit 0
        ;;
    *)
        echo "❌ Choix invalide"
        ;;
esac

echo ""
echo "Appuyez sur Entrée pour continuer..."
read
