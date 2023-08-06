import time

from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

__all__ = [
    "ATRFileHandler",
]

class ATRFileHandler(TimedRotatingFileHandler):
    """ A TimedRotatingFileHandler that works for repeated short-duration executions. 
    When instanciated it tries to read the next rollover time from a cache file, if it exists.
    Otherwise it uses the current time to calculate the next rollover and write it to the cache. 
    The cache is automatically updated when rollover occurs.
    
    By default, the cache is a file with the log filename plus '.nextrot' suffix.
        For a logfile 'test.log', the cachefile will be 'test.log.nextrot'. """

    def __init__(self, *args, cache_suffix: str = ".nextrot", **kwargs):
        super().__init__(*args, **kwargs)
        self.cache_suffix = cache_suffix
        if self._rollover_cache_exists():
            self.rolloverAt = self._read_next_rollover_from_cache()
        else:
            self._write_next_rollover_to_cache()
    
    def _cache_filename(self) -> Path:
        return Path(f"{self.baseFilename}{self.cache_suffix}") 

    def _rollover_cache_exists(self) -> bool:
        return self._cache_filename().exists()

    def _read_next_rollover_from_cache(self) -> int:
        with open(self._cache_filename(), "r") as fp:
            timestamp = fp.read().strip()
            return int(timestamp)
    
    def _write_next_rollover_to_cache(self):
        with open(self._cache_filename(), "w") as fp:
            fp.write(str(self.rolloverAt))

    def doRollover(self):
        """ Perform current rollover and write next rollover time to cache """
        super().doRollover()
        self._write_next_rollover_to_cache()
