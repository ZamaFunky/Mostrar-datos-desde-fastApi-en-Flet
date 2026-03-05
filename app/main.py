import flet as ft
from flet import Colors
from app.home import list_products, get_product, create_product, update_product, delete_product
from app.components.error import ApiError

def main(page: ft.Page):
    page.title = "Inventario - Gestión de Productos"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    
    # Variables para almacenar datos
    product_id_input = ft.TextField(hint_text="Ingrese ID", width=150)
    product_name_input = ft.TextField(hint_text="Nombre del producto", width=250)
    product_price_input = ft.TextField(hint_text="Precio", width=150, keyboard_type=ft.KeyboardType.NUMBER)
    product_stock_input = ft.TextField(hint_text="Cantidad", width=150, keyboard_type=ft.KeyboardType.NUMBER)
    status_text = ft.Text(size=14)
    
    # Lista de productos
    products_list = ft.ListView(expand=True, spacing=5)
    
    def show_message(msg, is_error=True):
        status_text.value = msg
        status_text.color = Colors.RED if is_error else Colors.GREEN
        page.update()
    
    def load_products(e=None):
        try:
            products = list_products()
            products_list.controls.clear()
            
            if isinstance(products, list):
                for product in products:
                    products_list.controls.append(
                        ft.Container(
                            content=ft.Column([
                                ft.Text(f"ID: {product.get('id', 'N/A')}", weight=ft.FontWeight.BOLD),
                                ft.Text(f"Nombre: {product.get('name', 'N/A')}"),
                                ft.Text(f"Precio: ${product.get('price', 0)}"),
                                ft.Text(f"Stock: {product.get('stock', 0)}"),
                            ]),
                            padding=10,
                            border=ft.border.all(1, Colors.OUTLINE),
                            margin=5,
                            border_radius=5
                        )
                    )
            else:
                products_list.controls.append(
                    ft.Text("No hay productos disponibles")
                )
            
            show_message("Productos cargados correctamente", False)
            page.update()
        except Exception as e:
            show_message(f"Error al cargar productos: {str(e)}")
    
    def search_product(e):
        product_id = product_id_input.value
        if not product_id:
            show_message("Por favor ingrese un ID de producto")
            return
        
        try:
            product = get_product(product_id)
            show_message(f"Producto encontrado: {product.get('name', 'N/A')}", False)
            page.update()
        except Exception as e:
            show_message(f"Error: {str(e)}")
    
    def add_product(e):
        name = product_name_input.value
        price = product_price_input.value
        stock = product_stock_input.value
        
        if not name or not price or not stock:
            show_message("Por favor complete todos los campos")
            return
        
        try:
            data = {
                "name": name,
                "price": float(price),
                "stock": int(stock)
            }
            result = create_product(data)
            show_message(f"Producto creado: {result.get('name', name)}", False)
            product_name_input.value = ""
            product_price_input.value = ""
            product_stock_input.value = ""
            load_products()
        except Exception as e:
            show_message(f"Error al crear producto: {str(e)}")
    
    def edit_product(e):
        product_id = product_id_input.value
        name = product_name_input.value
        price = product_price_input.value
        stock = product_stock_input.value
        
        if not product_id:
            show_message("Por favor ingrese el ID del producto")
            return
        
        try:
            data = {}
            if name:
                data["name"] = name
            if price:
                data["price"] = float(price)
            if stock:
                data["stock"] = int(stock)
            
            result = update_product(product_id, data)
            show_message(f"Producto actualizado: {result.get('name', 'N/A')}", False)
            load_products()
        except Exception as e:
            show_message(f"Error al actualizar: {str(e)}")
    
    def remove_product(e):
        product_id = product_id_input.value
        if not product_id:
            show_message("Por favor ingrese el ID del producto a eliminar")
            return
        
        try:
            delete_product(product_id)
            show_message(f"Producto eliminado correctamente", False)
            product_id_input.value = ""
            load_products()
        except Exception as e:
            show_message(f"Error al eliminar: {str(e)}")
    
    # Título
    page.add(
        ft.Text("Gestión de Productos - Inventario", size=24, weight=ft.FontWeight.BOLD),
        ft.Divider(),
    )
    
    # Campos de entrada
    page.add(
        ft.Row([
            ft.Text("ID Producto:", width=120),
            product_id_input,
            ft.Button("Buscar", on_click=search_product),
            ft.Button("Eliminar", on_click=remove_product, bgcolor=Colors.RED),
        ]),
        ft.Row([
            ft.Text("Nombre:", width=120),
            product_name_input,
        ]),
        ft.Row([
            ft.Text("Precio:", width=120),
            product_price_input,
            ft.Text("Stock:", width=80),
            product_stock_input,
        ]),
        ft.Row([
            ft.Button("Agregar Producto", on_click=add_product, bgcolor=Colors.GREEN),
            ft.Button("Actualizar Producto", on_click=edit_product, bgcolor=Colors.BLUE),
            ft.Button("Cargar Productos", on_click=load_products, bgcolor=Colors.ORANGE),
        ]),
        ft.Divider(),
        ft.Text("Productos:", size=18, weight=ft.FontWeight.BOLD),
        ft.Container(
            content=products_list,
            height=300,
            border=ft.border.all(1, Colors.OUTLINE),
            padding=10,
        ),
        ft.Divider(),
        status_text,
    )
    
    # Cargar productos al iniciar
    load_products()

if __name__ == "__main__":
    ft.app(target=main)
