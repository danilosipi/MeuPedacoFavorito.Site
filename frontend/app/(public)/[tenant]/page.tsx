'use client';
import { useEffect, useState } from 'react';

export default function PublicSite({ params }: { params: { tenant: string } }) {
  const [tenant, setTenant] = useState('');

  useEffect(() => {
    setTenant(params.tenant);
  }, [params.tenant]);
  
  return (
    <main style={{ padding: 24, fontFamily: 'sans-serif' }}>
      <h2 style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>
        Loja Pública — <span style={{ color: '#1976d2' }}>{tenant}</span>
      </h2>
      <p>Site público com a lista de sabores e botão de comprar.</p>
      {/* Pizza editor component would go here */}
    </main>
  );
}
