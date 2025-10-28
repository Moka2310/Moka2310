import React from 'react';

const TradabotPrototype = () => {
  return (
    <div style={{ 
      background: 'linear-gradient(135deg, #1E1540 0%, #2B1F5C 100%)', 
      minHeight: '100vh', 
      padding: '20px',
      fontFamily: 'Segoe UI, Tahoma, Geneva, Verdana, sans-serif',
      color: 'white'
    }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto', background: '#1E1540', borderRadius: '15px', boxShadow: '0 20px 60px rgba(0, 0, 0, 0.5)', overflow: 'hidden' }}>
        
        {/* Title Bar */}
        <div style={{ background: 'linear-gradient(135deg, #FF1493 0%, #9B59B6 100%)', padding: '15px 20px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
            <div style={{ fontSize: '24px', fontWeight: 'bold', display: 'flex', alignItems: 'center', gap: '10px' }}>
              🤖 TRADABOT
              <div style={{ width: '12px', height: '12px', borderRadius: '50%', background: '#00FF00', animation: 'pulse 2s infinite' }}></div>
            </div>
            <div style={{ fontSize: '12px', opacity: 0.8 }}>v1.0.0 | MT4 Connecté</div>
          </div>
          <div style={{ display: 'flex', gap: '10px' }}>
            <button style={{ width: '35px', height: '35px', border: 'none', borderRadius: '50%', background: 'rgba(255, 255, 255, 0.2)', cursor: 'pointer' }}>_</button>
            <button style={{ width: '35px', height: '35px', border: 'none', borderRadius: '50%', background: 'rgba(255, 255, 255, 0.2)', cursor: 'pointer' }}>□</button>
            <button style={{ width: '35px', height: '35px', border: 'none', borderRadius: '50%', background: 'rgba(255, 255, 255, 0.2)', cursor: 'pointer' }}>✕</button>
          </div>
        </div>

        {/* Main Content */}
        <div style={{ display: 'flex', height: '700px' }}>
          
          {/* Sidebar */}
          <div style={{ width: '250px', background: 'rgba(43, 31, 92, 0.5)', padding: '20px', borderRight: '1px solid rgba(255, 20, 147, 0.3)' }}>
            <div style={{ padding: '15px', margin: '10px 0', borderRadius: '10px', background: 'linear-gradient(135deg, #FF1493 0%, #9B59B6 100%)', display: 'flex', alignItems: 'center', gap: '12px', fontSize: '14px', cursor: 'pointer' }}>
              <span style={{ fontSize: '20px' }}>📊</span> Dashboard
            </div>
            <div style={{ padding: '15px', margin: '10px 0', borderRadius: '10px', display: 'flex', alignItems: 'center', gap: '12px', fontSize: '14px', cursor: 'pointer' }}>
              <span style={{ fontSize: '20px' }}>⚙️</span> Configuration
            </div>
            <div style={{ padding: '15px', margin: '10px 0', borderRadius: '10px', display: 'flex', alignItems: 'center', gap: '12px', fontSize: '14px', cursor: 'pointer' }}>
              <span style={{ fontSize: '20px' }}>📈</span> Positions
            </div>
            <div style={{ padding: '15px', margin: '10px 0', borderRadius: '10px', display: 'flex', alignItems: 'center', gap: '12px', fontSize: '14px', cursor: 'pointer' }}>
              <span style={{ fontSize: '20px' }}>📜</span> Historique
            </div>
            <div style={{ padding: '15px', margin: '10px 0', borderRadius: '10px', display: 'flex', alignItems: 'center', gap: '12px', fontSize: '14px', cursor: 'pointer' }}>
              <span style={{ fontSize: '20px' }}>📝</span> Logs
            </div>
            <div style={{ padding: '15px', margin: '10px 0', borderRadius: '10px', display: 'flex', alignItems: 'center', gap: '12px', fontSize: '14px', cursor: 'pointer' }}>
              <span style={{ fontSize: '20px' }}>📡</span> Canaux Telegram
            </div>
            <div style={{ padding: '15px', margin: '10px 0', borderRadius: '10px', display: 'flex', alignItems: 'center', gap: '12px', fontSize: '14px', cursor: 'pointer' }}>
              <span style={{ fontSize: '20px' }}>🔧</span> Paramètres
            </div>
          </div>

          {/* Content */}
          <div style={{ flex: 1, padding: '30px', overflowY: 'auto' }}>
            
            {/* Stats */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '20px', marginBottom: '30px' }}>
              <div style={{ background: 'linear-gradient(135deg, rgba(255, 20, 147, 0.2) 0%, rgba(155, 89, 182, 0.2) 100%)', padding: '20px', borderRadius: '15px', border: '1px solid rgba(255, 20, 147, 0.3)' }}>
                <div style={{ fontSize: '12px', color: 'rgba(255, 255, 255, 0.7)', marginBottom: '8px' }}>Profit du Jour</div>
                <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#00FF00' }}>+234.50 $</div>
              </div>
              <div style={{ background: 'linear-gradient(135deg, rgba(255, 20, 147, 0.2) 0%, rgba(155, 89, 182, 0.2) 100%)', padding: '20px', borderRadius: '15px', border: '1px solid rgba(255, 20, 147, 0.3)' }}>
                <div style={{ fontSize: '12px', color: 'rgba(255, 255, 255, 0.7)', marginBottom: '8px' }}>Profit Total</div>
                <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#00FF00' }}>+1,245.80 $</div>
              </div>
              <div style={{ background: 'linear-gradient(135deg, rgba(255, 20, 147, 0.2) 0%, rgba(155, 89, 182, 0.2) 100%)', padding: '20px', borderRadius: '15px', border: '1px solid rgba(255, 20, 147, 0.3)' }}>
                <div style={{ fontSize: '12px', color: 'rgba(255, 255, 255, 0.7)', marginBottom: '8px' }}>Win Rate</div>
                <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#00FF00' }}>73.5%</div>
              </div>
              <div style={{ background: 'linear-gradient(135deg, rgba(255, 20, 147, 0.2) 0%, rgba(155, 89, 182, 0.2) 100%)', padding: '20px', borderRadius: '15px', border: '1px solid rgba(255, 20, 147, 0.3)' }}>
                <div style={{ fontSize: '12px', color: 'rgba(255, 255, 255, 0.7)', marginBottom: '8px' }}>Positions Ouvertes</div>
                <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#00FF00' }}>3</div>
              </div>
            </div>

            {/* Positions Section */}
            <div style={{ background: 'rgba(43, 31, 92, 0.5)', padding: '25px', borderRadius: '15px', marginBottom: '20px', border: '1px solid rgba(255, 20, 147, 0.3)' }}>
              <div style={{ fontSize: '18px', fontWeight: 'bold', marginBottom: '20px' }}>📈 Positions Ouvertes (3)</div>
              
              <div style={{ background: 'rgba(30, 21, 64, 0.5)', padding: '15px', borderRadius: '10px', marginBottom: '10px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', border: '1px solid rgba(255, 255, 255, 0.1)' }}>
                <div style={{ display: 'flex', gap: '20px', alignItems: 'center' }}>
                  <span style={{ fontWeight: 'bold', fontSize: '16px', color: '#FF1493' }}>XAUUSD</span>
                  <span style={{ padding: '4px 12px', borderRadius: '20px', fontSize: '12px', fontWeight: 'bold', background: 'rgba(0, 255, 0, 0.2)', color: '#00FF00' }}>BUY</span>
                  <span>0.10 lot</span>
                  <span>Entry: 2043.50</span>
                  <span>SL: 2030.00</span>
                  <span>TP: 2055.00</span>
                </div>
                <div style={{ fontSize: '18px', fontWeight: 'bold', color: '#00FF00' }}>+87.50 $</div>
              </div>

              <div style={{ background: 'rgba(30, 21, 64, 0.5)', padding: '15px', borderRadius: '10px', marginBottom: '10px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', border: '1px solid rgba(255, 255, 255, 0.1)' }}>
                <div style={{ display: 'flex', gap: '20px', alignItems: 'center' }}>
                  <span style={{ fontWeight: 'bold', fontSize: '16px', color: '#FF1493' }}>EURUSD</span>
                  <span style={{ padding: '4px 12px', borderRadius: '20px', fontSize: '12px', fontWeight: 'bold', background: 'rgba(255, 68, 68, 0.2)', color: '#FF4444' }}>SELL</span>
                  <span>0.05 lot</span>
                  <span>Entry: 1.0850</span>
                  <span>SL: 1.0880</span>
                  <span>TP: 1.0800</span>
                </div>
                <div style={{ fontSize: '18px', fontWeight: 'bold', color: '#00FF00' }}>+32.00 $</div>
              </div>

              <div style={{ background: 'rgba(30, 21, 64, 0.5)', padding: '15px', borderRadius: '10px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', border: '1px solid rgba(255, 255, 255, 0.1)' }}>
                <div style={{ display: 'flex', gap: '20px', alignItems: 'center' }}>
                  <span style={{ fontWeight: 'bold', fontSize: '16px', color: '#FF1493' }}>BTCUSD</span>
                  <span style={{ padding: '4px 12px', borderRadius: '20px', fontSize: '12px', fontWeight: 'bold', background: 'rgba(0, 255, 0, 0.2)', color: '#00FF00' }}>BUY</span>
                  <span>0.02 lot</span>
                  <span>Entry: 67,430</span>
                  <span style={{ background: 'rgba(255, 165, 0, 0.3)', padding: '2px 8px', borderRadius: '5px', fontSize: '11px' }}>🔒 BREAKEVEN</span>
                </div>
                <div style={{ fontSize: '18px', fontWeight: 'bold', color: '#00FF00' }}>+54.20 $</div>
              </div>
            </div>

            {/* Logs Section */}
            <div style={{ background: 'rgba(43, 31, 92, 0.5)', padding: '25px', borderRadius: '15px', marginBottom: '20px', border: '1px solid rgba(255, 20, 147, 0.3)' }}>
              <div style={{ fontSize: '18px', fontWeight: 'bold', marginBottom: '20px' }}>📡 Derniers Signaux Reçus</div>
              
              <div style={{ background: 'rgba(0, 0, 0, 0.3)', padding: '15px', borderRadius: '10px', maxHeight: '200px', overflowY: 'auto', fontFamily: 'Courier New, monospace', fontSize: '12px' }}>
                <div style={{ padding: '5px 0', borderBottom: '1px solid rgba(255, 255, 255, 0.1)' }}>
                  <span style={{ color: 'rgba(255, 255, 255, 0.5)' }}>[13:42:15]</span>{' '}
                  <span style={{ color: '#00FF00' }}>✅ Signal exécuté:</span>{' '}
                  <span>BUY XAUUSD @2043.50, TP1: 2047, TP2: 2055, SL: 2030</span>
                </div>
                <div style={{ padding: '5px 0', borderBottom: '1px solid rgba(255, 255, 255, 0.1)' }}>
                  <span style={{ color: 'rgba(255, 255, 255, 0.5)' }}>[13:35:22]</span>{' '}
                  <span style={{ color: '#1E90FF' }}>ℹ️ Signal reçu canal Forex:</span>{' '}
                  <span>BUY XAUUSD @2043.50</span>
                </div>
                <div style={{ padding: '5px 0', borderBottom: '1px solid rgba(255, 255, 255, 0.1)' }}>
                  <span style={{ color: 'rgba(255, 255, 255, 0.5)' }}>[13:28:41]</span>{' '}
                  <span style={{ color: '#00FF00' }}>✅ Position fermée:</span>{' '}
                  <span>SELL EURUSD profit: +45.30 $</span>
                </div>
                <div style={{ padding: '5px 0', borderBottom: '1px solid rgba(255, 255, 255, 0.1)' }}>
                  <span style={{ color: 'rgba(255, 255, 255, 0.5)' }}>[13:15:03]</span>{' '}
                  <span style={{ color: '#1E90FF' }}>🔒 Breakeven activé:</span>{' '}
                  <span>BTCUSD SL déplacé à breakeven</span>
                </div>
              </div>
            </div>

            {/* Canaux Section */}
            <div style={{ background: 'rgba(43, 31, 92, 0.5)', padding: '25px', borderRadius: '15px', border: '1px solid rgba(255, 20, 147, 0.3)' }}>
              <div style={{ fontSize: '18px', fontWeight: 'bold', marginBottom: '20px' }}>📡 Canaux Telegram Surveillés</div>
              
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '15px' }}>
                {['Forex', 'Crypto', 'Gold', 'Indices', 'Actions', 'Commodités'].map((canal, index) => (
                  <div key={index} style={{ background: 'rgba(0, 255, 0, 0.1)', padding: '15px', borderRadius: '10px', border: '1px solid rgba(0, 255, 0, 0.3)' }}>
                    <div style={{ fontWeight: 'bold', marginBottom: '5px' }}>🔗 {canal}</div>
                    <div style={{ fontSize: '12px', color: '#00FF00' }}>✅ Actif | {Math.floor(Math.random() * 10) + 3} signaux</div>
                  </div>
                ))}
              </div>
            </div>

          </div>
        </div>
      </div>

      <div style={{ textAlign: 'center', marginTop: '30px', color: 'rgba(255, 255, 255, 0.5)' }}>
        <p>🎨 PROTOTYPE INTERFACE TRADABOT DESKTOP</p>
        <p style={{ fontSize: '12px' }}>Design concept pour application Windows/Mac</p>
      </div>
    </div>
  );
};

export default TradabotPrototype;
