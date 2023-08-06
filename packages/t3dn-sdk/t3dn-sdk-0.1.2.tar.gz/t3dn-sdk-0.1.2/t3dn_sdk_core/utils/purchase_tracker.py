def _round(number, ndigits=None):
    '''Python 2 compatible round function.

    Args:
        number (float): Number to round.
        ndigits (int or None): Number of digits to round to.

    Returns:
        float or int: Rounded number, int if ndigits is None.
    '''
    if ndigits is not None:
        return round(number, ndigits)
    else:
        return int(number)


def calculate_percentage(progress, total, ndigits=None):
    '''Calculate the percentage.

    Args:
        progress (int): Number of bytes for progress.
        total (int): Number of bytes for total.
        digits (int or None): Number of digits to round output.

    Returns:
        float or int or None: Percentage of progress.
    '''
    if total:
        return _round(100 * progress / total, ndigits)


def convert_bytes_to_text(number, ndigits=None):
    '''Convert a number of bytes to a larger measurement.

    Args:
        number (int): Number of bytes.
        digits (int or None): Number of digits to round output.

    Returns:
        str or None: Number of B / KB / MB / GB / TB.
    '''
    if number:
        sizes = ('B', 'KB', 'MB', 'GB', 'TB')
        divisions = 0

        while number > 1024:
            number /= 1024
            divisions += 1

        return '{} {}'.format(
            _round(number, ndigits),
            sizes[divisions],
        )
