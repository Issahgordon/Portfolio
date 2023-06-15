from django.urls import path
from . views import Home,Manager_Login,Manager_Logout,Manager_Register,Dashboard,Upload,Delete_Book,Select_Book,Categories,Select_Category,Trends,About
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [




    path('', Home.as_view(), name="home"),
    path('about', About.as_view(), name="about"),

    path('register', Manager_Register.as_view(), name="register"),
    path('login', Manager_Login.as_view(), name="login"),
    path('logout', Manager_Logout.as_view(), name="logout"),
    path('dashboard', Dashboard.as_view(), name="dashboard"),
    path('upload', Upload.as_view(), name="upload"),
    path('delete_book', Delete_Book.as_view(), name="delete_book"),
    path('select_book/<int:pk>', Select_Book.as_view(), name="select_book"),

    path('categories', Categories.as_view(), name="categories"),
    path('select_category/<str:pk>', Select_Category.as_view(), name="select_category"),

    path('trends', Trends.as_view(), name="trends"),








]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)