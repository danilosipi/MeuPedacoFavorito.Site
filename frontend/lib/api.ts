export const api = (path: string, opts?: RequestInit) => {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';
  
  // Extrai o tenant do path do browser, se disponível
  const tenant = window.location.pathname.split('/')[2] || 'demo';

  const headers = {
    'Content-Type': 'application/json',
    'X-Tenant': tenant,
    ...opts?.headers,
  };

  return fetch(apiUrl + path, {
    ...opts,
    headers,
  });
}
