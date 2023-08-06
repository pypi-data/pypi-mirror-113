import time
from functools import wraps


def retry(
    exception,
    tries=4,
    delay=3,
    backoff=2,
    logging=False,
    use_reset=False,
):
    '''Retry calling the decorated function using an exponential backoff.

    Reference: http://wiki.python.org/moin/PythonDecoratorLibrary#Retry

    Args:
        exception (Exception or tuple of Exception): Exception(s) to catch.
        tries (int): Number of times to
            try (not retry) before giving up.
        delay (int): Initial delay between retries in seconds.
        backoff (int): Backoff multiplier. For example
            a value of 2 will double the delay each retry.
        logging (bool): Print messages to the console.
    '''

    def deco_retry(f):

        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay

            if use_reset:

                def cb_reset():
                    nonlocal mtries, mdelay
                    mtries, mdelay = tries, delay

                kwargs['cb_reset'] = cb_reset

            while True:
                try:
                    print('Trying...')
                    return f(*args, **kwargs)

                except exception as e:
                    if mtries <= 1:
                        raise

                    if logging:
                        print('{}, Retrying in {} seconds...'.format(e, mdelay))

                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff

        return f_retry

    return deco_retry


def abstractmethod(func):
    '''Print an error to console if the decorated method is not overwritten.'''

    @wraps(func)
    def print_not_implemented(self, *_args, **_kwargs):
        print('{exc}: {cls}.{func}'.format(
            exc=NotImplementedError.__name__,
            cls=type(self).__name__,
            func=func.__name__,
        ))

    return print_not_implemented
