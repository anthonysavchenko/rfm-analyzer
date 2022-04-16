from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponseNotFound
from django.shortcuts import render

from rfm_analyzer.apps.yclients.services import get_last_update_message

from .forms import DownloadForm


@login_required
def index(request: HttpRequest):
    return render(request, 'analysis.html',
                  {'update_message': get_last_update_message(request.user.id),
                   'download_form': DownloadForm()})


@login_required
def update(request):
    update_message = 'Обновление запущено...' # if try_start_background_task(request.user.id) else 'Сервер занят, повторите запрос через 10 минут.'
    return render(request, 'analysis.html',
                  {'update_message': update_message,
                   'download_form': DownloadForm()})


@login_required
def download(request):
    if request.method != 'POST':
        return HttpResponseNotFound()
    form = DownloadForm(request.POST)
    if not form.is_valid():
        return render(request, 'index.html', {'download_form': form})

