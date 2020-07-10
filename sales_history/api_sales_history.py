from datetime import datetime

from .models import Sale_record, Item, Customer


class Sales_History():

    """
    Метод анализириует исптори продаж из БД и выбирает 5 покупателей,
    потртивших больше всего денег.

    Возваращет: Список с полем response, со списком из 5 клиентов, каждый
    из которых описан следу.щими полями: username, spent_money, gems
    """
    def get_5_customers():
        # Подготавливем пустые словари для хранения потраченной суммы и
        # купленных предметов
        customer_spent = dict()
        customer_items = dict()
        # Получаем три поля из тиблицы с историей продаж: покупателей, предметы
        # и потраченну сумму
        sale_records = Sale_record.objects.values_list(
            'customer',
            'item',
            'total_spent'
        )
        # проходимся по всем записям в полученных данных
        for sale_record in sale_records:
            # распаковываем данные каждой записи в 3 переменные
            customer, item, total_spent = sale_record
            # если покупатель еще не встерчался, то...
            if customer not in customer_spent:
                # создаем поле с кл.чем = никнеймом покупателя в наших словарях
                customer_spent[customer] = 0
                customer_items[customer] = set()
            # прибавляем сумму текущей покупки к общей сумме покупателя
            customer_spent[customer] += total_spent
            # добавляем купленный предмет к множеству предметов покупателя
            customer_items[customer].add(item)
        # сортируем по потраченным деньгам
        customer_spent = sorted(list(customer_spent.items()),
                    key=lambda i: i[1],
                    reverse=True
        )
        if len(customer_spent) < 5:
            return({"Error": "Недостаточно записей в базе данных"})
        # подготавливаем список для словарей
        response_list = list()
        # проходим по 5 покупателям, потратившим наибольшее кол-во денег
        for i in range(5):
            # распаковываем данные из списка кортежей, полученного после
            # сортировки
            customer, total_spent = customer_spent[i]
            # подготавливаем множетсво камней, совпада.щих с друигими
            # покупателями
            items = set()
            # 4 раза находим пересечение множеств камней других покупателей
            # и объединяем результат с множеством items
            for j in range(5):
                # проводим объединение с множеством камней всех
                # покупателей, кроме
                # текущего
                if j == i:
                    continue
                items |= customer_items[customer] & customer_items[
                    customer_spent[j][0]
                ]

            # получаем название камней из бд по их pk
            items_list = list()
            for i in items:
                items_list.append(Item.objects.get(pk=i).name)

            customer_dict = dict([
                ('username', Customer.objects.get(pk=customer).customer),
                ('spent_money', str(total_spent)),
                ('gems', items_list)
            ])
            response_list.append(customer_dict)
        return {'response': response_list}

    """
    Метод обработки полученного файла и сохранение записей продаж в базу данных

    Принимает: список из строк вида: "customer,item,total,quantity,date"
    """
    def save_data_to_db(sale_record_file):
        sale_records = sale_record_file.decode('utf-8').split("\r\n")
        if len(sale_records) <= 1:
            return {"Status": """Error, Desc: В файле нет не одной записи
или разделители строк не \"\\r\\n\""""}

        headers = sale_records[0].split(',')
        if len(headers) != 5 or headers != ['customer', 'item', 'total',
                                            'quantity', 'date']:
            return {"Status": """Error, Desc: Заголовки полей не верны.
Ожидается: customer,item,total,quantity,date
Получено: {}""".format(sale_records[0])}

        sale_records = sale_records[1:]

        # Список с покупателями, которые уже есть в БД
        customers_db = Customer.objects.all()
        customers = dict((x.customer, x) for x in customers_db)
        # Список с предметами, которые уже есть в БД
        items_db = Item.objects.all()
        items = dict((x.name, x) for x in items_db)
        # Пустой список с данными, подготовленными к отпраке в БД
        db_sale_records_view = list()

        # Проходимся по каждой записи из полученных данных
        for sale_record_str in sale_records:
            if sale_record_str == '':
                break

            sale_record = tuple(sale_record_str.split(','))
            # Получаем каждое отдельное поле
            customer, item, total, quantity, date = sale_record

            # Обработка покупателя
            if customer not in customers: # Если покупатель еще нет в бд, то
                                        # добавляем
                obj = Customer.objects.create(customer=customer)
                customers[customer] = obj

            # Обработка проданнаго предмета аналогично как и с покупателем
            if item not in items:
                obj = Item.objects.create(name=item)
                items[item] = obj

            if not total.isdigit() or not quantity.isdigit():
                return({"Status": """Error, Desc: Строка {}
total = \"{}\" или quantity = \"{}\" не является числом типа int""".format(
                        sale_records.index(sale_record_str)+2,
                        total, quantity)})
            try:
                date = datetime.fromisoformat(date)
            except:
                return({"Status": """Error, Decs: Строка {}
неверный формат времени.
Получено: {}
Ожидается: {}""".format(sale_records.index(sale_record_str)+2,
                        date, "yyyy-mm-dd hh:mm:ss.ssssss")})

            db_sale_record = Sale_record(
                date = date,
                total_spent = int(total),
                quantity = int(quantity),
                item = items[item],
                customer = customers[customer]
            )
            db_sale_records_view.append(db_sale_record)
        Sale_record.objects.bulk_create(db_sale_records_view)
        return {"Status": "OK"}
