import flet as ft
from app.service.transacciones_api_productos import (
    create_product,
    update_product,
    list_products as listar_productos
)
from app.views.nuevo_editar import formulario_nuevo_editar_producto
from app.components.popup import show_popup, show_snackbar
import app.service.transacciones_api_productos as api_service
from app.styles.estilos import Colors

def products_view(page: ft.Page) -> ft.Control:
    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Cantidad")),
            ft.DataColumn(ft.Text("Ingreso")),
            ft.DataColumn(ft.Text("Min")),
            ft.DataColumn(ft.Text("Max")),
            ft.DataColumn(ft.Text("Acciones")),
        ],
        rows=[]
    )
    async def actualizar_data():
        try:
            data = listar_productos(limit=500, offset=0)
            items = data.get("items", [])
            nuevas_filas = []
            for p in items:
                nuevas_filas.append(
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(p.get("name", ""))),
                        ft.DataCell(ft.Text(str(p.get("quantity", "")))),
                        ft.DataCell(ft.Text(p.get("ingreso_date", "") or "")),
                        ft.DataCell(ft.Text(str(p.get("min_stock", "")))),
                        ft.DataCell(ft.Text(str(p.get("max_stock", "")))),
                        ft.DataCell(
                            ft.Row(
                                controls=[
                                    ft.IconButton(icon=ft.icons.EDIT, tooltip="Editar", on_click=lambda e, p=p: inicio_editar_producto(p)),
                                ]
                            )
                        ),
                    ])
                )
            tabla.rows = nuevas_filas
            page.update()
        except Exception as e:
            page.update()
    def abrir_formulario(producto_existente=None):
        async def procesar_datos(data_capturada: dict):
            try:
                if "id" in data_capturada:
                    product_id = data_capturada["id"]
                    data_sin_id = data_capturada.copy()
                    del data_sin_id["id"]
                    update_product(product_id, data_sin_id)
                    await show_snackbar(page, "Éxito", "Producto actualizado.", bgcolor=Colors.SUCCESS)
                else:
                    create_product(data_capturada)
                    await show_snackbar(page, "Éxito", "Producto creado.", bgcolor=Colors.SUCCESS)
                await actualizar_data()
            except Exception as ex:
                await show_popup(page, "Error", str(ex))
        dlg, open_form, _ = formulario_nuevo_editar_producto(
            page,
            on_submit=procesar_datos,
            initial=producto_existente
        )
        open_form()
    def inicio_editar_producto(p: dict):
        async def editar_producto(data: dict):
            try:
                data_sin_id = data.copy()
                if "id" in data_sin_id:
                    del data_sin_id["id"]
                update_product(p["id"], data_sin_id)
                close_()
                await show_snackbar(page, "Éxito", "Producto actualizado", bgcolor=Colors.SUCCESS)
                await actualizar_data()
            except Exception as ex:
                await show_snackbar(page, "Error", str(ex), bgcolor=Colors.DANGER)
        dlg, open_, close_ = formulario_nuevo_editar_producto(page, on_submit=editar_producto, initial=p)
        open_()
    def toggle_mock(e):
        api_service.MOCK_MODE = not api_service.MOCK_MODE
        page.snack_bar = ft.SnackBar(
            content=ft.Text(f"Modo API: {'Mock ✅' if api_service.MOCK_MODE else 'Real 🔌'}"),
            bgcolor=Colors.INFO
        )
        page.snack_bar.open = True
        page.update()
        page.run_task(actualizar_data())
    btn_nuevo = ft.FilledButton(
        "Nuevo producto",
        icon=ft.icons.ADD,
        on_click=lambda e: abrir_formulario()
    )
    page.run_task(actualizar_data)
    return ft.Column(
        expand=True,
        controls=[
            ft.Row(
                [
                    ft.Text("Inventario", size=25, weight="bold"),
                    ft.IconButton(
                        icon=ft.icons.SCIENCE if api_service.MOCK_MODE else ft.icons.STORAGE,
                        tooltip="Toggle Mock/Real API",
                        on_click=lambda e: toggle_mock(e)
                    ),
                    btn_nuevo
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            ft.Divider(),
            ft.Container(
                content=ft.Container(
                    content=tabla,
                    padding=10,
                    alignment=ft.alignment.center
                ),
                alignment=ft.alignment.center,
                expand=True
            )
        ]
    )
