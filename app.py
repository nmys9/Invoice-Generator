import tkinter as tk
from tkinter import messagebox
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors
import arabic_reshaper
from bidi.algorithm import get_display
import datetime

# تسجيل الخط
pdfmetrics.registerFont(TTFont('Arabic', 'Amiri-Regular.ttf'))

products = []

def add_product():
    name = entry_product.get()
    quantity = entry_quantity.get()
    price = entry_price.get()

    if not name or not quantity or not price:
        messagebox.showerror("خطأ", "يرجى تعبئة جميع الحقول")
        return

    try:
        quantity = int(quantity)
        price = float(price)
        total = quantity * price
        products.append((name, quantity, price, total))

        listbox.insert(tk.END, f"{name} - الكمية: {quantity} - السعر: {price} - الإجمالي: {total}")
        clear_fields()

    except ValueError:
        messagebox.showerror("خطأ", "تأكد من أن الكمية والسعر أرقام صحيحة")

def generate_invoice():
    if not products:
        messagebox.showerror("خطأ", "لم يتم إضافة أي منتج")
        return

    try:
        discount_percent = float(entry_discount.get() or 0)
    except ValueError:
        messagebox.showerror("خطأ", "نسبة الخصم يجب أن تكون رقمًا")
        return

    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d %H:%M:%S")

    c = canvas.Canvas("فاتورة.pdf", pagesize=A4)
    c.setFont("Arabic", 14)

    width, height = A4
    y = height - 50

    # عنوان الفاتورة
    title = get_display(arabic_reshaper.reshape("فاتورة شراء"))
    c.setFont("Arabic", 20)
    c.drawCentredString(width / 2, y, title)
    y -= 30

    # التاريخ
    c.setFont("Arabic", 12)
    date_text = get_display(arabic_reshaper.reshape(f"تاريخ الإنشاء: {date_str}"))
    c.drawRightString(width - 50, y, date_text)
    y -= 40

    # رؤوس الجدول
    headers = ["المنتج", "الكمية", "السعر", "الإجمالي"]
    header_reshaped = [get_display(arabic_reshaper.reshape(h)) for h in headers]
    col_widths = [150, 80, 80, 80]
    x_start = 50
    y_table = y

    # خلفية الرأس
    c.setFillColorRGB(0.9, 0.9, 0.9)
    c.rect(x_start, y_table, sum(col_widths), 25, fill=1)
    c.setFillColor(colors.black)

    for i, h in enumerate(header_reshaped):
        c.drawCentredString(x_start + sum(col_widths[:i]) + col_widths[i]/2, y_table + 7, h)

    y_table -= 30
    total_all = 0

    for product in products:
        name, qty, price, total = product
        total_all += total

        row_data = [
            get_display(arabic_reshaper.reshape(str(name))),
            str(qty),
            str(price),
            str(total)
        ]

        for i, item in enumerate(row_data):
            c.drawCentredString(x_start + sum(col_widths[:i]) + col_widths[i]/2, y_table + 7, item)

        y_table -= 25

    c.line(x_start, y_table, x_start + sum(col_widths), y_table)
    y_table -= 30

    # الحسابات المالية
    discount_value = (discount_percent / 100) * total_all
    final_amount = total_all - discount_value

    # المبلغ الإجمالي
    c.setFont("Arabic", 14)
    total_text = get_display(arabic_reshaper.reshape(f"المبلغ الإجمالي: {total_all:.2f} شيكل"))
    c.drawRightString(width - 50, y_table, total_text)
    y_table -= 25

    # الخصم
    discount_text = get_display(arabic_reshaper.reshape(f"قيمة الخصم ({discount_percent}%): {discount_value:.2f} شيكل"))
    c.drawRightString(width - 50, y_table, discount_text)
    y_table -= 25

    # المبلغ بعد الخصم
    final_text = get_display(arabic_reshaper.reshape(f"المبلغ بعد الخصم: {final_amount:.2f} شيكل"))
    c.setFont("Arabic", 16)
    c.setFillColor(colors.darkblue)
    c.drawRightString(width - 50, y_table, final_text)

    c.save()
    messagebox.showinfo("تم", "تم حفظ الفاتورة باسم 'فاتورة.pdf'")

def clear_fields():
    entry_product.delete(0, tk.END)
    entry_quantity.delete(0, tk.END)
    entry_price.delete(0, tk.END)

def clear_all():
    clear_fields()
    listbox.delete(0, tk.END)
    products.clear()
    entry_discount.delete(0, tk.END)

# واجهة المستخدم
window = tk.Tk()
window.title("مولد فواتير")
window.geometry("500x600")
window.configure(bg="#f0f0f0")

tk.Label(window, text="اسم المنتج:", bg="#f0f0f0").pack(pady=5)
entry_product = tk.Entry(window, width=50)
entry_product.pack()

tk.Label(window, text="الكمية:", bg="#f0f0f0").pack(pady=5)
entry_quantity = tk.Entry(window, width=50)
entry_quantity.pack()

tk.Label(window, text="السعر للوحدة:", bg="#f0f0f0").pack(pady=5)
entry_price = tk.Entry(window, width=50)
entry_price.pack()

tk.Button(window, text="إضافة المنتج", command=add_product, bg="#2196F3", fg="white").pack(pady=10)

listbox = tk.Listbox(window, width=70)
listbox.pack(pady=10)

# حقل الخصم
tk.Label(window, text="نسبة الخصم (%)", bg="#f0f0f0").pack(pady=5)
entry_discount = tk.Entry(window, width=20)
entry_discount.pack()

tk.Button(window, text="توليد الفاتورة", command=generate_invoice, bg="#4CAF50", fg="white").pack(pady=5)
tk.Button(window, text="تفريغ الكل", command=clear_all, bg="#f44336", fg="white").pack(pady=5)

window.mainloop()
