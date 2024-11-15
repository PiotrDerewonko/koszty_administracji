from django.shortcuts import render

def  reports_view(request):
    has_group = request.user.groups.filter(name='Raporty').exists()
    return render(request, 'electricity_cost/reports.html', {'has_group': has_group})