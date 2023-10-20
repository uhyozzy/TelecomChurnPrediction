"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from Telco_defence import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/1', views.test),  # 기본 테스트
    path('test/2', views.inputtest, name='itt_a'),  # 입력 테스트
    path('test/3', views.savetest, name='stt'),  # 저장 및 DB 반영 테스트
    path('', views.main_page_render, name='main-page'),  # 메인 페이지 렌더링
    path('list', views.customer_list, name='customer-list'),  # 리스트 페이지
    path('detail', views.customer_detail, name='customer-detail'),  # 세부 정보 페이지
    path('detail/<str:customer_ids>', views.customer_detail, name='customer-detail-selected'),  # 세부 정보 페이지
    path('dashboard', views.dashboard, name='dashboard'),  # 세부 정보 페이지
]
