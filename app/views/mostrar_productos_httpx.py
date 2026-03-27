import flet as ft
from typing import Any

from app.service.transacciones_api_productos import (
    list_products,
    get_product,
    create_product,
    update_product,
    delete_product
)

from app.components.popup import (
    show_popup,
    show_snackbar,
)

from app.components.error import ApiError, api_error_to_text
from app.styles.estilos import Colors

def products_view(page: ft.Page) -> ft.Control:

    # Contador total
    total_text = ft.Text(
        "Total de productos: (cargando...)",
        size=18
    )

    # Columnas
    columnas = [
        ft.DataColumn(label=ft.Text("Nombre")),
        ft.DataColumn(label=ft.Text("Cantidad")),
        ft.DataColumn(label=ft.Text("Ingreso")),
        ft.DataColumn(label=ft.Text("Min")),
        ft.DataColumn(label=ft.Text("Max")),
        ft.DataColumn(label=ft.Text("Acciones")),
    ]

    tabla = ft.DataTable(
        columns=columnas,
        rows=[],
        width=900,
    )

    async def actualizar_data():
        try:
            data = list_products(limit=500, offset=0)
            total_text.value = "Total de productos: " + str(data.get("total", 0))
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
                                    ft.IconButton(icon=ft.Icons.EDIT, tooltip="Editar", on_click=lambda e, p=p: inicio_editar_producto(p)),
                                    # ft.IconButton(icon=ft.Icons.DELETE, tooltip="Borrar", on_click=lambda e, p=p: inicio_borrar_producto(p))
                                ]
                            )
                        )
                    ])
                )
            tabla.rows = nuevas_filas
            page.update()
        except Exception as e:
            page.update()

    async def formulario_nuevo(producto_existente=None):
        async def procesar_datos(data):
            try:
                if "id" in data:
                    product_id = data["id"]
                    data_sin_id = data.copy()
                    del data_sin_id["id"]
                    update_product(product_id, data_sin_id)
                    await show_snackbar(page, "Éxito", "Producto actualizado.", bgcolor=Colors.SUCCESS)
                else:
                    create_product(data)
                    await show_snackbar(page, "Éxito", "Producto creado.", bgcolor=Colors.SUCCESS)
                await actualizar_data()
            except Exception as ex:
                await show_popup(page, "Error", str(ex))

        dlg, open_form, _ = formulario_nuevo_editar_producto(
            page, on_submit=procesar_datos, initial=producto_existente
        )
        open_form()

    ########## Editar producto ##########
    # Esta función se ejecuta al hacer click en el icono "editar"
    def inicio_editar_producto(p: dict[str, Any]):
        async def editar_producto(data: dict):
            try:
                await update_product(p["id"], data)
                close()
                await show_snackbar(page, "Éxito", "Producto actualizado", bgcolor=Colors.SUCCESS)
                await actualizar_data()
            except ApiError as ex:
                await show_popup(page, "Error", api_error_to_text(ex))
            except Exception as ex:
                await show_snackbar(page, "Error", str(ex), bgcolor=Colors.DANGER)

        # dlg: dialogo, open_: función para abrir, close: función para cerrar
        dlg, open_, close = formulario_nuevo_editar_producto(page, on_submit=editar_producto, initial=p)
        open_()

    btn_nuevo = ft.FilledButton(
        "Nuevo producto",
        icon=ft.Icons.ADD,
        on_click=lambda e: formulario_nuevo()
    )

    page.run_task(actualizar_data)

    return ft.Column(
        expand=True,
        controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text("Inventario", size=25, weight="bold"),
                    total_text,
                    btn_nuevo
                ]
            ),
            ft.Divider(),
            ft.Container(
                content=tabla,
                padding=10,
                alignment=ft.alignment.center,
                expand=True,
            )
        ]
    )
