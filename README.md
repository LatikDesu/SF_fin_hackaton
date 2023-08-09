## Техническое задание
Заказчику (сотруднику отдела финансов) необходимо автоматизировать его рутинную работу с таблицей, а именно: брать при необходимости данные из исходной таблицы и на их основе формировать два отчета в виде таблиц и актуализировать данные отчеты в случае добавления/изменения данных в исходной таблице.

## Вводные данные
На вход программе подается гугл таблица, в которой записи уникальны по столбцу «Уникальный номер размещения»‎.
Ссылка на тестовую таблицу: https://docs.google.com/spreadsheets/d/1uLz23xjF9w5jvROO9TwjOEk1Pv7zGq67M4U8aG8gqrE/edit?usp=sharing

## Задача
Отслеживать изменения для каждого «уникального размещения»‎ (уникальной записи/строки) из столбца «Месяц учета оказания услуг» (подсвечен желтым) и «Дата учета оказания услуг»‎ в исходной таблице и выполнять следующие действия:
3.1. Формировать отчеты в виде файла, состоящего из двух таблиц.
3.2. Если в исходной таблице появились новые уникальные размещения или изменились значения в столбцах «Месяц учета оказания услуг»‎ и «Дата учета оказания услуг»‎ у старых записей, то обновить таблицы в отчете.

## Запуск
1. Получите учетные данные OAuth2 из Google Developers Console для google spreadsheet api и drive api и сохраните файл client_secret.json в том же каталоге, что и проект.
   <br>Инструкция: https://pygsheets.readthedocs.io/en/latest/authorization.html
2. Установить виртуальное окружение и необходимые библиотеки:
    ```
        pip install requirements.txt
    ```
3. Запустить проект:
    ```
        flet fletApp.py
    ```

## Реализация
Программа реализована в виде Flet-приложения. На вход подается ссылка на гугл-таблицу, на выходе - выдается ссылка на таблицу с результатами. Есть возможность задеплоить проект как десктопное приложение через pyinstaller.

### Основное окно
<p float="left">
  <img src="https://github.com/LatikDesu/SF_fin_hackaton/blob/master/assets/Start_screen.jpg" width="33%" />
  <img src="https://github.com/LatikDesu/SF_fin_hackaton/blob/master/assets/Result_empty.jpg" width="33%" />
  <img src="https://github.com/LatikDesu/SF_fin_hackaton/blob/master/assets/Result_all.jpg" width="33%" />
</p>

### Результат
<p float="left">
  <img src="https://github.com/LatikDesu/SF_fin_hackaton/blob/master/assets/Screenshot%20result_1.jpg" width="45%" />
  <img src="https://github.com/LatikDesu/SF_fin_hackaton/blob/master/assets/Screenshot%20result_2.jpg" width="45%" />
</p>
