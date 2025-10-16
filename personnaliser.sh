#!/bin/bash

echo "============================================"
echo "🎨 Personnalisation Tradalife"
echo "============================================"
echo ""

echo "Que voulez-vous modifier ?"
echo ""
echo "1) Ajouter une vidéo à la page d'accueil"
echo "2) Modifier l'image d'une formation"
echo "3) Modifier la description d'une formation"
echo "4) Modifier le prix d'une formation"
echo "5) Ajouter une nouvelle formation"
echo "6) Voir toutes les formations"
echo "7) Modifier les images des canaux (fichier)"
echo "0) Quitter"
echo ""
read -p "Votre choix (0-7): " choice

case $choice in
    1)
        echo ""
        echo "📹 Ajout d'une vidéo page d'accueil"
        echo ""
        read -p "Titre de la vidéo: " video_title
        read -p "Description: " video_desc
        read -p "URL YouTube (embed): " video_url
        read -p "Durée (ex: 10:30): " video_duration
        
        if [ ! -z "$video_title" ]; then
            video_id="home_video_$(date +%s)"
            mongosh --quiet --eval "
                use tradalife;
                db.videos.insertOne({
                    id: '$video_id',
                    formationId: 'home',
                    title: '$video_title',
                    description: '$video_desc',
                    url: '$video_url',
                    duration: '$video_duration',
                    order: 1,
                    section: 'homepage',
                    createdAt: new Date()
                });
                print('✅ Vidéo ajoutée avec succès !');
            "
        fi
        ;;
    2)
        echo ""
        echo "🖼️  Modification de l'image d'une formation"
        echo ""
        echo "Formations disponibles:"
        mongosh --quiet --eval "
            use tradalife;
            db.formations.find({}, {id: 1, title: 1, _id: 0}).forEach(function(doc) {
                print(doc.id + ' - ' + doc.title);
            });
        "
        echo ""
        read -p "ID de la formation (1-5): " formation_id
        read -p "Nouvelle URL de l'image: " new_image
        
        if [ ! -z "$formation_id" ]; then
            mongosh --quiet --eval "
                use tradalife;
                db.formations.updateOne(
                    { id: '$formation_id' },
                    { \$set: { image: '$new_image' }}
                );
                print('✅ Image modifiée !');
            "
        fi
        ;;
    3)
        echo ""
        echo "📝 Modification de la description"
        echo ""
        echo "Formations disponibles:"
        mongosh --quiet --eval "
            use tradalife;
            db.formations.find({}, {id: 1, title: 1, _id: 0}).forEach(function(doc) {
                print(doc.id + ' - ' + doc.title);
            });
        "
        echo ""
        read -p "ID de la formation (1-5): " formation_id
        echo "Entrez la nouvelle description (tapez sur Entrée 2 fois pour finir):"
        description=""
        while IFS= read -r line; do
            [ -z "$line" ] && break
            description="$description$line "
        done
        
        if [ ! -z "$formation_id" ]; then
            mongosh --quiet --eval "
                use tradalife;
                db.formations.updateOne(
                    { id: '$formation_id' },
                    { \$set: { description: '$description' }}
                );
                print('✅ Description modifiée !');
            "
        fi
        ;;
    4)
        echo ""
        echo "💰 Modification du prix"
        echo ""
        echo "Formations disponibles:"
        mongosh --quiet --eval "
            use tradalife;
            db.formations.find({}, {id: 1, title: 1, price: 1, _id: 0}).forEach(function(doc) {
                print(doc.id + ' - ' + doc.title + ' - ' + doc.price + '€');
            });
        "
        echo ""
        read -p "ID de la formation (1-5): " formation_id
        read -p "Nouveau prix (ex: 249.0): " new_price
        
        if [ ! -z "$formation_id" ]; then
            mongosh --quiet --eval "
                use tradalife;
                db.formations.updateOne(
                    { id: '$formation_id' },
                    { \$set: { price: $new_price }}
                );
                print('✅ Prix modifié !');
            "
        fi
        ;;
    5)
        echo ""
        echo "➕ Ajout d'une nouvelle formation"
        echo ""
        read -p "ID (ex: 6): " new_id
        read -p "Titre: " new_title
        read -p "Description: " new_desc
        read -p "Prix (ex: 329.0): " new_price
        read -p "Durée (ex: 9 heures): " new_duration
        read -p "Niveau (ex: Intermédiaire): " new_level
        read -p "URL de l'image: " new_image
        read -p "Nombre de vidéos: " new_video_count
        read -p "Lien Telegram: " new_telegram
        
        if [ ! -z "$new_id" ]; then
            mongosh --quiet --eval "
                use tradalife;
                db.formations.insertOne({
                    id: '$new_id',
                    title: '$new_title',
                    description: '$new_desc',
                    price: $new_price,
                    duration: '$new_duration',
                    level: '$new_level',
                    image: '$new_image',
                    videoCount: $new_video_count,
                    telegramLinks: [
                        {
                            name: 'Canal VIP',
                            url: '$new_telegram'
                        }
                    ],
                    createdAt: new Date()
                });
                print('✅ Formation ajoutée !');
            "
        fi
        ;;
    6)
        echo ""
        echo "📋 Liste des formations"
        echo ""
        mongosh --quiet --eval "
            use tradalife;
            db.formations.find().forEach(function(doc) {
                print('');
                print('ID: ' + doc.id);
                print('Titre: ' + doc.title);
                print('Prix: ' + doc.price + '€');
                print('Description: ' + doc.description.substring(0, 100) + '...');
                print('Image: ' + doc.image);
                print('---');
            });
        "
        ;;
    7)
        echo ""
        echo "🖼️  Modifier les images des canaux"
        echo ""
        echo "Ouverture du fichier /app/frontend/src/mockData.js"
        echo ""
        echo "Cherchez la section 'export const canaux' et modifiez les URLs"
        echo ""
        nano /app/frontend/src/mockData.js
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
