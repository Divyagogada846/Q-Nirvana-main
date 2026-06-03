import React from 'react';

const MedAI = () => {
  return (
    <div style={{ width: '100%', height: 'calc(100vh - 80px)', overflow: 'hidden', borderRadius: '12px', background: 'white', border: '1px solid var(--slate-200)' }}>
      <iframe 
        src="http://localhost:5001" 
        title="MedAI Assistant" 
        style={{ width: '100%', height: '100%', border: 'none' }}
      />
    </div>
  );
};

export default MedAI;
