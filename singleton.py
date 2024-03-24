from config import SINGLETON_FILELOCK, SINGLETON_TIMEOUT
import filelock

class SingletonError(Exception):...

def ensure_singleton():
    try:
        return filelock.FileLock(SINGLETON_FILELOCK, timeout=SINGLETON_TIMEOUT)
    except:
        raise SingletonError("Only one application instance shall be alive at a time.")