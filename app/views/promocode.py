from app.views import *
from openpyxl import Workbook
from django.contrib import messages
from app.services.promocode_service import *

async def export_promo_codes_view(request):

    # Создаем новый Excel файл
    wb = Workbook()
    ws = wb.active
    ws.title = "Promokodlar"

    # Записываем заголовки
    ws.append(["Kod", "Yaratilgan sanasi", "Ishlatilgan?"])

    # Записываем данные
    async for promo_code in promocodes_all():
        ws.append([promo_code.code, promo_code.created_at, promo_code.used])

    # Подготавливаем HTTP ответ с Excel файлом
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=promo_codes.xlsx'
    wb.save(response)
    return response

async def generate_promo_codes_view(request):
    if request.method == 'POST':
        number_of_codes = int(request.POST.get('number_of_codes', 10))
        code_length = int(request.POST.get('code_length', 10))
        codes_list = [
            ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(code_length))
            for _ in range(number_of_codes) 
        ]
        await create_promocodes(codes_list)
            
        messages.success(request, f'{number_of_codes} ta promokodlar muvaffaqiyatli yaratildi')
        return redirect('admin:app_promocode_changelist')
    else:
        return redirect('admin:app_promocode_changelist')