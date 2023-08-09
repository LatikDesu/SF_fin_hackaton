import logging

import pygsheets
from utils import (create_result_document, get_raw_data, get_sheet_data,
                   update_data, update_result_document, update_table_data)

logging.basicConfig(level=logging.INFO)

gc = pygsheets.authorize(client_secret='client_secret.json')

# Open spreadsheet and then worksheet
url = input('Введите url таблицы:')
sh = gc.open_by_url(url)
filename = sh.title

logging.info(f'Получаем данные из файла: {filename}')
raw_data = get_raw_data(sh[0])

logging.info(f'Открываем файл с результатами: {filename}_result')
try:
    result_sh = gc.open(f'{filename}_result')
    logging.info(f'Opened spreadsheet with id: {result_sh.id} and url: {result_sh.url}')
    logging.info(f'Получаем данные из файла: {filename}_result')
    table1_data, table2_data = get_sheet_data(result_sh)

    logging.info(f'Проверяем на новые записи в таблице')
    table1_data, table2_data = update_data(raw_data, table1_data, table2_data)

    logging.info(f'Обновляем данные в таблице 1')
    table1_data = update_table_data(table1_data, raw_data, 1)

    logging.info(f'Обновляем данные в таблице 2')
    table2_data = update_table_data(table2_data, raw_data, 2)

    logging.info(f'Обновляем результаты в файл {filename}_result')
    update_result_document(result_sh, table1_data, table2_data)

except pygsheets.SpreadsheetNotFound as error:
    logging.info(f'Spreadsheet with title "{filename}_results" does not exist.')
    result_sh = gc.create(f'{filename}_result')

    logging.info(f'Создаем файл с результатами: {filename}_result')
    create_result_document(result_sh, raw_data)

    logging.info(f'Готово!')

