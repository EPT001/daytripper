from django.urls import path
from myapp import views
from . import views


app_name = 'myapp'
urlpatterns = [
path('', views.search_current_location, name='index'),
path('login/',views.loginPage, name ='loginPage'),
path('logout/',views.logoutUser, name ='logout'),
path('signup/',views.signupPage, name ='signupPage'),
path('autocomplete/',views.autocomplete,name='autocomplete'),
path('current_location/',views.search_current_location,name='current_location'),
path('returnplaces/',views.returnplaces,name='returnplaces'),
path('selected_place/<placeId>/',views.selected_place,name='selected_place'),
path('bookmarks/', views.user_bookmarks, name='user_bookmarks'),
path('delete_bookmark/<int:bookmark_id>/', views.delete_bookmark, name='delete_bookmark')
]
