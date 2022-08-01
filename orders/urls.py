from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "orders"
urlpatterns = [
    # pages
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("r/<int:r_id>", views.r_info, name="r_info"),
    path("h/<int:h_id>", views.h_info, name="h_info"),
    path("odvoz", views.odvoz, name="odvoz"),
    path("permissionNG", views.permissionNG, name="permissionNG"),
    

    # functions
    path("done", views.done, name="done"),
    path("count", views.count, name="count"),
    path("countBaliky", views.countBaliky, name="countBaliky"),
    path('needMaterial', views.needMaterial, name="needMaterial"),
    path('needOdvoz', views.needOdvoz, name="needOdvoz"),
    path('getOdvoz', views.getOdvoz, name="getOdvoz"),
    path('check', views.check, name="check"),
    path('odpad', views.odpad, name="odpad"),
    path('h/<int:h_id>/pdf_export', views.pdf_export, name="pdf_export"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)