 #app/services/transacciones_api_productos.py
import requests
import uuid
from app.components.error import ApiError

BASE ="http://localhost:8000/products"
TIME_OUT=10

MOCK_MODE = True  # Toggle False for real backend
_local_products = [
    {"id": "1", "name": "Laptop Demo", "quantity": 10, "ingreso_date": "2024-01-01", "min_stock": 1, "max_stock": 100},
    {"id": "2", "name": "Mouse Demo", "quantity": 20, "ingreso_date": "2024-01-02", "min_stock": 0, "max_stock": 50},
]

#Obtiene la lista de productos de FastAPI
def list_products(limit:int=20, offset:int=0) -> dict:
    if MOCK_MODE:
        total = len(_local_products)
        items = _local_products[offset:offset + limit]
        return {"total": total, "items": items}
    try:
        #request.get se conecta al api y entrega la información en r
        r=requests.get(f"{BASE}/", params={"limit":limit, "offset":offset}, timeout=TIME_OUT)
        #si el status_code es cualquier código 200 se entrega el resultado en formato json
        if 200 <= r.status_code < 300:
            return r.json() if r.content else {}
        raise ValueError(f"Error {r.status_code}", r.status_code, r.text)
    except requests.exceptions.RequestException as e:
        raise ValueError("Error de conexión", None, str(e))

#Obtiene el productos con el id que se le pasa como parametro
def get_product(product_id:str) -> dict:
    if MOCK_MODE:
        for p in _local_products:
            if p.get("id") == product_id:
                return p
        return {}
    try:
        r=requests.get(f"{BASE}/{product_id}", timeout=TIME_OUT)
        if 200 <= r.status_code < 300:
            return r.json() if r.content else {}
        raise ValueError(f"Error {r.status_code}", r.status_code, r.text)
    except requests.exceptions.RequestException as e:
        raise ValueError("Error de conexión", None, str(e))

#Crea un producto nuevo con los datos que se le pasan como parametro en un diccionario
def create_product(data:dict)->dict:
    if MOCK_MODE:
        data["id"] = str(uuid.uuid4())[:8]
        _local_products.append(data)
        return data
    try:
        r=requests.post(f"{BASE}/", json=data, timeout=TIME_OUT)
        if 200 <= r.status_code < 300:
            return r.json() if r.content else {}
        raise ValueError(f"Error {r.status_code}", r.status_code, r.text)
    except requests.exceptions.RequestException as e:
        raise ValueError("Error de conexión", None, str(e))

#Actualiza el producto que se le indica con el id y los datos nuevos en un diccionario
def update_product(product_id:str, data:dict)->dict:
    if MOCK_MODE:
        for p in _local_products:
            if p.get("id") == product_id:
                p.update(data)
                return p
        raise ValueError(f"Producto {product_id} no encontrado")
    try:
        r=requests.put(f"{BASE}/{product_id}", json=data, timeout=TIME_OUT)
        if r.status_code >= 400:
            try:
                payload = r.json()
                detail=payload.get("error") or payload.get("detail") or r.text
            except Exception:
                detail = r.text
            raise ApiError(detail, r.status_code)
            
        return r.json()
    except requests.Timeout:
        raise ApiError("El servidor tardó demasiado en responder",0)
    except requests.ConnectionError:
        raise ApiError("No se pudo conectar al servidor",0)
    except requests.RequestException as e:
        raise ApiError(f"Error de red {str(e)}",0)

#Borra el producto que se le indica con el id
def delete_product(product_id:str):
    if MOCK_MODE:
        global _local_products
        _local_products = [p for p in _local_products if p.get("id") != product_id]
        return {"deleted": True}
    try:
        r=requests.delete(f"{BASE}/{product_id}", timeout=TIME_OUT)
        if 200 <= r.status_code < 300:
            return r.json() if r.content else {}
        raise ValueError(f"Error {r.status_code}", r.status_code, r.text)
    except requests.exceptions.RequestException as e:
        raise ValueError("Error de conexión", None, str(e))

#ejecutar así:

# Ejecuta el proyecto del backend (proyecto inventario) así:
# uvicorn app.main:app --reload

# Test code removed to prevent execution on import.
# Run backend: uvicorn app.main:app --reload (in backend project)
# Test API: python -c "from app.service.transacciones_api_productos import list_products; print(list_products())"
