import flet as ft
from typing import Any

def products_view(page: ft.Page) -> ft.Control:
    # Encabezados
    columnas = [
        ft.DataColumn(label=ft.Text("Nombre")),
        ft.DataColumn(label=ft.Text("Cantidad")),
        ft.DataColumn(label=ft.Text("Ingreso")),
        ft.DataColumn(label=ft.Text("Min")),
        ft.DataColumn(label=ft.Text("Max")),
    ]
    
    # Datos de prueba
    data = []
    data.append(
        ft.DataRow(
            cells=[
                ft.DataCell(ft.Text("nombre1...")),
                ft.DataCell(ft.Text("cantidad1...")),
                ft.DataCell(ft.Text("ingreso1...")),
                ft.DataCell(ft.Text("min1...")),
                ft.DataCell(ft.Text("max1...")),
            ]
        )
    )

    # Se crea la tabla con los encabezados (columnas) y los datos de prueba (data)
    tabla = ft.DataTable(
        columns=columnas,
        rows=data,
        width=900,
        heading_row_height=60,
        data_row_max_height=60,
        data_row_min_height=48
    )

    return tabla
