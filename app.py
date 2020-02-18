import datetime
import logging
import os
import sys
import time

from pythonjsonlogger import jsonlogger

# This will tell the jsonlogger what available values to pull in from the LogRecord attributes
# https://docs.python.org/2/library/logging.html#logrecord-attributes
format_str = '%(message)%(levelname)%(name)%(asctime)%(thread)'

# Overwrite the root logger like a boss
log = logging.getLogger()
log.propagate = False
log.setLevel(logging.INFO)
log_handler = logging.StreamHandler()
# This ensures the only output is ours, your use case may differ
log.handlers = [log_handler]
# This is the magic here, get us those one-line JSON logs
log_formatter = jsonlogger.JsonFormatter(format_str)
log_handler.setFormatter(log_formatter)
log.addHandler(log_handler)

# Dictionaries get converted directly on to the json object
log.info({
  'from': 'userA',
  'to': 'userB'
})
# {"message": null, "levelname": "INFO", "name": "root", "asctime": "2020-02-18 15:33:32,200", "thread": 4619554240, "from": "userA", "to": "userB"}

# Dictionaries inside strings do not
log.info('{"from": "userC", "to": "userD"}')
# {"message": "{\"from\": \"userC\", \"to\": \"userD\"}", "levelname": "INFO", "name": "root", "asctime": "2020-02-18 15:33:32,200", "thread": 4619554240}

# Extra works as expected
log.info("This is a log with extra stuff.", extra={"foo": "bar"})
# {"message": "This is a log with extra stuff.", "levelname": "INFO", "name": "root", "asctime": "2020-02-18 15:33:32,200", "thread": 4619554240, "foo": "bar"}

# exception logging even makes your stack trace work
try:
    bad_juju = 1 / 0
except:
    log.exception("We got some bad juju")
# {"message": "We got some bad juju", "levelname": "ERROR", "name": "root", "asctime": "2020-02-18 15:33:32,200", "thread": 4619554240, "exc_info": "Traceback (most recent call last):\n  File \"app.py\", line 39, in <module>\n    bad_juju = 1 / 0\nZeroDivisionError: division by zero"}

# you can also manually pull in exc_info when needed
try:
    bad_juju = 2 / 0
except:
    log.error("We got more bad juju", exc_info=True)
# {"message": "We got more bad juju", "levelname": "ERROR", "name": "root", "asctime": "2020-02-18 15:33:32,200", "thread": 4619554240, "exc_info": "Traceback (most recent call last):\n  File \"app.py\", line 46, in <module>\n    bad_juju = 2 / 0\nZeroDivisionError: division by zero"}


if __name__ == '__main__':
    messages = 1

    try:
        while os.getenv('LOOP_FOREVER') == "true":
            time.sleep(os.getenv("SECONDS_BETWEEN_LOG_MESSAGES", 5))
            log.info(f"The current time is {datetime.datetime.now()}", extra={"messages": messages})
            messages += 1
    except KeyboardInterrupt:
        log.exception("Keyboard Interrupt")
        sys.exit(1)
