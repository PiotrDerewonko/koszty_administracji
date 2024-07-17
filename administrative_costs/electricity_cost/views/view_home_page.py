from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = 'electricity_cost/home_page.html'