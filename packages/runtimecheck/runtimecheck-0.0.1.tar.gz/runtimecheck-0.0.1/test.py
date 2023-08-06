import time

from runtimecheck.Timer import check_runtime

'''~~~~~~~~~~~~~~~~~~~~~~~~~Function Example~~~~~~~~~~~~~~~~~~~~~~~~~'''

@check_runtime()      # no location given automatically create a location named generic-logs and store log file
def say_hi():       # name of log file will be say_hi
    time.sleep(2)
    print("Hi")


say_hi()
