# Invoice-Generator

# 📟 Arabic Invoice Generator – مولد فواتير باللغة العربية

تطبيق بسيط لتوليد فواتير PDF باستخدام Python وواجهة رسومية (Tkinter)، مع دعم كامل للغة العربية في التنسيق والطباعة.

---

## 📆 متطلبات التشغيل

قبل البدء، تأكد من توفر:

* Python 3.8 أو أحدث
* الخط العربي `Amiri-Regular.ttf` في نفس مجلد المشروع
* مكتبات Python المطلوبة (موجودة في ملف `requirements.txt`)

---

## ⚙️ خطوات تشغيل المشروع

### 1. تحميل المشروع

يمكنك تحميل المشروع عن طريق:

* الضغط على زر `Code` > ثم `Download ZIP`
* أو باستخدام Git:

  ```bash
  git clone https://github.com/nmys9/Invoice-Generator.git
  ```

ثم ادخل إلى مجلد المشروع:

```bash
cd Invoice-Generator
```

---

### 2. إنشاء بيئة افتراضية (Virtual Environment)

من المفضل تشغيل المشروع على بيئة نظيفة:

```bash
python -m venv venv
```

تفعيل البيئة:

* على Windows:

  ```bash
  venv\Scripts\activate
  ```
* على macOS/Linux:

  ```bash
  source venv/bin/activate
  ```

---

### 3. تثبيت المكتبات

تم تحديد كل المكتبات اللازمة في `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

### 4. تشغيل التطبيق

شغّل الملف الرئيسي:

```bash
python invoice_generator.py
```

---

## 📅 كيف يعمل البرنامج؟

* أدخل اسم المنتج والكمية والسعر
* يمكنك ادخال نسبة خصم (اختياري)
* اضف أكثر من منتج
* اضغط على "توليد الفاتورة" وسيتم إنشاء ملف `فاتورة.pdf` بتنسيق عربي من اليمين للشمال

---

## 📁 الملفات الهامة

| الملف                  | الوصف                                |
| ---------------------- | ------------------------------------ |
| `invoice_generator.py` | الكود الرئيسي للتطبيق                |
| `requirements.txt`     | يحتوي على جميع المكتبات اللازمة      |
| `Amiri-Regular.ttf`    | الخط العربي المستخدم لتنسيق الفاتورة |

---

## 📜 ملاحظات

* تأكد من وجود `Amiri-Regular.ttf` في نفس ملف الكود.
* يعمل البرنامج على أنظمة Windows و Linux.
* يدعم الكتابة من اليمين للشمال بفضل `arabic-reshaper` و `python-bidi`.

---

## 👨‍💼 المطور

تم تطوير المشروع بواسطة Noor – كمشروع تدريبي لدعم اللغة العربية في توليد الفواتير المنسقة.

Feel free to contribute or customize!
