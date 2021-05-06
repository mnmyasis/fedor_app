from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from django.urls import reverse


@login_required
def index(request):
    return HttpResponseRedirect(
        reverse('manual_matching:show_manual_matching_page')
    )
