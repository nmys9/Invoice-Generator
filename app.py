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
import os

class InvoiceGenerator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("مولد فواتير متقدم")
        self.geometry("600x700")
        self.configure(bg="#f5f5f5")

        # متغيرات التطبيق
        self.products = []
        self.font_name = "Amiri-Regular.ttf"
        self.output_file = "فاتورة.pdf"

        # تهيئة الخط العربي
        self._setup_fonts()

        # إنشاء واجهة المستخدم
        self._create_widgets()

        # ربط زر الإدخال بإضافة منتج
        self.bind('<Return>', lambda e: self.add_product())
        self.entry_product = self.entry_product # لتسهيل الوصول

    def _setup_fonts(self):
        """تسجيل الخط العربي المستخدم في الفاتورة"""
        try:
            pdfmetrics.registerFont(TTFont('Arabic', self.font_name))
        except Exception as e:
            messagebox.showerror("خطأ", f"الخط {self.font_name} غير موجود. يرجى تثبيته أولاً.\n{e}")
            self.destroy()

    def _create_widgets(self):
        """إنشاء عناصر واجهة المستخدم"""
        input_frame = tk.LabelFrame(self, text="بيانات المنتج", bg="#f5f5f5", padx=10, pady=10)
        input_frame.pack(pady=10, padx=10, fill="x")

        fields = [
            ("اسم المنتج:", "entry_product"),
            ("الكمية:", "entry_quantity"),
            ("السعر للوحدة:", "entry_price")
        ]

        for text, var_name in fields:
            tk.Label(input_frame, text=text, bg="#f5f5f5").grid(sticky="e")
            entry = tk.Entry(input_frame, width=40)
            entry.grid(row=len(input_frame.children)//2, column=1, pady=5)
            setattr(self, var_name, entry)

        btn_frame = tk.Frame(self, bg="#f5f5f5")
        btn_frame.pack(pady=5)

        buttons = [
            ("إضافة المنتج", "#2196F3", self.add_product),
            ("توليد الفاتورة", "#4CAF50", self.generate_invoice),
            ("تفريغ الكل", "#f44336", self.clear_all),
            ("فتح الفاتورة", "#FF9800", self.open_invoice)
        ]

        for text, color, command in buttons:
            tk.Button(btn_frame, text=text, bg=color, fg="white",
                    command=command).pack(side="left", padx=5)

        list_frame = tk.LabelFrame(self, text="المنتجات المضافة", bg="#f5f5f5")
        list_frame.pack(pady=10, padx=10, fill="both", expand=True)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        self.listbox = tk.Listbox(list_frame, width=70, height=10,
                                    yscrollcommand=scrollbar.set)
        self.listbox.pack(fill="both", expand=True)
        scrollbar.config(command=self.listbox.yview)

        discount_frame = tk.Frame(self, bg="#f5f5f5")
        discount_frame.pack(pady=5)

        tk.Label(discount_frame, text="نسبة الخصم (%):", bg="#f5f5f5").pack(side="left")
        self.entry_discount = tk.Entry(discount_frame, width=10)
        self.entry_discount.pack(side="left", padx=5)
        self.entry_discount.insert(0, "0")

    def add_product(self):
        """إضافة منتج جديد إلى القائمة"""
        name = self.entry_product.get().strip()
        quantity = self.entry_quantity.get().strip()
        price = self.entry_price.get().strip()

        if not all([name, quantity, price]):
            messagebox.showerror("خطأ", "يرجى تعبئة جميع الحقول")
            return

        try:
            quantity = int(quantity)
            price = float(price)

            if quantity <= 0 or price <= 0:
                raise ValueError

            total = quantity * price
            self.products.append((name, quantity, price, total))

            text = f"{name} -> الكمية: {quantity} - السعر: {price:.2f} - الإجمالي: {total:.2f}"

            reshaped_text = arabic_reshaper.reshape(text)
            bidi_text = get_display(reshaped_text)

            self.listbox.insert(tk.END, bidi_text)

            self.clear_fields()

        except ValueError:
            messagebox.showerror("خطأ", "الكمية يجب أن تكون عدد صحيح والسعر عدد موجب")

    def generate_invoice(self):
        """توليد ملف PDF للفاتورة"""
        if not self.products:
            messagebox.showerror("خطأ", "لم يتم إضافة أي منتج")
            return

        try:
            discount_percent = float(self.entry_discount.get() or 0)
            if discount_percent < 0 or discount_percent > 100:
                raise ValueError
        except ValueError:
            messagebox.showerror("خطأ", "نسبة الخصم يجب أن تكون بين 0 و 100")
            return

        try:
            c = canvas.Canvas(self.output_file, pagesize=A4)
            width, height = A4

            # إعداد الخط
            c.setFont("Arabic", 14)

            # معلومات الفاتورة الأساسية
            self._draw_header(c, width, height)

            # جدول المنتجات
            self._draw_products_table(c, width, height - 120) # تم تعديل قيمة البدء

            # الحسابات النهائية
            self._draw_calculations(c, width, height - 120 - len(self.products)*25 - 50, discount_percent) # وتم تعديلها هنا أيضاً

            # حفظ الملف
            c.save()
            messagebox.showinfo("تم", f"تم حفظ الفاتورة باسم '{self.output_file}'")

        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء إنشاء الفاتورة: {str(e)}")

    def _draw_header(self, c, width, height):
        """رسم رأس الفاتورة"""
        # عنوان الفاتورة
        title = self._format_arabic("فاتورة شراء")
        c.setFont("Arabic", 20)
        c.drawCentredString(width / 2, height - 50, title)

        # التاريخ والوقت
        date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        date_text = self._format_arabic(f"تاريخ الإنشاء: {date_str}")
        c.setFont("Arabic", 12)
        c.drawRightString(width - 50, height - 80, date_text)

    def _draw_products_table(self, c, width, start_y):
        """رسم جدول المنتجات"""
        headers = ["الإجمالي", "السعر", "الكمية", "المنتج"]
        col_widths = [80, 80, 80, 160]
        x_start = 50

        c.setFillColorRGB(0.9, 0.9, 0.9)
        c.rect(x_start, start_y, sum(col_widths), 25, fill=1)
        c.setFillColor(colors.black)

        for i, h in enumerate(headers):
            c.drawCentredString(x_start + sum(col_widths[:i]) + col_widths[i]/2,
                                    start_y + 7,
                                    self._format_arabic(h))

        # بيانات المنتجات
        y = start_y - 25
        for product in self.products:
            name, qty, price, total = product

            row_data = [
                self._format_arabic(f"{total:.2f}"),
                self._format_arabic(f"{price:.2f}"),
                self._format_arabic(str(qty)),
                self._format_arabic(name)
            ]

            for i, item in enumerate(row_data):
                c.drawCentredString(x_start + sum(col_widths[:i]) + col_widths[i]/2,
                                        y + 7,
                                        item)

            y -= 25

        # خط نهاية الجدول
        c.line(x_start, y, x_start + sum(col_widths), y)

    def _draw_calculations(self, c, width, y, discount_percent):
        """رسم الحسابات النهائية"""
        total_all = sum(product[3] for product in self.products)
        discount_value = (discount_percent / 100) * total_all
        final_amount = total_all - discount_value

        # المبلغ الإجمالي
        total_text = self._format_arabic(f"المبلغ الإجمالي: {total_all:.2f} شيكل")
        c.drawRightString(width - 50, y, total_text)

        # الخصم
        discount_text = self._format_arabic(f"قيمة الخصم ({discount_percent}%): {discount_value:.2f} شيكل")
        c.drawRightString(width - 50, y - 25, discount_text)

        # المبلغ النهائي
        final_text = self._format_arabic(f"المبلغ بعد الخصم: {final_amount:.2f} شيكل")
        c.setFont("Arabic", 16)
        c.setFillColor(colors.darkblue)
        c.drawRightString(width - 50, y - 50, final_text)

    def _format_arabic(self, text):
        """تنسيق النص العربي للعرض الصحيح"""
        return get_display(arabic_reshaper.reshape(str(text)))

    def open_invoice(self):
        """فتح ملف الفاتورة باستخدام البرنامج الافتراضي"""
        if not os.path.exists(self.output_file):
            messagebox.showerror("خطأ", "الفاتورة غير موجودة، يرجى توليدها أولاً")
            return

        try:
            os.startfile(self.output_file)  # لنظام ويندوز
        except AttributeError:
            try:
                os.system(f'xdg-open "{self.output_file}"')  # لنظام لينكس
            except:
                messagebox.showinfo("تم", f"تم حفظ الفاتورة في: {os.path.abspath(self.output_file)}")

    def clear_fields(self):
        """مسح حقول الإدخال"""
        self.entry_product.delete(0, tk.END)
        self.entry_quantity.delete(0, tk.END)
        self.entry_price.delete(0, tk.END)
        self.entry_product.focus_set()

    def clear_all(self):
        """مسح كل البيانات"""
        self.clear_fields()
        self.listbox.delete(0, tk.END)
        self.products.clear()
        self.entry_discount.delete(0, tk.END)
        self.entry_discount.insert(0, "0")

if __name__ == "__main__":
    app = InvoiceGenerator()
    app.mainloop()