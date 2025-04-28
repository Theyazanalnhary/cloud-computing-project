from django.db import models
from django.contrib.auth.models import AbstractUser


# 1. جدول الوكلاء (Agent)
class Agent(models.Model):
    # اسم الوكيل
    agentname = models.CharField(max_length=65)
    # رقم حساب الوكيل
    agents_ac_no = models.CharField(max_length=6, unique=True)
    # اسم الشخص المسؤول
    contact_person = models.CharField(max_length=65, null=True, blank=True)
    # رقم الهاتف
    telephone = models.CharField(max_length=21, null=True, blank=True)
    # رقم الفاكس
    fax = models.CharField(max_length=21, null=True, blank=True)
    # البريد الإلكتروني
    email = models.EmailField(max_length=50, null=True, blank=True)
    # عنوان الفاتورة
    billing_address = models.CharField(max_length=15, null=True, blank=True)
    # المدينة
    town = models.CharField(max_length=35, null=True, blank=True)
    # الرمز البريدي
    postal_code = models.IntegerField(null=True, blank=True)
    # الشارع أو الطريق
    road_street = models.CharField(max_length=65, null=True, blank=True)
    # المبنى
    building = models.CharField(max_length=65, null=True, blank=True)
    # الارتباط بنوع السعر
    rate = models.ForeignKey('Rate', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.agentname


# 2. جدول الفواتير (Bill)
class Bill(models.Model):
    # رقم الحجز المرتبط بالفاتورة
    book_id = models.IntegerField()
    # تاريخ إصدار الفاتورة
    date_billed = models.DateTimeField()
    # رقم الفاتورة
    billno = models.IntegerField(default=0)
    # حالة الفاتورة
    status = models.SmallIntegerField(null=True, blank=True)
    # تاريخ التحقق من الفاتورة
    date_checked = models.DateField(null=True, blank=True)

    class Meta:
        # تحديد أن الرقم التسلسلي والرقم الفاتورة يجب أن يكونا فريدين معًا
        unique_together = ('book_id', 'billno')

    def __str__(self):
        return f"Bill {self.billno} for Booking {self.book_id}"


# 3. جدول الحجز (Booking)
class Booking(models.Model):
    # ربط الحجز بالضيف
    guest = models.ForeignKey('Guest', on_delete=models.CASCADE)
    # نوع الحجز (مثل: فردي، عائلي)
    booking_type = models.CharField(max_length=1)
    # نوع الوجبات
    meal_plan = models.CharField(max_length=2)
    # عدد البالغين
    no_adults = models.SmallIntegerField(null=True, blank=True)
    # عدد الأطفال
    no_child = models.SmallIntegerField(null=True, blank=True)
    # تاريخ الوصول
    checkin_date = models.DateField()
    # تاريخ المغادرة
    checkout_date = models.DateField()
    # معرف الإقامة
    residence_id = models.CharField(max_length=2, null=True, blank=True)
    # طريقة الدفع
    payment_mode = models.SmallIntegerField(null=True, blank=True)
    # ربط الحجز بالوكيل
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=True)
    # رقم الغرفة
    roomid = models.IntegerField()
    # الشخص الذي سجل الوصول
    checkedin_by = models.IntegerField(null=True, blank=True)
    # رقم الفاتورة
    invoice_no = models.CharField(max_length=15, null=True, blank=True)
    # حالة الفاتورة (هل تم دفعها)
    billed = models.SmallIntegerField(null=True, blank=True)
    # الشخص الذي سجل المغادرة
    checkout_by = models.IntegerField(null=True, blank=True)
    # تاريخ ووقت التسجيل
    codatetime = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Booking {self.guest}"


# 4. جدول الدول (Country)
class Country(models.Model):
    # اسم الدولة
    country = models.CharField(max_length=150)
    # رمز الدولة
    countrycode = models.CharField(max_length=10, unique=True)
    # رمز المشترك (لأغراض خاصة)
    subscriber = models.CharField(max_length=19, null=True, blank=True)
    # الجنسية
    nationality = models.CharField(max_length=150, null=True, blank=True)
    # العملة
    currency = models.CharField(max_length=45, null=True, blank=True)

    def __str__(self):
        return self.country


# 5. جدول التفاصيل (Detail)
class Detail(models.Model):
    # اسم العنصر
    item = models.CharField(max_length=35)
    # وصف العنصر
    description = models.CharField(max_length=150, null=True, blank=True)
    # هل هو للبيع؟
    sale = models.BooleanField(default=False)
    # هل هو من المصاريف؟
    expense = models.BooleanField(default=False)

    def __str__(self):
        return self.item


# 6. جدول نوع الوثائق (DocType)
class DocType(models.Model):
    # رمز الوثيقة
    doc_code = models.CharField(max_length=5)
    # نوع الوثيقة
    doc_type = models.CharField(max_length=25)
    # ملاحظات إضافية
    remarks = models.TextField(null=True, blank=True)
    # حسابات خاصة
    accounts = models.SmallIntegerField(null=True, blank=True)
    # تعاونيات
    cooperative = models.SmallIntegerField(null=True, blank=True)
    # الرواتب
    payroll = models.SmallIntegerField(null=True, blank=True)

    def __str__(self):
        return self.doc_type


# 7. جدول السجل الضيفي (Guestbook)
class Guestbook(models.Model):
    # اسم الضيف
    name = models.CharField(max_length=100, null=True, blank=True)
    # البريد الإلكتروني للضيف
    email = models.EmailField(max_length=100, null=True, blank=True)
    # تاريخ الرسالة
    date = models.DateTimeField(null=True, blank=True)
    # الرسالة
    message = models.TextField(null=True, blank=True)
    # الرد على الرسالة
    reply = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Message from {self.name}"


# 8. جدول الضيوف (Guest)
class Guest(models.Model):
    # اسم العائلة
    lastname = models.CharField(max_length=40)
    # الاسم الأول
    firstname = models.CharField(max_length=20, null=True, blank=True)
    # الاسم الأوسط
    middlename = models.CharField(max_length=15, null=True, blank=True)
    # رقم جواز السفر
    pp_no = models.CharField(max_length=15, null=True, blank=True)
    # رقم الهوية
    idno = models.IntegerField(null=True, blank=True)
    # رمز الدولة
    countrycode = models.CharField(max_length=2)
    # صندوق البريد
    pobox = models.CharField(max_length=10, null=True, blank=True)
    # المدينة
    town = models.CharField(max_length=30, null=True, blank=True)
    # الرمز البريدي
    postal_code = models.CharField(max_length=5, null=True, blank=True)
    # الهاتف
    phone = models.CharField(max_length=15, null=True, blank=True)
    # البريد الإلكتروني
    email = models.EmailField(max_length=50, null=True, blank=True)
    # الهاتف المحمول
    mobilephone = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return f"{self.lastname}, {self.firstname}"


# 9. جدول طرق الدفع (PaymentMode)
class PaymentMode(models.Model):
    # خيار الدفع
    payment_option = models.CharField(max_length=30)

    def __str__(self):
        return self.payment_option


# 10. جدول الأسعار (Rate)
class Rate(models.Model):
    # نوع الحجز
    booking_type = models.CharField(max_length=1)
    # الإشغال
    occupancy = models.CharField(max_length=1)
    # نوع السعر
    rate_type = models.CharField(max_length=1)
    # سعر BO
    bo = models.DecimalField(max_digits=10, decimal_places=0)
    # سعر BB
    bb = models.DecimalField(max_digits=10, decimal_places=0)
    # سعر HB
    hb = models.DecimalField(max_digits=10, decimal_places=0)
    # سعر FB
    fb = models.DecimalField(max_digits=10, decimal_places=0)
    # العملة
    currency = models.CharField(max_length=45)
    # تاريخ بدء السعر
    date_started = models.DateField()
    # تاريخ انتهاء السعر
    date_stopped = models.DateField()

    def __str__(self):
        return f"Rate {self.booking_type} - {self.currency}"


# 11. جدول الحجوزات (Reservation)
class Reservation(models.Model):
    # طريقة الحجز
    reserved_through = models.CharField(max_length=15)
    # ربط الحجز بالضيف
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    # من قام بالحجز
    reservation_by = models.CharField(max_length=35, null=True, blank=True)
    # هاتف الشخص المحجوز
    reservation_by_phone = models.CharField(max_length=23, null=True, blank=True)
    # تاريخ الحجز
    date_reserved = models.DateField()
    # تاريخ الوصول المحجوز
    reserve_checkin_date = models.DateField()
    # تاريخ المغادرة المحجوز
    reserve_checkout_date = models.DateField(null=True, blank=True)
    # عدد البالغين
    no_adults = models.SmallIntegerField(null=True, blank=True)
    # عدد الأطفال من 0 إلى 5 سنوات
    no_child_0_5 = models.SmallIntegerField(null=True, blank=True)
    # عدد الأطفال من 6 إلى 12 سنة
    no_child_6_12 = models.SmallIntegerField(null=True, blank=True)
    # عدد الأطفال الرضع
    no_babies = models.SmallIntegerField(null=True, blank=True)
    # خطة الوجبات
    meal_plan = models.CharField(max_length=2, null=True, blank=True)
    # تعليمات الدفع
    billing_instructions = models.TextField(null=True, blank=True)
    # مبلغ الإيداع
    deposit = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    # ربط الحجز بالوكيل
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=True)
    # رقم القسيمة
    voucher_no = models.CharField(max_length=15, null=True, blank=True)
    # من قام بالحجز
    reserved_by = models.IntegerField()
    # تاريخ الحجز
    date_reserved = models.DateField(null=True, blank=True)
    # من أكد الحجز
    confirmed_by = models.IntegerField(null=True, blank=True)
    # تاريخ التأكيد
    confirmed_date = models.DateField(null=True, blank=True)
    # رقم الغرفة المحجوزة
    roomid = models.IntegerField()
    # هل تم الفوترة؟
    billed = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Reservation {self.reserved_through} for {self.guest}"


# 12. جدول الغرف (Room)
class Room(models.Model):
    # رقم الغرفة
    roomno = models.SmallIntegerField()
    # نوع الغرفة
    roomtype = models.ForeignKey('RoomType', on_delete=models.SET_NULL, null=True, blank=True)
    # اسم الغرفة
    roomname = models.CharField(max_length=35, null=True, blank=True)
    # عدد الغرف
    noofrooms = models.SmallIntegerField(null=True, blank=True)
    # عدد الأشخاص المسموح بهم
    occupancy = models.SmallIntegerField(null=True, blank=True)
         # هل تحتوي الغرفة على تلفزيون؟
    tv = models.BooleanField(default=False, verbose_name="هل تحتوي الغرفة على تلفزيون؟")
# هل تحتوي الغرفة على تكييف؟
    aircondition = models.BooleanField(default=False, verbose_name="هل تحتوي الغرفة على تكييف؟")
# هل تحتوي الغرفة على مروحة؟
    fun = models.BooleanField(default=False, verbose_name="هل تحتوي الغرفة على مروحة؟")
# هل تحتوي الغرفة على صندوق أمانات؟
    safe = models.BooleanField(default=False, verbose_name="هل تحتوي الغرفة على صندوق أمانات؟")
# هل تحتوي الغرفة على ثلاجة؟
    fridge = models.BooleanField(default=False, verbose_name="هل تحتوي الغرفة على ثلاجة؟")

    # حالة الغرفة
    status = models.CharField(
    max_length=1,
    choices=[
        ('V', 'متاحة'),      # Vacant → شاغر
        ('R', 'محجوز'),    # Reserved → محجوز
        ('B', 'تم الحجز'),  # Booked → تم الحجز
        ('L', 'مغلق')      # Locked → مغلق
    ],
    default='V',
    verbose_name="حالة الحجز"
)

    # صورة الغرفة
    photo = models.BinaryField(null=True, blank=True)
    # نوع الصورة
    filetype = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"Room {self.roomno}"


# 13. جدول أنواع الغرف (RoomType)
class RoomType(models.Model):
    # نوع الغرفة
    roomtype = models.CharField(max_length=15)
    # وصف نوع الغرفة
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.roomtype


# 14. جدول المعاملات (Transaction)
class Transaction(models.Model):
    # رقم الفاتورة
    billno = models.IntegerField()
    # نوع الوثيقة
    doc_type = models.CharField(max_length=15)
    # رقم الوثيقة
    doc_no = models.IntegerField()
    # تاريخ الوثيقة
    doc_date = models.DateField()
    # تفاصيل المعاملة
    details = models.CharField(max_length=65)
    # المبلغ المدين
    dr = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # المبلغ الدائن
    cr = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Transaction {self.doc_no}"

from django.contrib.auth.hashers import make_password

class User(models.Model):
    userid = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=25)
    sname = models.CharField(max_length=25)
    loginname = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=128)  # دعم التشفير
    phone = models.BigIntegerField(null=True, blank=True)
    mobile = models.BigIntegerField(null=True, blank=True)
    fax = models.BigIntegerField(null=True, blank=True)
    email = models.EmailField(max_length=65, null=True, blank=True)
    dateregistered = models.DateField(null=True, blank=True)
    countrycode = models.SmallIntegerField(null=True, blank=True)

    # تشفير كلمة المرور عند الحفظ
    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.loginname



# 16. جدول الجلسات (Session)
class Session(models.Model):
    # معرف الجلسة
    session_id = models.CharField(max_length=32, unique=True)
    # ربط الجلسة بالمستخدم
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    # عنوان الـ IP للمستخدم
    ip_address = models.CharField(max_length=15, null=True, blank=True)
    # آخر نشاط للجلسة
    last_active = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.session_id


# 17. جدول نوع المعاملات (TransactionType)
class TransactionType(models.Model):
    # نوع المعاملة
    trans_type = models.CharField(max_length=10)

    def __str__(self):
        return self.trans_type


# 18. جدول المستخدمين المتصلين (UsersOnline)
class UsersOnline(models.Model):
    # ربط المستخدم
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # تاريخ آخر نشاط
    timestamp = models.DateTimeField(auto_now=True)
    # حالة النشاط
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"User {self.user.username} Online"


# 19. جدول المدفوعات (Payment)
class Payment(models.Model):
    # ربط طريقة الدفع
    payment_mode = models.ForeignKey(PaymentMode, on_delete=models.SET_NULL, null=True, blank=True)
    # ربط الدفع بالضيف
    guest = models.ForeignKey(Guest, on_delete=models.SET_NULL, null=True, blank=True)
    # المبلغ المدفوع
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    # تاريخ الدفع
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.amount} for {self.guest}"
