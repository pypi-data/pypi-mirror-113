import time
from t3dn_sdk_core.utils.browser import popup_url, get_focused_workspace

if __name__ == '__main__':
    print('Browser/Example: Opening URL 1...')
    popup_url(
        'http://example.com/',
        'Example Domain',
        (600, 400),
        get_focused_workspace(),
    )
    print('Browser/Example: ... completed')
    time.sleep(5)
    print('Browser/Example: Opening URL 2...')
    popup_url(
        'https://www.test.de/',
        'Stiftung Warentest',
        (800, 600),
        get_focused_workspace(),
    )
    print('Browser/Example: ... completed')
    time.sleep(5)
