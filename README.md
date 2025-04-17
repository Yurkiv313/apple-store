# 🛍️ Apple Store – Django Project

**Apple Store** is a fully functional e-commerce platform  
built with Django and Bootstrap 5.

It offers smooth product browsing, category filtering, a full-featured shopping cart, order processing, and secure user authentication with email confirmation — all backed by AWS S3 media storage.

---
## 🌐 Live Demo

You can visit the live version of the project here:  
🔗 [Apple Store on Render](https://apple-store-so34.onrender.com/)


## 🚀 Features

- 🛒 Product list with search and filtering
- 📦 Product detail pages with structured layout
- 📄 Pagination included for product list and category pages
- 🧺 Full-featured cart system — **works even for anonymous users**
- 📂 Category listing with responsive card layout
- ✅ Order confirmation page with smart redirect and cancel options
- 🔐 User registration with email verification
- 📸 Product images stored on AWS S3 (via `django-storages`)
- ⚙️ Admin panel for product & category management
- 💡 Responsive layout with consistent header, sidebar, and footer

---

## 🛠️ Tech Stack

- Django 5.2  
- django-crispy-forms & crispy-bootstrap5  
- Bootstrap 5 & Bootstrap Icons  
- Pillow (image handling)  
- django-storages & boto3 (for AWS S3)  
- python-dotenv  
- django-debug-toolbar (for development)

---

## 📁 Project Structure

```text
apple_store/
├── store/               # Main Django app
├── templates/           # All HTML templates
├── static/              # Custom styles
├── media/               # Uploaded images (served via S3)
├── requirements.txt
└── manage.py
```

---
✅ Tests

Basic test coverage is included for:

models (__str__, computed fields)
views (product listing, cart, orders)
forms (cart and user creation)
admin interface (custom fields and displays)
To run tests:
```bash
python manage.py test store.tests
```

## ⚙️ Installation

Clone the repository, create a virtual environment, and install dependencies:

```bash
git clone https://github.com/Yurkiv313/apple-store.git
cd apple-store
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
DEBUG=True
SECRET_KEY=your-django-secret-key
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_STORAGE_BUCKET_NAME=your-s3-bucket
```

Run migrations and start the development server:

```bash
python manage.py migrate
python manage.py runserver
```

## 📦 Populate Database
```bash
python manage.py populate_db
```
---
