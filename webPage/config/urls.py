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
from Telco_defence import views  # 사용하고자 하는 app을 넣어주여야 url과 기능 연결 가능

urlpatterns = [
    path('admin/', admin.site.urls),  # 장고 자체 어드민 페이지
    path('', views.main_page_render, name='main-page'),  # 메인 페이지 렌더링
    path('list', views.customer_list, name='customer-list'),  # 리스트 페이지
    path('detail', views.customer_detail, name='customer-detail'),  # 세부 정보 페이지
    path('detail/<str:customer_ids>', views.customer_detail_selected, name='customer-detail-selected'),  # 리스트에서 선택했을때 접근
    path('detail/result/<str:customer_ids>', views.customer_detail_search, name='customer-detail-searched'),  # 검색했을때 접근
    path('dashboard', views.dashboard, name='dashboard'),  # 세부 정보 페이지
    path('administration', views.re_calc, name='administration_page'),
]
