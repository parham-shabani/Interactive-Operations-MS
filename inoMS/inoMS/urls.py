"""
URL configuration for ProjectNameMS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView


urlpatterns = [
    path('admin/', admin.site.urls),

    # for apps:
    path('core/', include("core.urls")),
    path('ipc/', include("ipc.urls")),
    path('interactive-ops/', include("InteractiveOperations.urls")),

    # path('system_setting/', include("system_setting.urls")),
    # path('report_log/', include("report_log.urls")),
    # path('app_test_front/', include("app_test_front.urls")),
    # add other app urls ...

    # for elasticsearch:
    # path("search/", include("search.urls")),

    # for Spectacular, Optional UI:
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

# ***************** add for gRPC **************************************************************************************

"""
Running the gRPC server alongside the Django application occurs in two modes:

1-In the local development environment, when running the command 'python manage.py runserver 0.0.0.0:8000', 
  Django sets the environment variable 'RUN_MAIN' which indicates the main process is running. 
  In this mode, the gRPC server is started only once during this main process execution.

2-In the production environment, such as when the application is run 
  with 'gunicorn' (e.g., gunicorn ProjectNameMS.wsgi:application -b :8000), the 'SERVER_SOFTWARE' environment variable 
  is set by the WSGI server, indicating the application is running as a server, and the gRPC server should also 
  be started in this mode.

To prevent blocking the main Django execution, the gRPC server runs in a separate process using 
'multiprocessing.Process', ensuring parallel execution and enabling communication between microservices.
"""

import os
from multiprocessing import Process
from ipc.grpc_server import grpc_server_run

GRPC_SERVER_URL = os.environ.get('GRPC_SERVER_URL')

if os.environ.get('RUN_MAIN') or os.environ.get('SERVER_SOFTWARE'):
    grpc_process = Process(target=grpc_server_run)
    print(f'---Server is running. {GRPC_SERVER_URL}')
    grpc_process.start()
