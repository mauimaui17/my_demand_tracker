from django.urls import path
from . import views

urlpatterns = [
    path("add-to-cart/", views.addToCart, name="add-to-cart"),
    path("remove-from-cart/", views.removeFromCart, name="remove-from-cart"),
    path("profile/", views.profile, name="profile"),
    path("catalog/", views.index, name="catalog"),
    path('course/', views.coursepage, name='coursepage'),
    path('admin-dash/', views.admindash, name='admindash'),
    path('upload-report/', views.upload_report, name='upload-report'),
    path('add-course/', views.add_course, name='add-course'),
    path("", views.homepage, name="homepage"),
    path("home/", views.homepage, name="homepage"),
    path("reports/", views.report_index, name="reports"),
    path("download-pdf/", views.download_report, name='download-pdf'),
    path("site-statistics/", views.get_site_statistics, name='site-statistics')
    
]
