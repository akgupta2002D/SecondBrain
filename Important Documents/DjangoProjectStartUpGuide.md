# Django Project & App Creation Cheat Sheet
1. Install Django: | pip install django
2. Create Project: | django-admin startproject projectname
3. Navigate to Project Directory: | cd projectname
4. Create App: | python manage.py startapp appname
5. Add App to INSTALLED_APPS: Open projectname/settings.py and add appname to INSTALLED_APPS list:
    ``` 
        INSTALLED_APPS = [
            ...
            'appname',
    ]
    ```
1. Create Initial Migration: | python manage.py makemigrations
2. Apply Migrations: | python manage.py migrate
3. Run Development Server: | python manage.py runserver
4. Create View in appname/views.py:
    ```
     from django.http import HttpResponse 

        def index(request):
            return HttpResponse("Hello, world!") 
    ```

1.  Add URL Pattern in appname/urls.py:
    ```
    1.  from django.urls import path
        from . import views

        urlpatterns = [
            path('', views.index, name='index'),
        ]
    ```

2.  Include App URLs in projectname/urls.py:
    ```    
        from django.contrib import admin
        from django.urls import include, path

        urlpatterns = [
            path('appname/', include('appname.urls')),
            path('admin/', admin.site.urls),
        ]
    ```