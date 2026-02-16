# 🛒 eMarket API

مشروع **eMarket API** هو Back-End مبني باستخدام **Django REST Framework**  
بيوفر نظام كامل لإدارة متجر إلكتروني (مستخدمين – منتجات – طلبات – تقييمات)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📁 هيكل المشروع
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

account/     ➜ تسجيل المستخدمين – تعديل الحساب – استرجاع كلمة المرور  
product/     ➜ إدارة المنتجات – التقييمات – الفلاتر – الباجينيشن  
order/       ➜ إنشاء الطلبات – معالجتها – حذفها  
emarket/     ➜ إعدادات المشروع الرئيسية  
utils/       ➜ أدوات مساعدة  

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 APIs المستخدمين (AUTH & USER)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔹 تسجيل مستخدم جديد
────────────────────
URL: /api/register/  
METHOD: POST  

BODY:
{
  "first_name": "Ahmed",
  "last_name": "Ali",
  "email": "ahmed@email.com",
  "password": "123456"
}

📝 الوصف:
- إنشاء حساب جديد
- التأكد إن الإيميل مش متكرر
- تشفير كلمة المرور

RESPONSES:
201 ➜ تم إنشاء الحساب  
400 ➜ الإيميل موجود بالفعل  

────────────────────

🔹 جلب بيانات المستخدم الحالي
────────────────────
URL: /api/userinfo/  
METHOD: GET  
PERMISSION: IsAuthenticated  

📝 الوصف:
- يرجع بيانات المستخدم المسجل دخوله حاليًا

────────────────────

🔹 تعديل بيانات المستخدم
────────────────────
URL: /api/userinfo/update/  
METHOD: PUT  
PERMISSION: IsAuthenticated  

BODY:
{
  "first_name": "Ahmed",
  "last_name": "Ali",
  "email": "ahmed@email.com",
  "password": "newpassword"
}

📝 الوصف:
- تحديث الاسم والإيميل
- تحديث الباسورد فقط لو تم إدخاله

────────────────────

🔹 نسيان كلمة المرور
────────────────────
URL: /api/forgot_password/  
METHOD: POST  

BODY:
{
  "email": "ahmed@email.com"
}

📝 الوصف:
- إنشاء توكن عشوائي
- التوكن صالح لمدة 30 دقيقة
- إرسال لينك إعادة التعيين على الإيميل

────────────────────

🔹 إعادة تعيين كلمة المرور
────────────────────
URL: /api/reset_password/<token>  
METHOD: POST  

BODY:
{
  "password": "newpassword",
  "confirmPassword": "newpassword"
}

📝 الوصف:
- التأكد من صلاحية التوكن
- التأكد من تطابق الباسورد
- تحديث كلمة المرور

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📦 APIs الطلبات (ORDERS)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔹 إنشاء طلب جديد
────────────────────
URL: /api/order/new  
METHOD: POST  
PERMISSION: IsAuthenticated  

BODY:
{
  "order_Items": [
    { "product": 1, "quantity": 2, "price": 50 }
  ],
  "city": "Cairo",
  "zip_code": "12345",
  "street": "Main St",
  "phone_no": "01000000000",
  "country": "Egypt"
}

📝 الوصف:
- حساب السعر الإجمالي تلقائيًا
- خصم الكمية من المخزون
- إنشاء Order و OrderItems

────────────────────

🔹 جلب كل الطلبات
────────────────────
URL: /api/orders/  
METHOD: GET  
PERMISSION: IsAuthenticated  

────────────────────

🔹 جلب طلب واحد
────────────────────
URL: /api/order/<id>/  
METHOD: GET  

────────────────────

🔹 معالجة الطلب
────────────────────
URL: /api/order/<id>/process/  
METHOD: PUT  
PERMISSION: IsAdminUser  

📝 الوصف:
- تغيير حالة الطلب (pending / shipped / delivered)

────────────────────

🔹 حذف طلب
────────────────────
URL: /api/order/<id>/delete/  
METHOD: DELETE  
PERMISSION: IsAdminUser  

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🛍 APIs المنتجات (PRODUCTS)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔹 جلب كل المنتجات
────────────────────
URL: /api/products/  
METHOD: GET  

📝 الوصف:
- دعم Pagination
- دعم Filters
- 12 منتج في الصفحة

────────────────────

🔹 جلب منتج بالـ ID
────────────────────
URL: /api/products/<id>/  
METHOD: GET  

────────────────────

🔹 إضافة منتج جديد
────────────────────
URL: /api/products/new  
METHOD: POST  
PERMISSION: IsAuthenticated  

────────────────────

🔹 تعديل منتج
────────────────────
URL: /api/products/update/<id>/  
METHOD: PUT  
PERMISSION: IsAdminUser + Owner  

────────────────────

🔹 حذف منتج
────────────────────
URL: /api/products/delete/<id>/  
METHOD: DELETE  
PERMISSION: IsAdminUser + Owner  

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⭐ APIs التقييمات (REVIEWS)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔹 إضافة / تعديل تقييم
────────────────────
URL: /api/<product_id>/review/  
METHOD: POST  
PERMISSION: IsAuthenticated  

📝 الشروط:
- التقييم من 1 إلى 5
- تحديث التقييم لو موجود
- حساب متوسط التقييم تلقائيًا

────────────────────

🔹 حذف تقييم
────────────────────
URL: /api/<product_id>/review/delete  
METHOD: DELETE  
PERMISSION: IsAdminUser  

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔐 الصلاحيات
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

IsAuthenticated ➜ المستخدم لازم يكون مسجل دخول  
IsAdminUser    ➜ الأدمن فقط  

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 ملاحظات مهمة
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✔ تشفير كلمات المرور  
✔ Reset Password بتوكن صالح 30 دقيقة  
✔ تحديث Rating تلقائي  
✔ Pagination = 12 عنصر  

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚀 المشروع جاهز للربط مع Front-End (React / Vue / Mobile)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
