from fastapi import APIRouter, Request, Depends
from app.main import templates

router = APIRouter()

@router.get("/{store_slug}/menu")
async def store_menu(store_slug: str, request: Request):
    # TODO: buscar store e menu_items via camada de serviço/DAO
    store = {"id": "uuid-da-loja", "name": store_slug.title()}
    menu_items = [
        {"id": "uuid-item-1", "name": "Mussarela", "description": "Clássica",
         "price_slice_cents": 990},
    ]
    return templates.TemplateResponse("menu.html",
                                      {"request": request, "store": store, "menu_items": menu_items})
