import React from 'react';

const TradabotPrototype = () => {
  return (
    <div style={{ background: 'linear-gradient(135deg, #1E1540 0%, #2B1F5C 100%)', minHeight: '100vh', padding: '20px' }}>
      <iframe 
        src="/tradabot-prototype.html" 
        style={{ 
          width: '100%', 
          height: '100vh', 
          border: 'none',
          borderRadius: '15px'
        }}
        title="TRADABOT Desktop Prototype"
      />
    </div>
  );
};

export default TradabotPrototype;
