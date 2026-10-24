"""Keep Windows from sleeping until the given time (a second guard beside 01b_live_poll.py, which asks the same).
usage: python keep_awake.py 2026-10-20T20:15"""
import ctypes, datetime, sys, time
until = datetime.datetime.fromisoformat(sys.argv[1])
ES_CONTINUOUS, ES_SYSTEM_REQUIRED, ES_AWAYMODE_REQUIRED = 0x80000000, 0x00000001, 0x00000040
while datetime.datetime.now() < until:
    ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)
    time.sleep(60)
ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
