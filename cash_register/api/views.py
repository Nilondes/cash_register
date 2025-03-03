import os
import tempfile
from decimal import Decimal
from io import BytesIO

import pdfkit
import qrcode
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Check, CheckItem, Item, ItemAmount


@api_view(['POST'])
def create_check(request):
    """
    Creates check based on id's and returns QR-code to download the check.

    :param request: HTTP-request, containing list of item id's.
    :return: HttpResponse with QR-code image.
    """

    item_ids = request.data.get('items', [])
    items = Item.objects.filter(id__in=item_ids)
    if not items.exists():
        return Response({"error": "Указанные товары не найдены"},
                        status=status.HTTP_404_NOT_FOUND)

    check = Check.objects.create(total_price=Decimal(0), file_path='')
    total_price = Decimal(0)

    for item in items:
        item_amount = ItemAmount.objects.filter(item=item).first()
        if not item_amount:
            return Response({"error": f"Количество для товара {item.id} не указано"},
                            status=status.HTTP_400_BAD_REQUEST)

        item_total_price = item.price * item_amount.amount
        CheckItem.objects.create(check_id=check,
                                  item=item,
                                  amount=item_amount.amount,
                                  item_price=item_total_price)
        total_price += item_total_price

    check.total_price = total_price
    check.save()

    check_items = CheckItem.objects.filter(check_id=check)
    template_data = {
        'timestamp': check.timestamp,
        'items': check_items,
        'total_price': check.total_price,
    }

    template = get_template('check.html')
    html = template.render(template_data)

    options = {
        'encoding': 'UTF-8',
        'quiet': ''
    }
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf_file:
        pdf_path = temp_pdf_file.name
        pdfkit.from_string(html, pdf_path, options=options)

        with open(pdf_path, 'rb') as f:
            pdf_buffer = BytesIO(f.read())

    os.remove(pdf_path)

    pdf_name = f"check_{check.id}.pdf"
    pdf_path = os.path.join(settings.MEDIA_ROOT, pdf_name)
    check.file_path = pdf_name
    check.save()
    with open(pdf_path, 'wb') as f:
        f.write(pdf_buffer.getvalue())

    pdf_url = f"{request.build_absolute_uri(settings.MEDIA_URL)}{pdf_name}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(pdf_url)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    response = HttpResponse(img_io.getvalue(), content_type='image/png')
    return response
