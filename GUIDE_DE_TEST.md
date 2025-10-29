# 🧪 GUIDE DE TEST - TRADABOT

## 📋 Comptes de Test Disponibles

### 🔐 Compte 1 - Super Admin
```
Email:    yafoy2310@gmail.com
Password: Admin2024!
Rôle:     Super Administrateur
Accès:    TRADABOT + Panel Admin complet
```

### 🔐 Compte 2 - Utilisateur Test
```
Email:    test@test.com
Password: Test2024!
Rôle:     Utilisateur standard
Accès:    TRADABOT uniquement
```

### 🔐 Compte 3 - Compte Demo
```
Email:    demo@tradabot.com
Password: Demo2024!
Rôle:     Utilisateur standard
Accès:    TRADABOT uniquement
```

---

## 🌐 URLs de Test

### Frontend Principal
🔗 https://metaconnect-1.preview.emergentagent.com

### Pages Spécifiques
- 🔐 **Login**: https://metaconnect-1.preview.emergentagent.com/login
- 🤖 **TradaBot Demo (Web)**: https://metaconnect-1.preview.emergentagent.com/tradabot-demo
- ⚙️ **TradaBot Config**: https://metaconnect-1.preview.emergentagent.com/tradabot
- 📊 **Dashboard**: https://metaconnect-1.preview.emergentagent.com/dashboard
- 👨‍💼 **Admin Panel**: https://metaconnect-1.preview.emergentagent.com/admin (admin uniquement)

---

## 🧪 Scénarios de Test

### ✅ Test 1: Connexion et Accès
1. Aller sur https://metaconnect-1.preview.emergentagent.com/login
2. Se connecter avec **test@test.com** / **Test2024!**
3. Vérifier que vous êtes redirigé vers le Dashboard
4. Cliquer sur le bouton **"TRADABOT - MODE DÉMO"**

### ✅ Test 2: TradaBot Demo Web
1. Se connecter avec n'importe quel compte ci-dessus
2. Naviguer vers https://metaconnect-1.preview.emergentagent.com/tradabot-demo
3. **Tester le dropdown MT4**:
   - Cliquer sur l'onglet "Configuration"
   - Descendre à la section "Connexion MT4/MT5"
   - Ouvrir le dropdown "Serveur"
   - **Vérifier**: Le texte est bien BLANC sur fond VIOLET (et non blanc sur blanc)
4. **Tester la configuration**:
   - Remplir Login: 123456
   - Remplir Server: GlobalPrime-Demo (depuis le dropdown)
   - Cliquer "Connecter MT4"
5. **Vérifier les signaux**:
   - Onglet "Signaux" → devrait afficher les signaux Telegram en temps réel

### ✅ Test 3: Configuration des Canaux
1. Aller dans l'onglet "Configuration"
2. Activer/Désactiver les canaux Telegram
3. Modifier les lots (Forex, Crypto, Gold)
4. Cliquer "Sauvegarder Configuration"
5. Vérifier le message de succès

### ✅ Test 4: Visualisation des Signaux Réels
1. Onglet "Signaux"
2. Observer les signaux qui arrivent en temps réel des canaux Telegram
3. Format affiché:
   - Type (BUY/SELL)
   - Symbole (XAUUSD, EURUSD, etc.)
   - Prix d'entrée
   - Stop Loss
   - Take Profit

### ✅ Test 5: Admin Panel (compte yafoy2310@gmail.com uniquement)
1. Se connecter avec **yafoy2310@gmail.com** / **Admin2024!**
2. Aller sur https://metaconnect-1.preview.emergentagent.com/admin
3. Naviguer dans les onglets:
   - Utilisateurs
   - Bot Pre-orders
   - Members
   - Bonus Management
4. Tester l'attribution d'accès TRADABOT à un utilisateur

---

## 🖥️ Test de l'Application Desktop (Windows uniquement)

### Prérequis
- Windows 10/11
- MetaTrader 4 ou 5 installé
- Compte broker (démo recommandé): GlobalPrime, ICMarkets, XM, etc.

### Instructions
1. **Ouvrir MetaTrader 4/5**
2. **Récupérer vos identifiants MT4**:
   - Menu → Outils → Options → Serveur
   - Noter votre **Login** (numéro)
   - Noter votre **Serveur** (ex: GlobalPrime-Demo)
3. **Lancer TRADABOT Desktop** (si construit)
4. **Se connecter** avec un compte ci-dessus
5. **Configurer MT4**:
   - Login: [votre numéro MT4]
   - Password: [votre mot de passe MT4]
   - Server: [votre serveur MT4]
6. **Activer les canaux** Telegram
7. **Définir les lots** pour chaque catégorie
8. **Démarrer le Bot** ▶️
9. **Observer**:
   - Les signaux reçus dans l'onglet "Signaux"
   - Les trades exécutés automatiquement
   - Les positions ouvertes dans MT4
   - Le breakeven activé quand TP1 est atteint

---

## 🎯 Points Clés à Vérifier

### Interface Web
- ✅ Dropdown MT4 lisible (violet + blanc)
- ✅ Connexion fonctionnelle
- ✅ Dashboard accessible
- ✅ Bouton "TRADABOT - MODE DÉMO" visible
- ✅ Signaux Telegram affichés en temps réel
- ✅ Configuration sauvegardée

### Application Desktop (si disponible)
- ✅ Connexion au compte tradalife.com
- ✅ Connexion à MT4/MT5
- ✅ Réception des signaux Telegram
- ✅ Exécution automatique des trades
- ✅ Breakeven activé à TP1
- ✅ Fermeture partielle à TP1 si TP2 existe
- ✅ Logs en temps réel

---

## 🔧 En Cas de Problème

### Impossible de se connecter
- Vérifier l'email et le mot de passe (sensible à la casse)
- Essayer un autre compte de la liste
- Vider le cache du navigateur (Ctrl+Shift+Delete)

### Dropdown MT4 illisible
- Actualiser la page (Ctrl+F5)
- Vider le cache du navigateur
- Le fix a été appliqué, devrait être violet/blanc

### Pas de signaux dans l'onglet Signaux
- Attendre quelques minutes (les signaux arrivent en temps réel)
- Vérifier que les canaux Telegram sont actifs
- Les signaux proviennent des vrais canaux Telegram VIP

### Application Desktop ne se lance pas
- Vérifier que vous êtes sur Windows
- MetaTrader 5 doit être installé
- Python 3.11+ requis pour le développement

---

## 📞 Support

Pour toute question:
- 📧 Email admin: yafoy2310@gmail.com
- 💬 Via le compte admin dans l'application

---

## 🎉 Tout est Prêt!

Vous pouvez maintenant tester toutes les fonctionnalités de TRADABOT avec les comptes ci-dessus.

**Bon testing! 🚀**
