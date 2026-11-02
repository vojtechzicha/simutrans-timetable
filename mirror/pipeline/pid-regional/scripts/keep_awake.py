"""Keep Windows awake, display on, until the given time (the guard beside 01_live_poll.py, which asks only for the system;
on Modern Standby laptops the system can still idle into standby once the display turns off, so this one holds the display
too, as `caffeinate -d` would). usage: python keep_awake.py 2026-11-03T20:20"""
import ctypes, datetime, sys, time
until = datetime.datetime.fromisoformat(sys.argv[1])
ES_CONTINUOUS, ES_SYSTEM_REQUIRED, ES_DISPLAY_REQUIRED = 0x80000000, 0x00000001, 0x00000002
while datetime.datetime.now() < until:
    ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED)
    print(datetime.datetime.now().strftime('%m-%d %H:%M'), 'awake', flush=True)
    time.sleep(300)
ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
