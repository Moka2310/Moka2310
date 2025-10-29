"""
TRADABOT - Version Web Flask
Application web accessible via navigateur pour tester immédiatement
Mode démo pour simuler le trading sans MT4/MT5
"""
from flask import Flask, render_template_string, request, jsonify, session
from flask_cors import CORS
import requests
from datetime import datetime, timezone
import secrets
import json

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
CORS(app)

# Configuration
API_BASE_URL = "https://auto-trader-70.preview.emergentagent.com"
TELEGRAM_CHANNELS = {
    'forex': -1002425540174,
    'crypto': -1002279973041,
    'gold': -1002355600472,
    'indices': -1002339785500,
    'actions': -1002376632406,
    'commodites': -1002368060694
}

# Stockage en mémoire (remplacé par DB en production)
active_signals = []
demo_positions = []
demo_account = {
    'balance': 10000.0,
    'equity': 10000.0,
    'profit': 0.0
}

# Template HTML complet
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TRADABOT - Version Web Démo</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #fff;
            min-height: 100vh;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            text-align: center;
            padding: 40px 20px;
            background: rgba(255,255,255,0.05);
            border-radius: 20px;
            margin-bottom: 30px;
        }
        .header h1 {
            font-size: 3em;
            background: linear-gradient(to right, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }
        .status-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px;
            background: rgba(255,255,255,0.05);
            border-radius: 15px;
            margin-bottom: 30px;
        }
        .status-item {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .status-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }
        .status-dot.connected { background: #4ade80; }
        .status-dot.disconnected { background: #ef4444; }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        .tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            overflow-x: auto;
        }
        .tab {
            padding: 15px 30px;
            background: rgba(255,255,255,0.05);
            border: none;
            color: #fff;
            cursor: pointer;
            border-radius: 10px;
            font-size: 16px;
            transition: all 0.3s;
            white-space: nowrap;
        }
        .tab:hover {
            background: rgba(255,255,255,0.1);
        }
        .tab.active {
            background: linear-gradient(to right, #667eea, #764ba2);
        }
        .tab-content {
            display: none;
            animation: fadeIn 0.3s;
        }
        .tab-content.active {
            display: block;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .card {
            background: rgba(255,255,255,0.05);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 20px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        .form-group label {
            display: block;
            margin-bottom: 8px;
            color: #a0aec0;
        }
        .form-group input {
            width: 100%;
            padding: 12px;
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 8px;
            color: #fff;
            font-size: 16px;
        }
        .form-group input:focus {
            outline: none;
            border-color: #667eea;
        }
        .btn {
            padding: 12px 30px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
        }
        .btn-primary {
            background: linear-gradient(to right, #667eea, #764ba2);
            color: #fff;
        }
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }
        .btn-success {
            background: #4ade80;
            color: #000;
        }
        .btn-danger {
            background: #ef4444;
            color: #fff;
        }
        .btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        .stat-card {
            background: rgba(255,255,255,0.05);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
        }
        .stat-card h3 {
            color: #a0aec0;
            font-size: 14px;
            margin-bottom: 10px;
        }
        .stat-card .value {
            font-size: 32px;
            font-weight: bold;
            color: #4ade80;
        }
        .signals-list, .positions-list {
            max-height: 400px;
            overflow-y: auto;
        }
        .signal-item, .position-item {
            background: rgba(255,255,255,0.05);
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 10px;
            border-left: 4px solid #667eea;
        }
        .signal-item.buy { border-left-color: #4ade80; }
        .signal-item.sell { border-left-color: #ef4444; }
        .position-item.profit { border-left-color: #4ade80; }
        .position-item.loss { border-left-color: #ef4444; }
        .logs {
            background: #000;
            padding: 20px;
            border-radius: 10px;
            max-height: 400px;
            overflow-y: auto;
            font-family: 'Courier New', monospace;
            font-size: 14px;
        }
        .log-entry {
            margin-bottom: 5px;
            color: #4ade80;
        }
        .channel-config {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 15px;
            background: rgba(255,255,255,0.05);
            border-radius: 10px;
            margin-bottom: 10px;
        }
        .switch {
            position: relative;
            display: inline-block;
            width: 60px;
            height: 34px;
        }
        .switch input {
            opacity: 0;
            width: 0;
            height: 0;
        }
        .slider {
            position: absolute;
            cursor: pointer;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: #ccc;
            transition: .4s;
            border-radius: 34px;
        }
        .slider:before {
            position: absolute;
            content: "";
            height: 26px;
            width: 26px;
            left: 4px;
            bottom: 4px;
            background-color: white;
            transition: .4s;
            border-radius: 50%;
        }
        input:checked + .slider {
            background-color: #4ade80;
        }
        input:checked + .slider:before {
            transform: translateX(26px);
        }
        .demo-badge {
            display: inline-block;
            padding: 5px 15px;
            background: linear-gradient(to right, #f59e0b, #ef4444);
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
            margin-left: 10px;
        }
        .alert {
            padding: 15px 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .alert-info {
            background: rgba(59, 130, 246, 0.2);
            border-left: 4px solid #3b82f6;
        }
        .alert-warning {
            background: rgba(245, 158, 11, 0.2);
            border-left: 4px solid #f59e0b;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 TRADABOT <span class="demo-badge">MODE DÉMO</span></h1>
            <p>Version Web - Trading Automatisé</p>
        </div>

        <div class="status-bar">
            <div class="status-item">
                <div class="status-dot" id="statusDot"></div>
                <span id="statusText">Déconnecté</span>
            </div>
            <div class="status-item">
                <span>👤 <span id="userEmail">-</span></span>
            </div>
            <div class="status-item">
                <button class="btn btn-danger" id="logoutBtn" style="display:none;" onclick="logout()">Déconnexion</button>
            </div>
        </div>

        <div class="tabs">
            <button class="tab active" onclick="showTab('login')">🔐 Connexion</button>
            <button class="tab" onclick="showTab('dashboard')" id="dashboardTab" disabled>📊 Dashboard</button>
            <button class="tab" onclick="showTab('config')" id="configTab" disabled>⚙️ Configuration</button>
            <button class="tab" onclick="showTab('signals')" id="signalsTab" disabled>📡 Signaux</button>
            <button class="tab" onclick="showTab('positions')" id="positionsTab" disabled>💼 Positions</button>
            <button class="tab" onclick="showTab('logs')" id="logsTab" disabled>📋 Logs</button>
        </div>

        <!-- Login Tab -->
        <div id="login-tab" class="tab-content active">
            <div class="card">
                <h2>Connexion à votre compte</h2>
                <div class="alert alert-info">
                    ℹ️ Connectez-vous avec vos identifiants tradalife.com
                </div>
                <div class="form-group">
                    <label>📧 Email</label>
                    <input type="email" id="loginEmail" placeholder="votre@email.com">
                </div>
                <div class="form-group">
                    <label>🔒 Mot de passe</label>
                    <input type="password" id="loginPassword" placeholder="Mot de passe">
                </div>
                <button class="btn btn-primary" onclick="login()">🚀 Se Connecter</button>
            </div>
        </div>

        <!-- Dashboard Tab -->
        <div id="dashboard-tab" class="tab-content">
            <div class="alert alert-warning">
                ⚠️ MODE DÉMO - Les trades sont simulés (pas de connexion MT4/MT5 réelle)
            </div>
            <div class="grid">
                <div class="stat-card">
                    <h3>Balance</h3>
                    <div class="value" id="balance">10,000.00 $</div>
                </div>
                <div class="stat-card">
                    <h3>Équité</h3>
                    <div class="value" id="equity">10,000.00 $</div>
                </div>
                <div class="stat-card">
                    <h3>Profit</h3>
                    <div class="value" id="profit">0.00 $</div>
                </div>
            </div>

            <div class="card">
                <h2>Contrôles</h2>
                <button class="btn btn-success" onclick="startBot()" id="startBtn">▶️ DÉMARRER LE BOT</button>
                <button class="btn btn-danger" onclick="stopBot()" id="stopBtn" style="display:none;">⏹️ ARRÊTER LE BOT</button>
            </div>
        </div>

        <!-- Config Tab -->
        <div id="config-tab" class="tab-content">
            <div class="card">
                <h2>Configuration des Canaux Telegram</h2>
                <div class="channel-config">
                    <span>📊 Forex</span>
                    <label class="switch">
                        <input type="checkbox" id="ch-forex" checked>
                        <span class="slider"></span>
                    </label>
                </div>
                <div class="channel-config">
                    <span>💰 Crypto</span>
                    <label class="switch">
                        <input type="checkbox" id="ch-crypto" checked>
                        <span class="slider"></span>
                    </label>
                </div>
                <div class="channel-config">
                    <span>🥇 Gold</span>
                    <label class="switch">
                        <input type="checkbox" id="ch-gold" checked>
                        <span class="slider"></span>
                    </label>
                </div>
                <div class="channel-config">
                    <span>📈 Indices</span>
                    <label class="switch">
                        <input type="checkbox" id="ch-indices" checked>
                        <span class="slider"></span>
                    </label>
                </div>
                <div class="channel-config">
                    <span>📊 Actions</span>
                    <label class="switch">
                        <input type="checkbox" id="ch-actions" checked>
                        <span class="slider"></span>
                    </label>
                </div>
                <div class="channel-config">
                    <span>🛢️ Commodités</span>
                    <label class="switch">
                        <input type="checkbox" id="ch-commodites" checked>
                        <span class="slider"></span>
                    </label>
                </div>
            </div>

            <div class="card">
                <h2>Configuration des Lots</h2>
                <div class="form-group">
                    <label>Forex (lot)</label>
                    <input type="number" id="lot-forex" value="0.01" step="0.01" min="0.01">
                </div>
                <div class="form-group">
                    <label>Crypto (lot)</label>
                    <input type="number" id="lot-crypto" value="0.01" step="0.01" min="0.01">
                </div>
                <div class="form-group">
                    <label>Gold (lot)</label>
                    <input type="number" id="lot-gold" value="0.01" step="0.01" min="0.01">
                </div>
                <button class="btn btn-primary" onclick="saveConfig()">💾 Sauvegarder</button>
            </div>
        </div>

        <!-- Signals Tab -->
        <div id="signals-tab" class="tab-content">
            <div class="card">
                <h2>📡 Signaux Reçus</h2>
                <div class="signals-list" id="signalsList">
                    <p style="text-align:center; color:#a0aec0;">Aucun signal reçu</p>
                </div>
            </div>
        </div>

        <!-- Positions Tab -->
        <div id="positions-tab" class="tab-content">
            <div class="card">
                <h2>💼 Positions Ouvertes (Simulation)</h2>
                <div class="positions-list" id="positionsList">
                    <p style="text-align:center; color:#a0aec0;">Aucune position ouverte</p>
                </div>
            </div>
        </div>

        <!-- Logs Tab -->
        <div id="logs-tab" class="tab-content">
            <div class="card">
                <h2>📋 Logs d'Activité</h2>
                <div class="logs" id="logsList">
                    <div class="log-entry">[SYSTÈME] TRADABOT initialisé - Mode Démo</div>
                </div>
            </div>
        </div>
    </div>

    <script>
        let isLoggedIn = false;
        let isBotRunning = false;
        let userToken = null;

        function showTab(tabName) {
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });
            document.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active');
            });
            
            document.getElementById(tabName + '-tab').classList.add('active');
            event.target.classList.add('active');
        }

        function addLog(message) {
            const logsList = document.getElementById('logsList');
            const time = new Date().toLocaleTimeString();
            const logEntry = document.createElement('div');
            logEntry.className = 'log-entry';
            logEntry.textContent = `[${time}] ${message}`;
            logsList.appendChild(logEntry);
            logsList.scrollTop = logsList.scrollHeight;
        }

        async function login() {
            const email = document.getElementById('loginEmail').value;
            const password = document.getElementById('loginPassword').value;

            if (!email || !password) {
                alert('Veuillez remplir tous les champs');
                return;
            }

            addLog('Connexion en cours...');

            try {
                const response = await fetch('/api/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                });

                const data = await response.json();

                if (data.success) {
                    isLoggedIn = true;
                    userToken = data.token;
                    
                    document.getElementById('statusDot').classList.add('connected');
                    document.getElementById('statusText').textContent = 'Connecté';
                    document.getElementById('userEmail').textContent = email;
                    document.getElementById('logoutBtn').style.display = 'block';

                    // Enable tabs
                    ['dashboardTab', 'configTab', 'signalsTab', 'positionsTab', 'logsTab'].forEach(id => {
                        document.getElementById(id).disabled = false;
                    });

                    addLog('✅ Connexion réussie');
                    showTab('dashboard');
                    document.querySelector('[onclick="showTab(\'dashboard\')"]').click();
                } else {
                    alert('Erreur: ' + data.error);
                    addLog('❌ Connexion échouée: ' + data.error);
                }
            } catch (error) {
                alert('Erreur de connexion: ' + error.message);
                addLog('❌ Erreur: ' + error.message);
            }
        }

        function logout() {
            isLoggedIn = false;
            userToken = null;
            
            document.getElementById('statusDot').classList.remove('connected');
            document.getElementById('statusText').textContent = 'Déconnecté';
            document.getElementById('userEmail').textContent = '-';
            document.getElementById('logoutBtn').style.display = 'none';

            ['dashboardTab', 'configTab', 'signalsTab', 'positionsTab', 'logsTab'].forEach(id => {
                document.getElementById(id).disabled = true;
            });

            addLog('🚪 Déconnecté');
            showTab('login');
            document.querySelector('[onclick="showTab(\'login\')"]').click();
        }

        async function startBot() {
            addLog('🚀 Démarrage du bot...');
            isBotRunning = true;
            document.getElementById('startBtn').style.display = 'none';
            document.getElementById('stopBtn').style.display = 'inline-block';
            
            addLog('✅ Bot démarré - Surveillance des canaux Telegram active');
            addLog('📡 Écoute des signaux sur 6 canaux...');
            
            // Simuler quelques signaux
            setTimeout(() => addDemoSignal('BUY', 'EURUSD', 1.0850, 1.0820, 1.0900), 5000);
            setTimeout(() => addDemoSignal('SELL', 'XAUUSD', 2050.00, 2060.00, 2035.00), 10000);
        }

        function stopBot() {
            addLog('⏹️ Arrêt du bot...');
            isBotRunning = false;
            document.getElementById('startBtn').style.display = 'inline-block';
            document.getElementById('stopBtn').style.display = 'none';
            addLog('✅ Bot arrêté');
        }

        function addDemoSignal(type, symbol, entry, sl, tp) {
            const signalsList = document.getElementById('signalsList');
            if (signalsList.querySelector('p')) {
                signalsList.innerHTML = '';
            }

            const signalItem = document.createElement('div');
            signalItem.className = `signal-item ${type.toLowerCase()}`;
            signalItem.innerHTML = `
                <div style="display:flex; justify-content:space-between;">
                    <strong>${type} ${symbol}</strong>
                    <span>${new Date().toLocaleTimeString()}</span>
                </div>
                <div style="margin-top:10px;">
                    Entry: ${entry} | SL: ${sl} | TP: ${tp}
                </div>
            `;
            signalsList.insertBefore(signalItem, signalsList.firstChild);

            addLog(`📡 Signal reçu: ${type} ${symbol} @ ${entry}`);
            
            // Simuler l'exécution
            setTimeout(() => executeDemoTrade(type, symbol, entry, sl, tp), 1000);
        }

        function executeDemoTrade(type, symbol, entry, sl, tp) {
            const positionsList = document.getElementById('positionsList');
            if (positionsList.querySelector('p')) {
                positionsList.innerHTML = '';
            }

            const ticket = Math.floor(Math.random() * 1000000);
            const positionItem = document.createElement('div');
            positionItem.className = 'position-item profit';
            positionItem.id = `pos-${ticket}`;
            positionItem.innerHTML = `
                <div style="display:flex; justify-content:space-between;">
                    <strong>#${ticket} - ${type} ${symbol}</strong>
                    <span style="color:#4ade80;">+0.00 $</span>
                </div>
                <div style="margin-top:10px; font-size:14px;">
                    Lot: 0.01 | Entry: ${entry} | SL: ${sl} | TP: ${tp}
                </div>
            `;
            positionsList.insertBefore(positionItem, positionsList.firstChild);

            addLog(`✅ Trade exécuté: ${type} ${symbol} | Ticket: ${ticket}`);
        }

        function saveConfig() {
            addLog('💾 Configuration sauvegardée');
            alert('Configuration sauvegardée avec succès!');
        }

        // Auto-scroll logs
        setInterval(() => {
            const logsList = document.getElementById('logsList');
            logsList.scrollTop = logsList.scrollHeight;
        }, 1000);
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    """Page principale"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/login', methods=['POST'])
def api_login():
    """Connexion à l'API tradalife"""
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        # Appel à l'API tradalife
        response = requests.post(
            f"{API_BASE_URL}/api/auth/login",
            json={'email': email, 'password': password},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            token = result.get('token')
            
            # Vérifier l'accès TRADABOT
            headers = {'Authorization': f'Bearer {token}'}
            access_response = requests.get(
                f"{API_BASE_URL}/api/tradabot/access",
                headers=headers,
                timeout=10
            )
            
            if access_response.status_code == 200:
                access_data = access_response.json()
                if access_data.get('hasAccess'):
                    session['token'] = token
                    session['email'] = email
                    return jsonify({
                        'success': True,
                        'token': token,
                        'user': result.get('user', {})
                    })
                else:
                    return jsonify({
                        'success': False,
                        'error': 'Vous n\'avez pas accès à TRADABOT'
                    }), 403
            else:
                return jsonify({
                    'success': False,
                    'error': 'Erreur vérification accès'
                }), 403
        else:
            return jsonify({
                'success': False,
                'error': 'Email ou mot de passe incorrect'
            }), 401
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/status')
def api_status():
    """Statut du bot"""
    return jsonify({
        'connected': session.get('token') is not None,
        'botRunning': False,
        'account': demo_account,
        'signals': len(active_signals),
        'positions': len(demo_positions)
    })

if __name__ == '__main__':
    print("=" * 60)
    print("  🤖 TRADABOT - Version Web Démo")
    print("=" * 60)
    print("")
    print("  📱 Application web accessible via navigateur")
    print("  🔐 Connexion avec votre compte tradalife.com")
    print("  ⚠️  Mode démo - Trades simulés")
    print("")
    print("  🌐 URL: http://localhost:5555")
    print("")
    print("  Canaux Telegram configurés:")
    for name, channel_id in TELEGRAM_CHANNELS.items():
        print(f"    - {name.capitalize()}: {channel_id}")
    print("")
    print("=" * 60)
    print("")
    
    app.run(host='0.0.0.0', port=5555, debug=False)
