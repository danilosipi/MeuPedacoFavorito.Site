from fastapi import Request, HTTPException, status

def get_tenant_from_request(request: Request) -> str:
    # Estratégia 1: Header (prioridade)
    tenant = request.headers.get("X-Tenant")
    if tenant:
        return tenant

    # Estratégia 2: Path (e.g., /api/client/{tenant}/...)
    path = request.url.path
    parts = [p for p in path.split("/") if p]
    
    # Procura por 'client' ou 'public' e pega o próximo segmento como tenant
    for segment in ["client", "public"]:
        if segment in parts:
            try:
                index = parts.index(segment)
                if index + 1 < len(parts):
                    return parts[index + 1]
            except ValueError:
                continue

    # Fallback para um tenant padrão ou erro
    # Em um sistema real, poderia lançar um erro se o tenant for obrigatório
    # raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tenant could not be identified")
    return "default"
