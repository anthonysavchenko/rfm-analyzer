from threading import Thread
from typing import Callable

from .models import BackgroundTask


def try_start_background_task(target: Callable[[None], None], user_id: int) -> bool:
    if BackgroundTask.objects.count() > 0:
        return False
    Thread(target=_run_target, args=(target, user_id))
    return True


def _run_target(target: Callable[[None], None], user_id: int) -> None:
    task = BackgroundTask.objects.create(user_id=user_id)
    target()
    BackgroundTask.delete(task)
