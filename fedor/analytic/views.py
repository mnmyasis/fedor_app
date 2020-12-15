from django.shortcuts import render


# Create your views here.
ANALYTIC_PAGE = 'analytic/page.html'


def analytic_page(request):
    return render(request, ANALYTIC_PAGE)


def status_matchings(request):
    pass