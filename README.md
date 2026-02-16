# eMarket API

eMarket API is a Django REST Framework project for managing an online marketplace.
It provides APIs for authentication, users, products, orders, and reviews.

==================================================

PROJECT STRUCTURE

account/    -> user registration, login, profile, password reset  
product/    -> product CRUD, listing, reviews  
order/      -> order creation, processing, deletion  
emarket/    -> project configuration (settings, urls)  
utils/      -> utilities and custom error handlers  

==================================================

AUTH & USER APIS

REGISTER USER
URL: /api/register/
METHOD: POST

REQUEST BODY:
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "password": "password123"
}

RESPONSES:
201 -> account created
400 -> email already exists

--------------------------------------------------

GET CURRENT USER
URL: /api/userinfo/
METHOD: GET
PERMISSION: Authenticated

RESPONSE:
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "username": "john@example.com"
}

--------------------------------------------------

UPDATE USER PROFILE
URL: /api/userinfo/update/
METHOD: PUT
PERMISSION: Authenticated

REQUEST BODY:
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "password": "newpassword123"
}

--------------------------------------------------

FORGOT PASSWORD
URL: /api/forgot_password/
METHOD: POST

REQUEST BODY:
{
  "email": "john@example.com"
}

--------------------------------------------------

RESET PASSWORD
URL: /api/reset_password/<token>
METHOD: POST

REQUEST BODY:
{
  "password": "newpassword123",
  "confirmPassword": "newpassword123"
}

==================================================

ORDER APIS

CREATE ORDER
URL: /api/order/new
METHOD: POST
PERMISSION: Authenticated

REQUEST BODY:
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

--------------------------------------------------

GET ALL ORDERS
URL: /api/orders/
METHOD: GET
PERMISSION: Authenticated

--------------------------------------------------

GET SINGLE ORDER
URL: /api/order/<id>/
METHOD: GET
PERMISSION: Authenticated

--------------------------------------------------

PROCESS ORDER
URL: /api/order/<id>/process/
METHOD: PUT
PERMISSION: Admin

--------------------------------------------------

DELETE ORDER
URL: /api/order/<id>/delete/
METHOD: DELETE
PERMISSION: Admin

==================================================

PRODUCT APIS

GET ALL PRODUCTS
URL: /api/products/
METHOD: GET

--------------------------------------------------

GET PRODUCT BY ID
URL: /api/products/<id>/
METHOD: GET

--------------------------------------------------

CREATE PRODUCT
URL: /api/products/new
METHOD: POST
PERMISSION: Admin / Owner

--------------------------------------------------

UPDATE PRODUCT
URL: /api/products/update/<id>/
METHOD: PUT
PERMISSION: Admin / Owner

--------------------------------------------------

DELETE PRODUCT
URL: /api/products/delete/<id>/
METHOD: DELETE
PERMISSION: Admin / Owner

--------------------------------------------------

CREATE REVIEW
URL: /api/<product_id>/review/
METHOD: POST
PERMISSION: Authenticated

--------------------------------------------------

DELETE REVIEW
URL: /api/<product_id>/review/delete
METHOD: DELETE
PERMISSION: Admin

==================================================

PERMISSIONS

IsAuthenticated  
IsAdminUser  

==================================================

NOTES

- passwords are hashed using make_password
- password reset uses token with 30 minutes expiration
- product rating calculated automatically from reviews
- pagination set to 12 products per page
