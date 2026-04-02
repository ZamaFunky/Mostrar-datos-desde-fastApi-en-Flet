import flet as ft

def show_popup(page: ft.Page, title: str, message: str):
    dlg = ft.AlertDialog(
        title=ft.Text(title),
        content=ft.Text(message),
        actions=[ft.TextButton("OK", on_click=lambda e: page.close_dialog())],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    page.dialog = dlg
    page.show_dialog(dlg)

def close_popup(page: ft.Page):
    page.close_dialog()
