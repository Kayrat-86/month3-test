import flet as ft
from datetime import datetime

def main(page: ft.Page):
    page.title = 'Мое первое приложение'
    page.theme_mode = ft.ThemeMode.LIGHT

    greeting_text = ft.Text(value='Hello world')
    greeting_history = []     
    history_text = ft.Text(value="История приветствий:")

    def update_history_list(data):
        if not data:
            history_text.value = "История приветствий:"
        else:
            lines = [
                f"{t.strftime('%y:%m:%d - %H:%M:%S')} - {name}"
                for t, name in data
            ]
            history_text.value = "История приветствий:\n" + "\n".join(lines)

    def on_button_click(_):
        name = name_input.value.strip()
        now = datetime.now()

        if name:
            timestamp_str = now.strftime("%y:%m:%d - %H:%M:%S")
            greeting_text.value = f'{timestamp_str} Hello {name}'
            greeting_text.color = None
            name_input.value = ""

            greeting_history.append((now, name))

            greeting_history[:] = greeting_history[-5:]

            update_history_list(greeting_history)

        else:
            greeting_text.value = 'Введите корректное имя'
            greeting_text.color = ft.Colors.RED

        page.update()

    name_input = ft.TextField(
        label='Введите имя',
        on_submit=on_button_click,
        expand=True
    )
    send_button = ft.ElevatedButton(text='send', on_click=on_button_click)

    def clear_history(_):
        greeting_history.clear()
        update_history_list(greeting_history)
        page.update()

    clear_button = ft.IconButton(icon=ft.Icons.DELETE, on_click=clear_history)

    def show_morning(_):
        filtered = [item for item in greeting_history if item[0].hour < 12]
        update_history_list(filtered)
        page.update()

    def show_evening(_):
        filtered = [item for item in greeting_history if item[0].hour >= 12]
        update_history_list(filtered)
        page.update()

    morning_button = ft.TextButton("Утренние", on_click=show_morning)
    evening_button = ft.TextButton("Вечерние", on_click=show_evening)

    page.add(
        ft.Row([greeting_text], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([name_input, send_button, clear_button]),
        ft.Row([morning_button, evening_button], alignment=ft.MainAxisAlignment.CENTER),
        history_text
    )

ft.app(target=main)