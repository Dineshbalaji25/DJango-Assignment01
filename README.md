#  Django Product Catalog

A Django-based web application that allows users to create, edit, and display products with multi-image support. The application includes a form-based frontend, RESTful API, PostgreSQL database support, and static/media file handling.

---

##  Quick Start (Local Development)

###  Prerequisites

1. **Install the following tools:**

   - Python 3.10+
   - pip
   - Git
   - PostgreSQL
   - Virtual Environment (`venv` or `virtualenv`)

---

### 1. Clone the Project

```bash
git clone git@github.com:Dineshbalaji25/DJango-Assignment01.git
cd DJango-Assignment01
```

---

### 2. Set Up Virtual Environment

**On Windows (CMD or PowerShell):**

```bash
python -m venv env
env\Scripts\activate
```

**On macOS/Linux:**

```bash
python3 -m venv env
source env/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure PostgreSQL

Make sure PostgreSQL is installed and running on your system.

#### 🔹 4.1 Create Database and User

Run the following SQL commands using `psql` or pgAdmin:

```sql
CREATE DATABASE django;
CREATE USER myprojectuser WITH PASSWORD '12345';
GRANT ALL PRIVILEGES ON DATABASE django TO myprojectuser;
```

#### 🔹 4.2 Update `settings.py`

In `product_app/settings.py`, update the `DATABASES` section:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'django',
        'USER': 'myprojectuser',
        'PASSWORD': '12345',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

**Optional: SQLite fallback (for development only):**

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / "db.sqlite3",
    }
}
```

---

### 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

---

### 7. Collect Static Files

```bash
python manage.py collectstatic
```

---

### 8. Run Development Server

```bash
python manage.py runserver
```

Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser to access the application locally.

---

##  Media File Uploads

Uploaded images will be saved to `/media/product_images/`.

Make sure these lines exist in `settings.py`:

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

---

 You’re now ready to use the Django Product Catalog locally!


#  Django Deployment on AWS EC2 (Ubuntu)

This guide provides step-by-step instructions to deploy your Django project on an AWS EC2 Ubuntu server using **Gunicorn** and **Nginx**.

---

##  1. Launch an EC2 Instance

1. Log in to your AWS Management Console.
2. Navigate to **EC2 → Instances → Launch Instance**.
3. Configure:

   - **Name:** Django Server  
   - **AMI:** Ubuntu Server 22.04 LTS (HVM)  
   - **Instance type:** t2.micro (Free Tier eligible)  
   - **Key pair:** Create or use existing `.pem` file  
   - **Storage:** Use default (8GB or more)  
   - **Security group:**
     - Allow SSH (port 22) from your IP
     - Allow HTTP (port 80) from anywhere
     - Allow HTTPS (port 443) from anywhere
     - Allow port 8000 (optional for testing)

4. Click **Launch Instance**.

---

##  2. Connect to the Instance

```bash
chmod 400 your-key.pem
ssh -i your-key.pem ubuntu@<public-ip-address>
```

**Example:**

```bash
ssh -i django-key.pem ubuntu@54.234.251.232
```

---

##  3. Update & Install Packages

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx curl -y
sudo apt install python3-venv -y
```

---

##  4. Set Up PostgreSQL

```bash
sudo -u postgres psql
```

Inside `psql` shell:

```sql
CREATE DATABASE django;
CREATE USER myprojectuser WITH PASSWORD '12345';
ALTER ROLE myprojectuser SET client_encoding TO 'utf8';
ALTER ROLE myprojectuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE myprojectuser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE django TO myprojectuser;
\q
```

---

##  5. Clone Your Django Project

```bash
git clone git@github.com:Dineshbalaji25/DJango-Assignment01.git
cd DJango-Assignment01
```

---

##  6. Create Virtual Environment

```bash
python3 -m venv env
source env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

##  7. Configure `settings.py`

### Database Configuration:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'django',
        'USER': 'myprojectuser',
        'PASSWORD': '12345',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Static and Media Files:

```python
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

### Allowed Hosts:

```python
ALLOWED_HOSTS = ['<your-public-ip>', 'yourdomain.com']
```

### Collect Static Files:

```bash
python manage.py collectstatic
```

---

##  8. Apply Migrations and Create Superuser

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

---

##  9. Run Gunicorn

Test Gunicorn:

```bash
gunicorn --bind 0.0.0.0:8000 product_app.wsgi
```

If you get a port error:

```bash
sudo lsof -i :8000
sudo kill -9 <PID>
```

---

## 🛡 10. Configure Gunicorn as a Service

Create a new systemd service file:

```bash
sudo nano /etc/systemd/system/gunicorn.service
```

Paste the following:

```ini
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/django-product-catalog
ExecStart=/home/ubuntu/django-product-catalog/env/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/ubuntu/django-product-catalog/gunicorn.sock product_app.wsgi:application

[Install]
WantedBy=multi-user.target
```

Start and enable Gunicorn:

```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl status gunicorn
```

---

##  11. Configure Nginx

Create a new config file:

```bash
sudo nano /etc/nginx/sites-available/django
```

Paste the following:

```nginx
server {
    listen 80;
    server_name <your-public-ip>;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        root /home/ubuntu/django-product-catalog;
    }

    location /media/ {
        root /home/ubuntu/django-product-catalog;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/django-product-catalog/gunicorn.sock;
    }
}
```

Enable the config and restart Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/django /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
sudo ufw allow 'Nginx Full'
```

---

##  12. Troubleshooting Common Errors

###  Gunicorn Port Already in Use:

```bash
sudo lsof -i :8000
sudo kill -9 <PID>
```

###  502 Bad Gateway (Nginx):

```bash
sudo systemctl restart gunicorn
sudo systemctl status gunicorn
```

###  Media Files Not Loading:

Ensure in `settings.py`:

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

In `urls.py`:

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

##  Final Checks

- Visit: `http://<your-public-ip>`
- Admin: `http://<your-public-ip>/admin`
- Confirm static and media files load properly.
- Add your domain to `ALLOWED_HOSTS` if using a custom domain.

---

