import flet as ft

class ApiError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


def api_error_to_text(error: ApiError):
    return str(error.message)

def show_snackbar(page: ft.Page, title: str, message: str, bgcolor=None):
    snackbar = ft.SnackBar(
        content=ft.Row([
            ft.Text(title, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
            ft.Text(message, color=ft.colors.WHITE),
        ]),
        bgcolor=bgcolor or ft.colors.BLUE,
        duration=ft.duration(seconds=4)
    )
    page.show_snack_bar(snackbar)


