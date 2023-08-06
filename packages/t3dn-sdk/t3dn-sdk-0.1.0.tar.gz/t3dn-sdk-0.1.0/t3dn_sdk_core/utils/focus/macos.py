import sys
import os
import subprocess


def focus_application():
    # detect app path
    parts = sys.executable.split('/')
    if len(parts) < 2:
        return False
    if parts[1] != 'Applications':
        return False
    app_path = None
    for i, part in enumerate(parts):
        if part.endswith('.app'):
            app_path = '/'.join(parts[0:i + 1])
            break
    if app_path is None:
        return False

    # bring application to foreground
    print('Focus: Launching open -a {0}'.format(app_path))
    with open(os.devnull, 'wb') as devnull:
        return subprocess.Popen(['open', '-a', app_path],
                                stdout=devnull,
                                stderr=devnull).poll() in (None, 0)
