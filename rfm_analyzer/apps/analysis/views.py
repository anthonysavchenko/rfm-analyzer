from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.utils import timezone

from xlsxwriter.workbook import Workbook

from rfm_analyzer.apps.analysis.forms import DownloadForm
from rfm_analyzer.apps.analysis.services.dates import get_week_monday, get_week_sunday_or_yesterday
from rfm_analyzer.apps.analysis.services.download import execute_query, write_to_sheet
from rfm_analyzer.apps.analysis.services.update import update as update_data
from rfm_analyzer.apps.background_task.services import try_start_background_task
from rfm_analyzer.apps.yclients.services import get_last_update


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
    update_message = 'Не указана конфигурация подключения к YClients' \
        if not hasattr(request.user, 'yclients_config') else \
        'Обновление запущено...' \
        if try_start_background_task(
            lambda: update_data(request.user.yclients_config),
            request.user.id
        ) else \
        'Сервер занят, повторите запрос через 5-10 минут.'
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

    query_since = get_week_monday(form.cleaned_data['since'])
    query_till = get_week_monday(form.cleaned_data['till'])
    sunday_or_yesterday = get_week_sunday_or_yesterday(
        form.cleaned_data['till'])
    period = f'{query_since:%d.%m.%Y} - {sunday_or_yesterday:%d.%m.%Y}'

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=RFM-analyzer {period}.xlsx'

    book = Workbook(response, {'in_memory': True})
    sheet = book.add_worksheet(f'{period}')
    query_result = execute_query(query_since, query_till, request.user.id)
    write_to_sheet(sheet, query_result)
    book.close()

    return response
