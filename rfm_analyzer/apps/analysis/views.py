from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponseNotFound
from django.shortcuts import render
from django.utils import timezone

from rfm_analyzer.apps.background_task.services import try_start_background_task
from rfm_analyzer.apps.yclients.services import get_last_update
from rfm_analyzer.apps.analysis.forms import DownloadForm
from rfm_analyzer.apps.analysis.services.update import update as update_data


@login_required
def index(request: HttpRequest):
    last_update = get_last_update(request.user.id)
    update_message = 'Обновление еще ни разу не выполнялось' \
        if last_update is None \
        else f'Последнее обновление {timezone.localtime(last_update):%d.%m.%y %H:%M}'
    return render(request, 'analysis.html',
                  {'update_message': update_message,
                   'download_form': DownloadForm()})


@login_required
def update(request):
    update_message = 'Обновление запущено...' \
        if try_start_background_task(
            lambda: update_data(request.user.yclients_config),
            request.user.id
        ) \
        else 'Сервер занят, повторите запрос через 5-10 минут.'
    return render(request, 'analysis.html',
                  {'update_message': update_message,
                   'download_form': DownloadForm()})


@login_required
def download(request):
    if request.method != 'POST':
        return HttpResponseNotFound()
    form = DownloadForm(request.POST)
    if not form.is_valid():
        return render(request, 'analysis.html', {'download_form': form})
