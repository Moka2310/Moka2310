# 🧪 Guide de Test - Tradalife

## URL de l'application
**https://tradalife-platform.preview.emergentagent.com**

---

## ✅ Checklist des tests

### 1. Page d'accueil
- [ ] La page charge correctement
- [ ] Navigation fonctionne (menu en haut)
- [ ] Toutes les sections s'affichent :
  - Hero section
  - Notre Mission / Pourquoi Nous Choisir
  - Statistiques (75%, 4000 membres, etc.)
  - Nos Canaux (6 icônes)
  - Nos Applications (MT4, MT5)
  - Vidéos
  - Formulaire de contact
- [ ] Footer avec liens Telegram et Facebook

### 2. Page Boutique (/boutique)
- [ ] 5 formations s'affichent :
  - Formation Trading Crypto (299€)
  - Formation Trading Forex (349€)
  - Formation Trading Gold (399€)
  - Formation Indices Boursiers (279€)
  - Pack Complet Trading (999€)
- [ ] Chaque carte de formation affiche :
  - Image
  - Titre
  - Description
  - Prix
  - Durée
  - Niveau
  - Nombre de vidéos
  - Bouton "Acheter maintenant"

### 3. Test d'inscription
1. Cliquer sur "Connexion" en haut à droite
2. Cliquer sur "Pas encore de compte ? S'inscrire"
3. Entrer :
   - Email : test@test.com
   - Mot de passe : Test123!
   - Confirmer le mot de passe
4. Cliquer sur "S'inscrire"
5. ✅ Vous devriez voir un message de succès
6. ✅ Redirection automatique vers le Dashboard

**Note** : Si vous avez configuré Gmail, vous recevrez un email de bienvenue !

### 4. Test de connexion
1. Aller sur /login
2. Entrer :
   - Email : test@test.com
   - Mot de passe : Test123!
3. Cliquer sur "Se connecter"
4. ✅ Redirection vers Dashboard

### 5. Test d'achat d'une formation
1. Aller sur /boutique
2. Choisir une formation
3. Cliquer sur "Acheter maintenant"
4. Si non connecté → redirection vers login
5. Si connecté → redirection vers page de paiement (/checkout)
6. Choisir méthode de paiement :
   - Stripe (carte bancaire)
   - PayPal
7. Cliquer sur "Payer XXX€"
8. ✅ Message de confirmation
9. ✅ Redirection vers Dashboard

**Note** : 
- Sans vraies clés API, le paiement est simulé
- Avec vraies clés, vous serez redirigé vers Stripe/PayPal

### 6. Test du Dashboard (/dashboard)
Après connexion et achat, vous devriez voir :

#### Onglet "Mes Formations"
- Liste des formations achetées
- Si KYC non approuvé :
  - Message "Complétez votre KYC pour débloquer l'accès"
  - Boutons grisés
- Si KYC approuvé :
  - Bouton "Accéder aux vidéos"
  - Liens vers canaux Telegram VIP

#### Onglet "Vérification KYC"
1. Remplir le formulaire :
   - Prénom : John
   - Nom : Doe
   - Pays : France
   - Téléphone : +33612345678
2. Uploader 3 documents :
   - Passeport (jpg, png ou pdf)
   - Carte d'identité (jpg, png ou pdf)
   - Preuve de résidence (jpg, png ou pdf)
3. Cliquer sur "Soumettre ma demande KYC"
4. ✅ Message "KYC soumis avec succès"
5. ✅ Status passe à "En cours de vérification"

**Note** : Si Gmail configuré, vous recevrez un email "KYC en cours"

### 7. Test du Panel Admin (/admin)

**Prérequis** : Avoir un compte admin
```bash
# Dans MongoDB
mongosh
use tradalife
db.users.updateOne(
  { email: "test@test.com" },
  { $set: { role: "admin" } }
)
```

Ensuite :
1. Aller sur /admin
2. Voir les statistiques :
   - Nombre d'utilisateurs
   - KYC en attente
   - Total achats
   - Revenu total
3. Section "Demandes KYC en attente" :
   - Voir les utilisateurs qui ont soumis leur KYC
   - Voir leurs informations (nom, email, pays, téléphone)
   - Voir les documents uploadés
4. Approuver un KYC :
   - Cliquer sur "Approuver"
   - ✅ Message de succès
   - ✅ Email envoyé à l'utilisateur (si Gmail configuré)
5. Rejeter un KYC :
   - Cliquer sur "Rejeter"
   - Entrer une raison
   - Cliquer sur "Confirmer le rejet"
   - ✅ Email envoyé avec la raison

### 8. Tests Mobile

Tester sur smartphone/tablette ou avec Chrome DevTools :
1. Ouvrir Chrome DevTools (F12)
2. Cliquer sur l'icône mobile (Toggle device toolbar)
3. Choisir :
   - iPhone 12 Pro
   - iPad Pro
   - Samsung Galaxy S20
4. Tester toutes les pages
5. Vérifier :
   - [ ] Menu hamburger fonctionne
   - [ ] Navigation fluide
   - [ ] Formulaires utilisables
   - [ ] Boutons cliquables
   - [ ] Texte lisible
   - [ ] Images bien dimensionnées

---

## 🐛 Résolution de problèmes

### L'application ne charge pas
```bash
# Vérifier les logs
tail -f /var/log/supervisor/frontend.out.log
tail -f /var/log/supervisor/backend.err.log

# Redémarrer
sudo supervisorctl restart all
```

### Erreur "Network Error" lors de l'achat
- Vérifier que le backend est démarré
- Tester l'API : `curl https://tradalife-platform.preview.emergentagent.com/api/formations`

### Email non reçu
- Vérifier que Gmail est configuré dans `/app/backend/.env`
- Vérifier les logs : `tail -f /var/log/supervisor/backend.err.log`
- Vérifier les spams

### Paiement ne fonctionne pas
- **Normal** : Sans vraies clés Stripe/PayPal, le paiement est simulé
- Configurer les clés dans `/app/backend/.env` (voir `/app/CONFIGURATION_API.md`)

### Page Admin inaccessible
- Vérifier que votre compte est admin :
```bash
mongosh
use tradalife
db.users.find({ email: "votre-email@test.com" })
# Vérifier que role: "admin"
```

### Documents KYC non uploadés
- Vérifier la taille du fichier (< 5MB recommandé)
- Formats acceptés : jpg, png, pdf
- Vérifier les permissions : `ls -la /app/backend/uploads`

---

## 📊 Scénario de test complet (E2E)

### Test du workflow utilisateur complet

1. **Inscription**
   - Aller sur /login
   - S'inscrire avec test1@test.com / Test123!
   - ✅ Email de bienvenue reçu

2. **Achat formation**
   - Aller sur /boutique
   - Acheter "Formation Trading Crypto" (299€)
   - Choisir Stripe
   - Confirmer le paiement
   - ✅ Email de confirmation reçu

3. **Soumettre KYC**
   - Aller sur /dashboard → Onglet KYC
   - Remplir le formulaire
   - Uploader 3 documents
   - Soumettre
   - ✅ Email "KYC en cours" reçu

4. **Validation Admin**
   - Se connecter avec compte admin
   - Aller sur /admin
   - Voir la demande KYC de test1@test.com
   - Approuver le KYC
   - ✅ Email "KYC approuvé" envoyé

5. **Accès formation**
   - Se reconnecter avec test1@test.com
   - Aller sur /dashboard → Onglet Formations
   - Voir la formation débloquée
   - Cliquer sur "Accéder aux vidéos"
   - Cliquer sur les liens Telegram VIP
   - ✅ Accès complet aux ressources

---

## 📱 Test sur vrais appareils

### iPhone/Android
1. Ouvrir Safari ou Chrome
2. Aller sur https://tradalife-platform.preview.emergentagent.com
3. Tester toutes les fonctionnalités

### Tablette
1. Ouvrir le navigateur
2. Vérifier le layout en mode portrait et paysage
3. Tester les formulaires

---

## ✨ Fonctionnalités à tester en priorité

1. ✅ Inscription/Connexion
2. ✅ Navigation entre les pages
3. ✅ Affichage des formations
4. ✅ Achat d'une formation
5. ✅ Upload de documents KYC
6. ✅ Panel Admin (si vous êtes admin)
7. ✅ Responsive mobile
8. ✅ Envoi d'emails (si Gmail configuré)

---

## 🎯 Prochaines étapes après les tests

Une fois que tout fonctionne :

1. **Configurer les vraies clés API** (voir `/app/CONFIGURATION_API.md`)
   - Stripe
   - PayPal
   - Gmail

2. **Ajouter vos vidéos de formation**
   - Uploader sur Google Drive / YouTube
   - Ajouter les liens dans MongoDB (voir `/app/GUIDE_GESTION_DONNEES.md`)

3. **Personnaliser le contenu**
   - Modifier les descriptions de formations
   - Ajouter vos propres images
   - Changer les liens Telegram

4. **Tester les emails**
   - Inscription
   - Achat
   - KYC

5. **Mettre en production**
   - Configurer un nom de domaine
   - Activer HTTPS
   - Sauvegarder MongoDB régulièrement

---

## 📞 Aide

Si vous rencontrez un problème :
1. Vérifier ce guide de test
2. Consulter `/app/GUIDE_UTILISATION.md`
3. Consulter `/app/CONFIGURATION_API.md`
4. Vérifier les logs :
   ```bash
   tail -f /var/log/supervisor/backend.err.log
   tail -f /var/log/supervisor/frontend.out.log
   ```
