import qrcode
from io import BytesIO
from django.shortcuts import render, redirect
import pandas as pd
import base64
from django import template

register = template.Library()

# Đăng ký filter để mã hóa base64
@register.filter
def b64encode(value):
    return base64.b64encode(value.encode('utf-8')).decode('utf-8')

def import_tickets(request):
    if request.method == 'POST' and 'excel_file' in request.FILES:
        excel_file = request.FILES['excel_file']
        df = pd.read_excel(excel_file, usecols="A:H")
        
        # Tạo danh sách lưu dữ liệu vé
        ticket_data = []
        for _, row in df.iterrows():
            ticket = {
                'code1': row[5],
                'ticket_name': row[4],
                'booking_code': row[0],
                'ticket_price': row[7],
                'ticket_date': row[2],
                'code2': row[5],
            }

            # # Kiểm tra tính hợp lệ của dữ liệu vé
            # if not all(ticket.values()):
            #     # Bỏ qua nếu có trường dữ liệu bị thiếu
            #     continue

            # try:
            #     # Kiểm tra kiểu dữ liệu của ticket_price
            #     ticket['ticket_price'] = float(ticket['ticket_price'])
            # except (TypeError, ValueError):
            #     # Bỏ qua nếu ticket_price không phải kiểu dữ liệu số
            #     continue

            # Tạo mã QR từ code1
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
            qr.add_data(ticket['code1'])
            qr.make(fit=True)

            # Tạo ảnh QR từ mã QR
            qr_image = qr.make_image(fill_color="black", back_color="white")

            # Tạo buffer để lưu trữ ảnh
            qr_buffer = BytesIO()
            qr_image.save(qr_buffer, format='PNG')
            qr_buffer.seek(0)

            # Chuyển đổi ảnh QR thành base64
            qr_code_base64 = base64.b64encode(qr_buffer.getvalue()).decode('utf-8')

            # Lưu trữ dữ liệu base64 vào từ điển ticket
            ticket['qr_code'] = qr_code_base64

            ticket_data.append(ticket)

        # Xóa dữ liệu session cũ
        request.session.pop('ticket_data', None)
        request.session.pop('selected_tickets', None)

        # Lưu trữ dữ liệu vào session
        request.session['ticket_data'] = ticket_data

        # Chuyển hướng sang trang chọn dữ liệu
        return redirect('select_tickets')

    return render(request, 'import_tickets.html')



def import_selected_tickets(request):
    if request.method == 'POST':
        selected_indices = request.POST.getlist('selected_tickets')

        # Kiểm tra nếu không có vé nào được chọn
        if len(selected_indices) == 0:
            return redirect('ticket_list')

        ticket_data = request.session.get('ticket_data', [])

        # Lọc dữ liệu theo các chỉ số được chọn
        selected_tickets = []
        for index in selected_indices:
            index = int(index)
            if index < len(ticket_data):
                selected_tickets.append(ticket_data[index])

        # Xóa dữ liệu session cũ
        request.session.pop('ticket_data', None)
        request.session.pop('selected_tickets', None)

        # Lưu trữ các vé được chọn vào session
        request.session['selected_tickets'] = selected_tickets

        # Chuyển hướng sang trang tickets.html
        return redirect('ticket_list')

    # Nếu không phải POST, hiển thị trang chọn dữ liệu
    # Chuẩn bị dữ liệu cho template: tạo danh sách tuple với chỉ số và giá trị
    ticket_data = request.session.get('ticket_data', [])
    enumerated_tickets = list(enumerate(ticket_data))

    return render(request, 'select_tickets.html', {'enumerated_tickets': enumerated_tickets})

def ticket_list(request):
    # Lấy danh sách vé đã chọn từ session
    selected_tickets = request.session.get('selected_tickets', [])

    # Xóa dữ liệu session cũ
    request.session.pop('ticket_data', None)
    request.session.pop('selected_tickets', None)

    return render(request, 'tickets.html', {'ticket_data': selected_tickets})

from django.shortcuts import redirect

def clear_session(request):
    # Xóa dữ liệu session và quay lại trang import
    request.session.flush()
    return redirect('import_tickets')