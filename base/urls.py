from django.urls import URLPattern, path
from . import views


urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutPage, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('', views.home, name="home"),
    path('room/<str:pk>/', views.room, name="room"),
    path('create_room/', views.CreateRoom, name="create_room"),
    path('update_room/<str:pk>/', views.UpdateRoom, name="update_room"),
    path('edit_message/<str:pk>/', views.EditMessage, name="edit_message"),
    path('delet_room/<str:pk>/', views.DeleteRoom, name="delete_room"),
    path('delete_message/<str:pk>/', views.deleteMessage, name='delete_message'),
    path('profile/<str:pk>/', views.UserProfile, name='user_profile'),
    path('update_user/', views.UpdateUser, name='update_user'),
    path('topics/', views.TopicsPages, name="topics"),
    path('activity/', views.ActivityPages, name="activity"),

]