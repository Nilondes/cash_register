import os
import tempfile
from django.http import HttpResponse
from .models import Item, ItemAmount, Check, CheckItems
from django.template.loader import get_template
from django.conf import settings
import pdfkit
import qrcode
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from io import BytesIO
from decimal import Decimal



@api_view(['POST'])
def create_check(request):
    if request.method == 'POST':
        item_ids = request.data.get('items', [])
        items = Item.objects.filter(id__in=item_ids)
        if not items.exists():
            return Response({"error": "Указанные товары не найдены"}, status=status.HTTP_404_NOT_FOUND)

        check = Check.objects.create(total_price=Decimal('0.00'), file_path='')
        total_price = Decimal('0.00')

        for item in items:
            item_amount = ItemAmount.objects.filter(item=item).first()
            if not item_amount:
                return Response({"error": f"Количество для товара {item.id} не указано"}, status=status.HTTP_400_BAD_REQUEST)

            item_total_price = item.price * item_amount.amount
            CheckItems.objects.create(check_id=check, item=item, amount=item_amount.amount, item_price=item_total_price)
            total_price += item_total_price

        check.total_price = total_price
        check.save()

        check_items = CheckItems.objects.filter(check_id=check)
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
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            pdf_path = tmp_file.name
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

        qr_name = f"qr_{check.id}.png"
        qr_path = os.path.join('qr_codes', qr_name)
        default_storage.save(qr_path, ContentFile(img_io.getvalue()))

        response = HttpResponse(img_io.getvalue(), content_type='image/png')
        response['Content-Disposition'] = f'inline; filename="qr_{check.id}.png"'
        return response

    return Response(status=status.HTTP_400_BAD_REQUEST)