import time
from datetime import datetime, timedelta


class LiveClock:
    def __init__(self):
        self._last_tick: datetime = datetime.now()

    def tick(self, refresh_rate: int) -> float:
        next_tick = self._last_tick + timedelta(seconds=1 / refresh_rate)
        print(f"last tick: {self._last_tick.time()}, now: {datetime.now().time()} next tick: {next_tick.time()}")
        overtime = (next_tick - datetime.now()).total_seconds()

        if overtime > 0:
            time.sleep(overtime)
        elif overtime < 0:
            print("Warning: Render loop took longer than the frame time.")

        self._last_tick = next_tick

        return overtime
