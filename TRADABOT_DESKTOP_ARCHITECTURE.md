# 🤖 TRADABOT - Application Desktop - Plan d'Architecture

## 📋 Vue d'ensemble

Application desktop standalone pour exécuter le bot de copy trading indépendamment du site web.

---

## 🏗️ Architecture Technique

### **Stack Technologique:**
- **Backend Bot**: Python 3.11+
- **Interface**: Electron (HTML/CSS/JS) ou PyQt6
- **Communication MT4**: MetaTrader API ou EA Bridge
- **Telegram**: python-telegram-bot library
- **Packaging**: PyInstaller (Windows .exe) / py2app (Mac .app)

---

## 🔄 Flux de Fonctionnement

```
1. Utilisateur télécharge l'app depuis tradalife.com
2. Lance l'application
3. Se connecte avec ses identifiants tradalife.com
4. L'app vérifie l'accès via API: /api/tradabot/access
5. Si accès OK:
   - Récupère la configuration: /api/tradabot/config
   - Se connecte aux 6 canaux Telegram
   - Se connecte à MT4/MT5
   - Parse les signaux et exécute les trades
6. Bot tourne en local sur le PC/VPS de l'utilisateur
```

---

## 📦 Composants de l'Application

### **1. Module d'Authentification**
```python
# tradabot_auth.py
- Login via tradalife.com API
- Stockage token local (crypté)
- Refresh token automatique
- Vérification accès toutes les heures
```

### **2. Module Telegram**
```python
# tradabot_telegram.py
- Connexion aux 6 canaux (IDs depuis config)
- Parsing des signaux: "BUY XAUUSD @4043, TP1: 4047, TP2: 4055, SL: 4030"
- Détection du mot "Breakeven"
- File d'attente des signaux
```

### **3. Module MT4/MT5**
```python
# tradabot_mt4.py
- Connexion MT4 via socket ou EA
- Envoi des ordres Market
- Monitoring des positions ouvertes
- Gestion breakeven automatique
- Mise à jour status en temps réel
```

### **4. Module Configuration**
```python
# tradabot_config.py
- Récupération config depuis API
- Synchronisation avec serveur
- Configuration lots par catégorie
- Sélection canaux actifs
```

### **5. Interface Utilisateur**
```
- Dashboard: Positions ouvertes, P&L
- Configuration: MT4 login, lots
- Logs: Signaux reçus, trades exécutés
- Status: Connexion MT4, Telegram, API
```

---

## 🎯 Fonctionnalités Phase 2

### **Essentielles:**
1. ✅ Lecture signaux Telegram (6 canaux)
2. ✅ Parsing format: `BUY/SELL SYMBOL @ENTRY, TP1: X, TP2: X, SL: X`
3. ✅ Exécution ordres Market sur MT4
4. ✅ Gestion SL, TP1, TP2
5. ✅ Breakeven automatique (détection mot-clé)
6. ✅ Configuration lots par catégorie
7. ✅ Logs en temps réel
8. ✅ Fonctionnement 24/7 en arrière-plan

### **Avancées (Phase 3):**
- Multi-comptes MT4
- Statistiques avancées
- Notifications push mobile
- Auto-restart en cas d'erreur
- Backup configuration

---

## 🔐 Sécurité

1. **Token crypté** localement (Fernet encryption)
2. **Mot de passe MT4 crypté** (AES-256)
3. **Communication HTTPS** uniquement
4. **Vérification signature** de l'application
5. **Auto-update** sécurisé

---

## 📥 Distribution

### **Site Web:**
- Page `/tradabot/download`
- Bouton "Télécharger pour Windows" (exe)
- Bouton "Télécharger pour Mac" (dmg)
- Guide d'installation PDF

### **Versions:**
- `tradabot-windows-v1.0.exe` (~50 MB)
- `tradabot-mac-v1.0.dmg` (~50 MB)
- Auto-update intégré

---

## 🚀 Plan de Développement

### **Phase 2 (Après recharge tokens):**
**Semaine 1-2:**
1. Module Telegram (parsing signaux)
2. Module MT4 (connexion, ordres)
3. Logique breakeven

**Semaine 3:**
4. Interface desktop (Electron/PyQt)
5. Intégration API tradalife.com
6. Tests avec compte démo

**Semaine 4:**
7. Packaging (exe/dmg)
8. Page téléchargement sur site
9. Tests utilisateurs beta
10. Documentation

### **Phase 3 (Améliorations):**
- Support MT5
- Multi-comptes
- Statistiques avancées
- Version mobile (React Native)?

---

## 💻 Configuration Requise

**Minimum:**
- Windows 10+ ou macOS 10.14+
- 4 GB RAM
- 500 MB espace disque
- Connexion internet stable
- Compte MT4/MT5 actif

**Recommandé:**
- VPS Windows (pour 24/7)
- 8 GB RAM
- SSD
- Connexion fibre

---

## 📝 Notes Importantes

1. **Indépendance**: Le bot fonctionne même si tradalife.com est en maintenance
2. **Performance**: Chaque utilisateur a son propre bot = pas de charge serveur
3. **Fiabilité**: Pas de downtime centralisé
4. **Contrôle**: Utilisateur a le contrôle total sur son bot

---

## 🎯 Estimation Développement

**Temps**: 3-4 semaines (après recharge tokens)
**Complexité**: Moyenne-Élevée
**Coût tokens estimé**: ~20,000-30,000 tokens

---

## ✅ Prochaines Étapes

1. ✅ Interface web configurée (FAIT)
2. ⏳ Développement bot Python (Phase 2)
3. ⏳ Interface desktop (Phase 2)
4. ⏳ Tests & packaging (Phase 2)
5. ⏳ Déploiement & distribution (Phase 2)

**Note**: Architecture hybride permet de commencer avec interface web maintenant, et ajouter l'app desktop plus tard sans tout refaire!

---

**Date**: 2025-10-28
**Status**: Phase 1 complète ✅
**Prêt pour**: Phase 2 (développement bot)
