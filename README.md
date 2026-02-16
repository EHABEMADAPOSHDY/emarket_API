# eMarket API

**eMarket API** is a Django REST Framework project for managing an online marketplace. It provides endpoints for user authentication, profile management, product CRUD, reviews, and order processing.

---

## 🗂 Project Structure

- `account/` – User registration, login, profile, password reset  
- `product/` – Product listing, CRUD, review management  
- `order/` – Order creation, retrieval, processing, deletion  
- `emarket/` – Project configuration (settings, urls, wsgi, asgi)  
- `utils/` – Utility modules like custom error handling  

---

## 🔑 User APIs

### Register a User
- **URL:** `/api/register/`  
- **Method:** `POST`  
- **Body:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "password": "password123"
}
Description: Registers a new user. Checks if email exists. Password is hashed using Django’s make_password.

Responses:

201 Created – Account registered successfully

400 Bad Request – Email already exists

Get Current User
URL: /api/userinfo/

Method: GET

Permissions: Authenticated users only

Description: Returns the current logged-in user’s details.

Response Example:

json
Copy code
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "username": "john@example.com"
}
Update User Profile
URL: /api/userinfo/update/

Method: PUT

Permissions: Authenticated users

Body Example:

json
Copy code
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "password": "newpassword123"
}
Description: Updates user information. Password will be updated only if a new value is provided.

Response: Returns updated user data.

Forgot Password
URL: /api/forgot_password/

Method: POST

Body Example:

json
Copy code
{
  "email": "john@example.com"
}
Description: Sends a password reset link with a token to the user’s email. Token expires in 30 minutes.

Response: Confirmation message about sending email.

Reset Password
URL: /api/reset_password/<token>

Method: POST

Body Example:

json
Copy code
{
  "password": "newpassword123",
  "confirmPassword": "newpassword123"
}
Description: Resets the password using a valid token. Checks for expiration and password match.

Response: Success or error message.

🛒 Order APIs
Create New Order
URL: /api/order/new

Method: POST

Permissions: Authenticated users

Body Example:

json
Copy code
{
  "order_Items": [
    {"product": 1, "quantity": 2, "price": 50},
    {"product": 2, "quantity": 1, "price": 30}
  ],
  "city": "Cairo",
  "zip_code": "12345",
  "street": "Main St",
  "phone_no": "01000000000",
  "country": "Egypt"
}
Description: Creates a new order, calculates total amount, reduces product stock, and saves order items.

Response: Returns order data.

Get All Orders
URL: /api/orders/

Method: GET

Permissions: Authenticated users

Description: Returns all orders for admin or user.

Response: List of orders.

Get Single Order
URL: /api/order/<pk>/

Method: GET

Permissions: Authenticated users

Description: Fetch a single order by ID.

Process Order
URL: /api/order/<pk>/process/

Method: PUT

Permissions: Admin users only

Description: Updates order status (e.g., pending, shipped, delivered).

Delete Order
URL: /api/order/<pk>/delete/

Method: DELETE

Permissions: Admin users only

Description: Deletes a specific order.

🛍 Product APIs
Get All Products
URL: /api/products/

Method: GET

Description: Returns all products with pagination and optional filters.

Get Product by ID
URL: /api/products/<pk>/

Method: GET

Description: Returns a single product by ID.

Create New Product
URL: /api/products/new

Method: POST

Permissions: Authenticated users

Description: Adds a new product. Admin or product owner only.

Update Product
URL: /api/products/update/<pk>/

Method: PUT

Permissions: Authenticated & product owner

Description: Updates product details. Admin or owner only.

Delete Product
URL: /api/products/delete/<pk>/

Method: DELETE

Permissions: Authenticated & product owner

Description: Deletes a product. Admin or owner only.

Create Review
URL: /api/<pk>/review/

Method: POST

Permissions: Authenticated users

Description: Creates or updates a review for a product. Ratings must be 1–5.

Delete Review
URL: /api/<pk>/review/delete

Method: DELETE

Permissions: Admin users only

Description: Deletes the review for the authenticated user.

🔒 Permissions
IsAuthenticated – Only logged-in users can access

IsAdminUser – Only admins can perform certain actions (like deleting or processing orders)

📦 Notes
Passwords are hashed using make_password.

Password reset uses a token system with 30-minute expiration.

Product ratings are automatically calculated based on reviews.

Pagination for products is set to 12 items per page.

