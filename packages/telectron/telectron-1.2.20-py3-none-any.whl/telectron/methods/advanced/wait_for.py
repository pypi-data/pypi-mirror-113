import logging, asyncio

from telectron import filters
from telectron.scaffold import Scaffold

log = logging.getLogger(__name__)


class Waiting:
    def __init__(self, waiting_filters, handler_type):
        self.filters = waiting_filters
        self.handler_type = handler_type
        self.event = asyncio.Event()
        self.update = None
        self.lock = asyncio.Lock()


class WaitFor(Scaffold):
    async def register_waiting(
            self,
            handler_type,
            waiting_filters=filters.all
    ):
        for lock in self.dispatcher.locks_list:
            await lock.acquire()

        try:
            waiting = Waiting(waiting_filters, handler_type)
            self.dispatcher.waiting_events.append(waiting)

        finally:
            for lock in self.dispatcher.locks_list:
                lock.release()

        return waiting

    async def wait_for(
        self,
        waiting,
        timeout=10
    ):
        try:
            await asyncio.wait_for(waiting.event.wait(), timeout)
            return waiting.update
        finally:
            for lock in self.dispatcher.locks_list:
                await lock.acquire()

            try:
                self.dispatcher.waiting_events.remove(waiting)

            finally:
                for lock in self.dispatcher.locks_list:
                    lock.release()
