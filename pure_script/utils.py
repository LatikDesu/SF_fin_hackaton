import datetime

import pygsheets

gc = pygsheets.authorize(client_secret='client_secret.json')
today = datetime.date.today().strftime('%d.%m.%Y')


def check_url(cls, url):
    try:
        sh = gc.open_by_url(url)
        return True
    except:
        return False


def get_raw_data(sheet):
    fio = sheet.get_col(6, include_tailing_empty=False)
    id_cell = sheet.get_col(35, include_tailing_empty=False)
    date_ych = sheet.get_col(12, include_tailing_empty=False)
    month_ych = sheet.get_col(15, include_tailing_empty=False)

    raw_data = {key: [value1, value2, value3]
                for key, value1, value2, value3
                in zip(id_cell, fio, date_ych, month_ych)}

    del raw_data['Уникальный номер размещения']

    return raw_data


def get_sheet_data(sheet):
    wks1 = sheet.worksheet_by_title("table 1")
    wks2 = sheet.worksheet_by_title("table 2")
    num_cols = len(wks1.get_row(1, include_tailing_empty=False))

    table1 = wks1.get_all_values(include_tailing_empty_rows=False)
    table2 = wks2.get_all_values(include_tailing_empty_rows=False)

    return (
        [row[:num_cols] for row in table1],
        [row[:num_cols] for row in table2]
    )


def update_data(raw_data, table1_data, table2_data):
    for key in raw_data:
        if any(key in sublist for sublist in table1_data):
            continue
        else:
            table1_data.append([raw_data[key][0], key])
            table1_data[-1].extend([''] * (len(table1_data[0])-2))
            table2_data.append([raw_data[key][0], key])
            table2_data[-1].extend([''] * (len(table2_data[0])-2))

    return table1_data, table2_data


def update_table_data(table_data, raw_data, x):
    table_data[0].append(today)

    for entity in raw_data:
        for i, sublist in enumerate(table_data):
            if entity in sublist:
                if raw_data[entity][x] not in table_data[i]:
                    table_data[i].append(raw_data[entity][x])
                else:
                    table_data[i].append('')

    return table_data


def create_result_document(sheet, raw_data):
    wks1 = sheet.add_worksheet("table 1")
    wks1.update_value('A1', 'ФИО/Название подрядчика')
    wks1.update_value('B1', 'Уникальный номер размещения')
    wks1.update_value('C1', today)
    wks1.update_values('A2', [[fio, id, data1] for id, (fio, data1, data2) in raw_data.items()])

    wks2 = sheet.add_worksheet("table 2")
    wks2.update_value('A1', 'ФИО/Название подрядчика')
    wks2.update_value('B1', 'Уникальный номер размещения')
    wks2.update_value('C1', today)
    wks2.update_values('A2', [[fio, id, data2] for id, (fio, data1, data2) in raw_data.items()])


def update_result_document(sheet, table1_data, table2_data):
    wks1 = sheet.worksheet_by_title("table 1")
    wks2 = sheet.worksheet_by_title("table 2")

    wks1.update_values('A1', table1_data)
    wks2.update_values('A1', table2_data)
