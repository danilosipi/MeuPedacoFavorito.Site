export default function Page() {
  return (
    <main style={{ padding: 24, fontFamily: 'sans-serif' }}>
      <header style={{ borderBottom: '1px solid #eee', paddingBottom: 16, marginBottom: 24 }}>
        <h1 style={{ fontSize: '2rem', fontWeight: 'bold' }}>Meu Pedaço Favorito 🍕</h1>
      </header>
      <p style={{ fontSize: '1.1rem', color: '#333' }}>
        A plataforma SaaS para pizzarias venderem por pedaço.
      </p>
      <div style={{ marginTop: 32, display: 'flex', gap: 16 }}>
        <a href="/public/demo" style={{ textDecoration: 'none', color: '#0070f3' }}>Ver Loja Demo</a>
        <a href="/client/demo" style={{ textDecoration: 'none', color: '#0070f3' }}>Acessar Painel Demo</a>
        <a href="/admin" style={{ textDecoration: 'none', color: '#0070f3' }}>Painel Superadmin</a>
      </div>
    </main>
  );
}
