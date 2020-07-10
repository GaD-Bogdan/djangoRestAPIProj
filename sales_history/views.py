from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser

from .api_sales_history import Sales_History


class SaleView(APIView):
    """
    Класс SaleView для работы с API

    Методы:
        get: Возращает файл csv с 5 покупаталями, потратившими наибольшее
    кол-во денег
        post: Передать файл csv с новой историей продаж для обработки
    """
    parser_classes = [FileUploadParser]

    def get(self, request):
        #Sale_record.objects.all().delete()
        #response = {'response': 'ok'}
        # получаем 5 покупателей, потративших больше всего денег
        response = Sales_History.get_5_customers()
        return Response(response, status=200)

    def post(self, request, filename, format=None):
        if 'file' in request.data:
            sale_record_file = request.data['file'].read()
            status = Sales_History.save_data_to_db(sale_record_file)
        else:
            status = {"Status": """Eror, Desc: Файл не получен, в запросе ожидается файл"""}
        return Response(status, status=200)
