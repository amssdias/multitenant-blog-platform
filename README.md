# Django Multitenant Blog Platform

![Django](https://img.shields.io/badge/Django-4.2-green?style=for-the-badge&logo=django)
![Python](https://img.shields.io/badge/Python-3.9-blue?style=for-the-badge&logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-blue?style=for-the-badge&logo=postgresql)
![Redis](https://img.shields.io/badge/Redis-7.2-red?style=for-the-badge&logo=redis)
![Multitenancy](https://img.shields.io/badge/Multitenancy-Supported-orange?style=for-the-badge)

## 🚀 About the Project

This is a **Django Multitenant Blog Platform** where users can sign up on the **main domain**, and upon registration,
they get their own **subdomain** with an isolated schema to create and manage their own blog.

## 🔥 Features

- **Main Domain** (`example.com`)
    - Users can **sign up** or **log in**.
    - Upon signup, users get a **dedicated subdomain** (`user.example.com`).
- **Subdomains** (`user.example.com`)
    - Users are redirected here upon login.
    - Create, edit, and manage blog posts.
    - Each tenant has an **isolated database schema**.
- **Tech Stack**
    - Django with **Multitenancy**
    - PostgreSQL as the database
    - Redis for caching and session management
    - Docker support (optional)

## 🛠️ Installation & Setup

### 1️⃣ Clone the Repository

```sh
git clone https://github.com/yourusername/multitenant-blog.git
cd multitenant-blog
```

### 2️⃣ Install Dependencies

```sh
pip install -r requirements.txt
```

### 3️⃣ Configure the Environment

Create a `.env` file and set up your database and Redis connections.

### 4️⃣ Run Migrations

```sh
python manage.py migrate
```

### 5️⃣ Start the Development Server

```sh
python manage.py runserver dev.localhost.com:8000
```

Ensure you have added `dev.localhost.com` and any test subdomains (`blog1.localhost.com`, `blog2.localhost.com`) to your
**hosts file**.

## 🎯 How It Works

1. **User signs up on the main domain**.
2. **A new subdomain and schema are created**.
3. **User is redirected to their subdomain** upon login.
4. **User can create and manage blog posts** from their subdomain.

---
🚀 Happy Coding! 🎯

