import flet as ft
from pygsheets import SpreadsheetNotFound

from Utility import (check_url, create_result_document, gc, get_raw_data,
                     get_sheet_data, update_data, update_result_document,
                     update_table_data)


def main(page: ft.Page):
    page.title = "SkillFactory Finance Hackaton"
    page.padding = 50
    page.window_width = 600
    page.window_height = 600

    page.update()

    def btn_url_check(e):
        if not check_url(url_input.value):
            url_input.error_text = "Некорректный URL"
            page.update()
        else:
            text_view.clean()

            raw_data, filename = get_raw_data(url=url_input.value)
            text_view.controls.append(ft.Text("--> Получены данные из таблицы ..." + filename))
            page.update()

            try:
                result_sh = gc.open(f'{filename}_results')
                text_view.controls.append(ft.Text(f'--> Получаем данные из таблицы: "{filename}_results".'))
                page.update()

                table1_data, table2_data = get_sheet_data(result_sh)
                text_view.controls.append(ft.Text('--> Проверяем на наличие новых записей...'))
                page.update()

                table1_data, table2_data = update_data(raw_data, table1_data, table2_data)
                text_view.controls.append(ft.Text('--> Обновляем данные в таблице 1 ...'))
                page.update()

                table1_data = update_table_data(table1_data, raw_data, 1)
                text_view.controls.append(ft.Text('--> Обновляем данные в таблице 2 ...'))
                page.update()

                table2_data = update_table_data(table2_data, raw_data, 2)
                text_view.controls.append(ft.Text(f'--> Обновляем результаты в файле {filename}_results ...'))
                page.update()

                update_result_document(result_sh, table1_data, table2_data)
                text_view.controls.append(ft.Text('--> Готово!'))
                text_view.controls.append(ft.TextButton(text="Таблица с результатами", url=result_sh.url)),
                page.update()

            except SpreadsheetNotFound:
                text_view.controls.append(ft.Text(f'--> Таблица с названием "{filename}_results" не найдена.'))
                page.update()
                result_sh = gc.create(f'{filename}_results')

                text_view.controls.append(ft.Text(f'--> Создаем таблицу с результатами: {filename}_results'))
                page.update()

                create_result_document(result_sh, raw_data)

                text_view.controls.append(ft.Text('--> Готово!'))
                text_view.controls.append(ft.TextButton(text="Таблица с результатами", url=result_sh.url)),
                page.update()

    url_input = ft.TextField(hint_text="Введите url таблицы", expand=True)

    url_view = ft.Column()
    text_view = ft.Column()

    img = ft.Image(
        src="assets/img.png",
        width=500,
        height=100,
        fit=ft.ImageFit.CONTAIN,
    )

    url_view = ft.Column(
        width=600,
        controls=[
            ft.Row(
                controls=[
                    url_input,
                    ft.FloatingActionButton(icon=ft.icons.CHECK, on_click=btn_url_check),
                ],
            ),
            url_view,
        ],
    )

    text_view = ft.Column(
        width=600,
        controls=[
            ft.Text("1. Введите URL google-таблицы"),
            ft.Text("2. Нажмите кнопку"),
            ft.Text("3. Результаты будут записаны в файл '<имя_таблицы>_results' "),
            ft.Text("4. Если такой файл существует, он будет перезаписан, если нет - он будет создан"),
        ],
    )

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.add(img)
    page.add(url_view)
    page.add(text_view)


ft.app(main)
