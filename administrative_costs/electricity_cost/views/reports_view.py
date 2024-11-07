from django.shortcuts import render

def  reports_view(request):
    return render(request, 'electricity_cost/reports.html')