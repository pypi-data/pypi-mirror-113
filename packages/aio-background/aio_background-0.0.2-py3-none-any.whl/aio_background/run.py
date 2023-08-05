import asyncio
import datetime
import logging
import time
from typing import Awaitable, Callable

import croniter  # type: ignore

from .job import Job

logger = logging.getLogger(__package__)


def run(func: Callable[[], Awaitable[None]], *, name: str = "unknown") -> Job:
    def report_if_not_cancelled(t: asyncio.Task[None]) -> None:
        if t.cancelled():
            return

        logger.exception("Job %s has stopped", name, exc_info=t.exception())

    task = asyncio.create_task(func(), name=f"{__package__}.{name}")
    task.add_done_callback(report_if_not_cancelled)
    return Job(task)


def run_by_cron(
    func: Callable[[], Awaitable[None]],
    spec: str,
    *,
    name: str = "unknown",
    suppress_exception: bool = True,
) -> Job:
    cron = croniter.croniter(expr_format=spec, start_time=datetime.datetime.now(datetime.timezone.utc))

    async def by_cron() -> None:
        attempt = 0
        for next_start_at in cron:
            await asyncio.sleep(next_start_at - time.time())

            try:
                # to have independent async context per run
                # to protect from misuse of contextvars
                await asyncio.create_task(func(), name=f"{__package__}.{name}.{attempt}")
            except Exception:
                if not suppress_exception:
                    raise

                logger.exception("Job %s has got unexpected exception", name)

            attempt += 1

    return run(by_cron, name=name)
