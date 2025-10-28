# 🚀 BUILD TRADABOT EN 3 CLICS (Windows)

## 📋 Prérequis (1 fois)

1. **Installer Python 3.11+**
   - Télécharger: https://www.python.org/downloads/
   - ⚠️ **IMPORTANT**: Cocher "Add Python to PATH"
   - Installer

2. **Avoir MetaTrader 4 ou 5 installé**
   - Pour tester le bot

---

## ⚡ Build en 3 Étapes

### Étape 1: Transférer le dossier
```
Copier le dossier /app/tradabot-app/ vers Windows
Par exemple: C:\TRADABOT\
```

### Étape 2: Installer les dépendances
```
Double-cliquer sur: install.bat
Attendre 2-5 minutes
```

### Étape 3: Créer l'exécutable
```
Double-cliquer sur: build.bat
Attendre 5-10 minutes
```

---

## ✅ Résultat

L'exécutable se trouve dans:
```
C:\TRADABOT\dist\TRADABOT.exe
```

Taille: ~50-80 MB

---

## 🧪 Tester

Double-cliquer sur: `test.bat`

Ou manuellement:
```
cd dist
TRADABOT.exe
```

---

## 📤 Distribuer

### Option 1: Votre serveur
```
Upload TRADABOT.exe vers:
https://tradalife.com/downloads/TRADABOT.exe
```

Puis mettre à jour le lien dans:
```
/app/frontend/src/pages/Tradabot.jsx
```

### Option 2: GitHub Releases
1. Créer un release sur GitHub
2. Upload TRADABOT.exe
3. Copier le lien direct

### Option 3: Google Drive
1. Upload TRADABOT.exe
2. Partager le fichier (lecture seule)
3. Copier le lien de téléchargement direct

---

## 🐛 Problèmes?

### Python introuvable
**Solution**: Réinstaller Python et cocher "Add Python to PATH"

### MetaTrader5 module not found
**Solution**: Normal sur Linux. Sur Windows:
```
pip install MetaTrader5
```

### Erreur lors du build
**Solution**: Regarder les logs et vérifier:
- Python 3.11+
- Toutes les dépendances installées
- MetaTrader 4 ou 5 installé

---

## 📞 Support

Email: yafoy2310@gmail.com

---

**C'est tout! Le build est très simple avec les scripts .bat** 🎉
