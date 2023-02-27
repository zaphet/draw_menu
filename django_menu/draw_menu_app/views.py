from django.shortcuts import render
from django.views import View


class MenusPageView(View):
    def get(self, request):
        return render(request, 'menus.html')
