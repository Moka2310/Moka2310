# 🎯 GUIDE ULTRA-SIMPLE - TRADABOT POUR DÉBUTANTS

## ⚠️ VOUS N'AVEZ PAS BESOIN D'ÊTRE UN EXPERT!

Ce guide est fait pour quelqu'un qui ne connaît RIEN à la programmation.
Suivez juste les étapes, image par image.

---

## 📦 ÉTAPE 1: TÉLÉCHARGER LE PACKAGE

### 1.1 Se connecter au Panel Admin
1. Ouvrez votre navigateur (Chrome, Firefox, Edge...)
2. Allez sur: https://www.tradalife.com/admin
3. Connectez-vous avec:
   - Email: yafoy2310@gmail.com
   - Mot de passe: Admin2024!

### 1.2 Télécharger TRADABOT
1. Dans le menu en haut, cliquez sur **"Télécharger TRADABOT"**
2. Cliquez sur le gros bouton **"⬇️ TÉLÉCHARGER LE PACKAGE"**
3. Un fichier `TRADABOT_Package.zip` va se télécharger
4. Le fichier ira dans votre dossier "Téléchargements"

---

## 💻 ÉTAPE 2: PRÉPARER VOTRE PC WINDOWS

### 2.1 Vérifier que vous avez Windows 10 ou 11
1. Clic droit sur le menu Démarrer (en bas à gauche)
2. Cliquer sur "Système"
3. Vous devez voir "Windows 10" ou "Windows 11"
   - ✅ Si oui: Parfait, continuez
   - ❌ Si Windows 7/8: Il faut mettre à jour Windows

### 2.2 Installer Python (Gratuit)
1. Allez sur: https://www.python.org/downloads/
2. Cliquez sur le gros bouton jaune **"Download Python 3.11.x"**
3. Le fichier `python-3.11.x.exe` se télécharge
4. **Double-cliquez** sur le fichier téléchargé
5. ⚠️ **TRÈS IMPORTANT:** 
   - ✅ COCHEZ la case **"Add Python to PATH"** tout en bas
   - C'EST ESSENTIEL!
6. Cliquez sur **"Install Now"**
7. Attendez que l'installation se termine (2-3 minutes)
8. Cliquez sur "Close"

**Comment vérifier que Python est installé:**
1. Appuyez sur les touches `Windows + R`
2. Tapez: `cmd`
3. Appuyez sur Entrée
4. Dans la fenêtre noire qui s'ouvre, tapez: `python --version`
5. Vous devez voir: `Python 3.11.x`
   - ✅ Si oui: Parfait!
   - ❌ Si erreur: Recommencez l'installation de Python

### 2.3 Installer MetaTrader 4 ou 5 (Gratuit)
1. Allez sur le site de votre broker (ex: XM, ICMarkets, etc.)
2. OU allez directement sur: https://www.metatrader5.com/
3. Téléchargez et installez MetaTrader 4 OU MetaTrader 5
4. Créez un compte DÉMO si vous n'en avez pas
   - Dans MT4/MT5: Fichier → Ouvrir un compte → Serveur démo
   - Notez bien votre Login et Mot de passe!

---

## 📂 ÉTAPE 3: EXTRAIRE ET PRÉPARER

### 3.1 Extraire le fichier ZIP
1. Allez dans votre dossier "Téléchargements"
2. Trouvez le fichier `TRADABOT_Package.zip`
3. **Clic droit** sur le fichier
4. Choisir **"Extraire tout..."**
5. Choisir un emplacement simple, par exemple:
   - `C:\TRADABOT\`
6. Cliquer sur **"Extraire"**
7. Un dossier `tradabot-app` est créé

### 3.2 Ouvrir PowerShell dans le bon dossier
1. Ouvrez l'explorateur de fichiers
2. Naviguez vers le dossier extrait: `C:\TRADABOT\tradabot-app\`
3. Dans la barre d'adresse (en haut), cliquez dedans
4. Tapez: `powershell`
5. Appuyez sur Entrée
6. Une fenêtre bleue s'ouvre (PowerShell)

---

## ⚙️ ÉTAPE 4: INSTALLER LES DÉPENDANCES

### Dans la fenêtre PowerShell (bleue):

**Tapez exactement cette commande et appuyez sur Entrée:**
```
pip install -r requirements.txt
```

**Attendez:** Ça va prendre 5-10 minutes. 
Vous allez voir plein de texte défiler. C'est normal!

**Quand c'est fini:**
Vous voyez `Successfully installed...` 
✅ Parfait, c'est terminé!

---

## 🔨 ÉTAPE 5: CONSTRUIRE L'APPLICATION

### Dans la même fenêtre PowerShell:

**Tapez cette commande et appuyez sur Entrée:**
```
python build_windows.py
```

**Attendez:** Ça va prendre 5-15 minutes.

**Ce qui va se passer:**
- Vous verrez plein de texte
- À la fin, vous verrez:
  ```
  ✅ BUILD RÉUSSI!
  📦 Exécutable créé: dist/TRADABOT.exe
  ```

✅ **FÉLICITATIONS! L'application est créée!**

---

## 🚀 ÉTAPE 6: LANCER TRADABOT

### 6.1 Trouver l'exécutable
1. Dans l'explorateur de fichiers
2. Allez dans: `C:\TRADABOT\tradabot-app\dist\`
3. Vous devez voir un fichier: **TRADABOT.exe**

### 6.2 Lancer l'application
1. **Double-cliquez** sur `TRADABOT.exe`
2. ⚠️ Si Windows vous demande: "Voulez-vous autoriser...?"
   - Cliquez sur **"Oui"**
3. L'application TRADABOT s'ouvre! 🎉

---

## 🔐 ÉTAPE 7: SE CONNECTER

### Dans l'application TRADABOT:

**Onglet "Connexion":**
1. Email: `yafoy2310@gmail.com`
2. Mot de passe: `Admin2024!`
3. Cliquez sur **"SE CONNECTER"**

✅ Vous devriez voir: "Connexion réussie"

---

## ⚙️ ÉTAPE 8: CONFIGURER MT4

### Onglet "Configuration":

**Section "Configuration MT4/MT5":**

1. **Login:** Entrez votre numéro de compte MT4
   - Exemple: 12345678
   - (Vous l'avez quand vous avez créé le compte)

2. **Password:** Entrez le mot de passe de votre compte MT4

3. **Server:** Cliquez sur la liste déroulante
   - Trouvez votre broker (ex: XM.COM-Demo, ICMarkets-Demo, etc.)
   - OU tapez pour rechercher
   - OU sélectionnez "Saisir manuellement" si votre serveur n'est pas listé

4. Cliquez sur **"CONNECTER MT4"**

✅ Vous devriez voir: "Connecté à MT4"

---

## 📡 ÉTAPE 9: ACTIVER LES CANAUX

### Toujours dans l'onglet "Configuration":

**Section "Canaux Telegram":**

Activez les canaux que vous voulez surveiller:
- ✅ Forex
- ✅ Crypto
- ✅ Gold
- ✅ Indices
- ✅ Actions
- ✅ Commodités

**Section "Configuration des Lots":**

Définissez combien vous voulez trader:
- Forex: 0.01 (recommandé pour débuter)
- Crypto: 0.01
- Gold: 0.01

Cliquez sur **"Sauvegarder Configuration"**

---

## ▶️ ÉTAPE 10: DÉMARRER LE BOT

### Onglet "Configuration":

1. Cliquez sur le gros bouton vert: **"▶️ DÉMARRER LE BOT"**

2. Vous devriez voir:
   - Status en haut à droite: "🟢 Bot Actif"
   - Dans l'onglet "Logs": "🚀 BOT DÉMARRÉ"

✅ **ÇA Y EST! LE BOT FONCTIONNE!**

---

## 📊 ÉTAPE 11: VÉRIFIER QUE ÇA MARCHE

### Onglet "Signaux":
- Attendez quelques minutes
- Les signaux des canaux Telegram vont apparaître ici
- Format: "BUY XAUUSD @ 2043 | TP: 2047 | SL: 2030"

### Onglet "Positions":
- Les trades exécutés automatiquement apparaîtront ici
- Vous verrez aussi vos positions dans MetaTrader 4/5

### Onglet "Logs":
- Tous les événements sont enregistrés ici
- Exemple:
  - "📡 Signal reçu: BUY XAUUSD"
  - "✅ Trade exécuté: Ticket 123456"
  - "🔒 Breakeven activé"

---

## ❓ EN CAS DE PROBLÈME

### Problème 1: "Python n'est pas reconnu"
**Solution:**
- Vous avez oublié de cocher "Add Python to PATH"
- Désinstallez Python (Panneau de configuration → Programmes)
- Réinstallez et cochez la case!

### Problème 2: "Échec connexion MT4"
**Solution:**
- Vérifiez que le Login est correct (c'est un numéro)
- Vérifiez que le Mot de passe est correct
- Vérifiez le nom EXACT du serveur dans MT4:
  - Ouvrez MT4 → Outils → Options → Serveur
  - Copiez le nom exact

### Problème 3: "Pas de signaux"
**Solution:**
- Attendez quelques minutes (les signaux arrivent en temps réel)
- Vérifiez que vous avez activé les canaux
- Vérifiez votre connexion internet

### Problème 4: "Le .exe ne se lance pas"
**Solution:**
- Votre antivirus bloque peut-être l'application
- Ajoutez TRADABOT.exe aux exceptions de l'antivirus
- OU désactivez temporairement l'antivirus pour tester

---

## 📞 BESOIN D'AIDE?

**Email:** yafoy2310@gmail.com  
**Support:** support@tradalife.com  
**Site:** https://www.tradalife.com

---

## 🎉 FÉLICITATIONS!

Vous avez réussi à installer et configurer TRADABOT!

Le bot va maintenant:
- ✅ Surveiller les 6 canaux Telegram VIP 24/7
- ✅ Copier automatiquement les signaux sur votre compte MT4
- ✅ Gérer le Stop Loss et Take Profit
- ✅ Activer le Breakeven quand TP1 est atteint
- ✅ Fermer partiellement les positions à TP1 si TP2 existe

**Laissez l'application ouverte pour que le bot fonctionne!**

---

**Date:** Octobre 2025  
**Version:** 1.0 - Guide Ultra-Simple
