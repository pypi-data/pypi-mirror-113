# ATRFileHandler

ATRFileHandler, or AbsoluteTimedRotatingFileHandler, is a file handler like [TimedRotatingFileHandler](https://docs.python.org/3/library/logging.handlers.html#logging.handlers.TimedRotatingFileHandler) that also caches the next rollover time for your logfiles, allowing future instances of your application to rotate the logfile in schedule, avoiding surprices of large logfiles that haven't rotated as you expected.

## Diferences with TimedRotatingFileHandler

The main difference is that instead of only using the handler creation time to calculate the next rollover, it also writes and reads it from a cache file.
With TimeRotatingFileHandler, if you want to rotate logs daily but your process starts and ends in a couple of minutes, when you run it in one hour the logfile
will not rotate, because the handler won't remember the last time it was used. ATRHandler will rotate it because it saves this data to a file cache.

This allows you to easily keep weekly logfiles for a periodic shot-lived process, without making that process into a service or long running process.

## Install

With pip:

```
pip install ATRFileHandler
```

## Usage

It can be used exactly as the [TimedRotatingFileHandler](https://docs.python.org/3/library/logging.handlers.html#logging.handlers.TimedRotatingFileHandler) from the builting `logging` module.

Example:

```
import logging
from ATRFileHandler import ATRFileHandler

logger = logging.getLogger()
handler = ATRFileHandler("test.log", when="D", interval=3, backupCount=3)
logger.addHandler(handler)
logger.error("too much rythm")
```

## Running tests

```
pip install -e .
pytest --cov=ATRFileHandler/
```