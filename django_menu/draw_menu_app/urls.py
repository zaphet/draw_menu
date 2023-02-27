from django.urls import path
from draw_menu_app.views import MenusPageView


app_name = 'draw_menu_app'

urlpatterns = [
    path('menus/', MenusPageView.as_view(), name='menus')
]
