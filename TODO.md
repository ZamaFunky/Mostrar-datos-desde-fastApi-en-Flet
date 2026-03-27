# Fix errors to make project run (Flet + FastAPI client)

## Steps:
1. [ ] Remove trailing test print(list_products()) from app/service/transacciones_api_productos.py (prevents ImportError on import)
2. [ ] Remove all debug print() statements from app/views/mostrar_productos_httpx.py (console noise)
3. [ ] Fix duplicate app/views/mostrar_productos.py: change 'app.services' → 'app.service', remove prints, or delete if unused
4. [ ] Test `python main.py` - should launch Flet app (empty/error if no backend localhost:8000)
5. [x] Test `python main.py` launches ✅

## New: Agregar productos (Mock mode)
6. [ ] service.py: Mock globals + logic in 5 funcs
7. [ ] view.py: Toggle button for MOCK_MODE
8. [ ] Test add/edit product local

Progress updated after each step.

