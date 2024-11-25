from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from ..models import Invoices, MeterReadingsList


@method_decorator(login_required, name='dispatch')
class ViewListMain(ListView):
    paginate_by = 20
    ordering = ['-id']  # Ustawienie domyślnego sortowania

    def get_queryset(self):
        """
         Pobiera zapytanie dla listy faktur.
         Sortuje faktury zgodnie z parametrem sort, jeśli jest dostępny.
        """
        queryset = super().get_queryset()
        # Pobranie wartości parametru sort z adresu URL
        sort_param = self.request.GET.get('sort')
        if sort_param:
            # Wykonanie sortowania na podstawie parametru sort
            queryset = queryset.order_by(sort_param)
        return queryset

    def get_context_data(self, **kwargs):
        """
        pobiera parametr sort, oraz sprawdza czy uzytkownik ma uprawnienia do danego modelu
        """
        model_name = self.model._meta.model_name  # Nazwa modelu w małych literach
        app_label = self.model._meta.app_label  # Nazwa aplikacji, w której jest model

        # Tworzymy klucz uprawnienia
        permission_codename = f"{app_label}.view_{model_name}"

        # Sprawdzamy, czy użytkownik ma uprawnienie
        has_permission = self.request.user.has_perm(permission_codename)

        context = super().get_context_data(**kwargs)
        sort_param = self.request.GET.get('sort', 'cost')
        context['sort'] = sort_param
        context['has_permission'] = has_permission
        return context


@method_decorator(login_required, name='dispatch')
class InvoicesListView(ViewListMain):
    # todo dorobic filtrowanie faktur
    """Widok listy faktur oparty na ListView. Widok ma slużyć do przeglądania oraz sortowania faktur. Dodatkowo
    formularz ma dawac mozliwosc przejscie do edycji danej faktury, a w przyszlosci filtrownia faktur"""
    model = Invoices
    template_name = 'electricity_cost/invoices_view.html'


@method_decorator(login_required, name='dispatch')
class EnergyReadingsView(ViewListMain):
    """Widok, ktory pokazuje wszystkie odczyty licznikow, z możliwością sortwania"""
    model = MeterReadingsList
    template_name = 'electricity_cost/readings_list_view.html'
