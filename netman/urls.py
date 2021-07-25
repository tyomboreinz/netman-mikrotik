"""netman URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib.auth.views import LoginView, LogoutView
from ddi.views import *

urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', LoginView.as_view(authentication_form=LoginForm), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('', home, name='home'),

    path('setting/', setting, name='setting'),
    path('os/delete/<int:id_os>', os_delete, name='os_delete'),

    path('domain/', domain_list, name='domain_list'),
    path('domain/add', domain_add, name='domain_add'),
    path('domain/edit/<int:id_domain>', domain_edit, name='domain_edit'),
    path('domain/delete/<int:id_domain>', domain_delete, name='domain_delete'),

    path('subdomain/<int:id_domain>', subdomain_list, name='subdomain_list'),
    path('subdomain/add', subdomain_add, name='subdomain_add'),
    path('subdomain/edit/<str:id_subdomain>', subdomain_edit, name='subdomain_edit'),
    path('subdomain/delete/<str:id_subdomain>', subdomain_delete, name='subdomain_delete'),
    
    path('dhcp/server/', dhcp_server_list, name='dhcp_server_list'),
    path('dhcp/server/add', dhcp_server_add, name='dhcp_server_add'),
    path('dhcp/server/edit/<int:id_dhcp_server>', dhcp_server_edit, name='dhcp_server_edit'),
    path('dhcp/server/delete/<int:id_dhcp_server>', dhcp_server_delete, name='dhcp_server_delete'),

    path('dhcp/lease/', dhcp_lease, name='dhcp_lease'),
    path('dhcp/static/', dhcp_static_lease, name='dhcp_static_lease'),
    path('dhcp/static/add', dhcp_static_add, name='dhcp_static_add'),
    path('dhcp/static/edit/<str:id_static>', dhcp_static_edit, name='dhcp_static_edit'),
    path('dhcp/static/delete/<str:id_static>', dhcp_static_delete, name='dhcp_static_delete'),

    path('network/', network_list, name='network_list'),
    path('network/add', network_add, name='network_add'),
    path('network/edit/<int:id_subnet>', network_edit, name='network_edit'),
    path('network/scan/<int:id_subnet>', network_scan , name='network_scan'),
    path('network/<int:id_subnet>', network_detail, name='detail_network'),
    path('network/delete/<int:id_subnet>', network_delete , name='network_delete'),

    path('ipaddress/add/', ip_add, name='ip_add'),
    path('ipaddress/delete/<int:id_ip>', ip_delete, name='ip_delete'),
    path('ipaddress/edit/<int:id_ip>', ip_edit, name='ip_edit'),
]