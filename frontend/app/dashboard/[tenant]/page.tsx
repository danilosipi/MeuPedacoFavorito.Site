'use client';
import { useEffect, useState } from 'react';

export default function Client({ params }: { params: { tenant: string } }) {
  const [tenant, setTenant] = useState('');

  useEffect(() => {
    setTenant(params.tenant);
  }, [params.tenant]);

  return (
    <main style={{ padding: 24, fontFamily: 'sans-serif' }}>
      <h2 style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>
        Painel da Pizzaria: <span style={{ color: '#e91e63' }}>{tenant}</span>
      </h2>
      <p>Aqui o dono da pizzaria gerencia seu CRUD de sabores, horários, promoções, etc.</p>
    </main>
  );
}
