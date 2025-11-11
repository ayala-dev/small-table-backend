import os
import subprocess
from pathlib import Path

# 🏗️ הגדרות בסיס
PROJECT_NAME = "small_table_config"
APPS = [
    "users",
    "vendors",
    "products",
    "packages",
    "addons",
    "orders",
    "blog",
    "qna",
    "api"
]

print("🚀 התחלת Setup למערכת 'שולחן קטן'")

# 1️⃣ יצירת סביבת עבודה
print("📦 יוצרת סביבת עבודה וירטואלית (venv)...")
subprocess.run(["python", "-m", "venv", "venv"])

# 2️⃣ התקנת Django וספריות נלוות
print("⬇️ מתקינה Django וספריות נלוות...")
subprocess.run(["venv/Scripts/pip", "install", "django", "djangorestframework", "pillow"])

# 3️⃣ יצירת פרויקט Django חדש
print(f"🏗️ יוצרת את פרויקט Django הראשי בשם {PROJECT_NAME}...")
subprocess.run(["venv/Scripts/django-admin", "startproject", PROJECT_NAME])

# 🟢 תיקון עיקרי – נכנסת לתוך תיקיית הפרויקט
os.chdir(PROJECT_NAME)

# 4️⃣ יצירת אפליקציות עסקיות
for app in APPS:
    print(f"🧩 יוצרת אפליקציה: {app}")
    subprocess.run(["../venv/Scripts/python", "manage.py", "startapp", app])

# 5️⃣ עדכון קובץ settings.py
settings_path = Path(PROJECT_NAME) / "settings.py"
with open(settings_path, "r", encoding="utf-8") as f:
    content = f.read()

extra_apps = "\n    " + ",\n    ".join(f"'{app}'" for app in APPS) + ",\n    'rest_framework',"
content = content.replace(
    "    'django.contrib.staticfiles',",
    "    'django.contrib.staticfiles'," + extra_apps
)

content += """

# 📂 הגדרות סטטיות ומדיה
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

# ⚙️ הגדרות REST Framework בסיסיות
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
}
"""

with open(settings_path, "w", encoding="utf-8") as f:
    f.write(content)

# 6️⃣ יצירת קובץ urls ראשי
urls_path = Path(PROJECT_NAME) / "urls.py"
with open(urls_path, "w", encoding="utf-8") as f:
    f.write("""from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/vendors/', include('vendors.urls')),
    path('api/products/', include('products.urls')),
    path('api/packages/', include('packages.urls')),
    path('api/addons/', include('addons.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/blog/', include('blog.urls')),
    path('api/qna/', include('qna.urls')),
    path('api/', include('api.urls')),
]
""")

# 7️⃣ יצירת קובץ .gitignore
gitignore = Path("..") / ".gitignore"
with open(gitignore, "w", encoding="utf-8") as f:
    f.write("""venv/
__pycache__/
*.pyc
db.sqlite3
media/
static/
""")

print("\n✅ הספרינט Setup הושלם בהצלחה! 🎉")
print("📂 מבנה פרויקט נוצר:")
print(f"   {Path.cwd()}")
print("""
📁 small_table_config/
 ├── manage.py
 ├── small_table_config/
 │   ├── settings.py
 │   ├── urls.py
 │   └── __init__.py
 ├── users/
 ├── vendors/
 ├── products/
 ├── packages/
 ├── addons/
 ├── orders/
 ├── blog/
 ├── qna/
 ├── api/
 └── venv/
""")

print("\nכדי להריץ את השרת:")
print("1️⃣ הפעלת סביבת העבודה:")
print("   venv\\Scripts\\activate")
print("2️⃣ הרצת מיגרציות:")
print("   python manage.py migrate")
print("3️⃣ הרצת השרת:")
print("   python manage.py runserver")
print("\n🌐 השרת ירוץ בכתובת: http://127.0.0.1:8000/")
