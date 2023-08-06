try:
    from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
except ImportError:
    from SocketServer import ThreadingMixIn
    from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

    class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
        pass


try:
    from html import escape
except ImportError:
    from cgi import escape

import threading
import uuid

# Global state
lock = threading.Lock()
server = None
port = None
transactions = dict()


class _HttpRequestHandler(BaseHTTPRequestHandler):

    def _send_headers(self, ok):
        if ok:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=UTF-8')
        else:
            self.send_response(400)
        self.end_headers()

    def log_message(self, format, *args):
        pass

    def do_HEAD(self):
        self._send_headers(True)

    def do_GET(self):
        with lock:

            # Extract transaction id
            trx_id = self.path.rsplit('/', 1)[-1]
            if trx_id not in transactions:
                self._send_headers(False)
                return

            # Get transaction data
            trx_url, trx_title, trx_event = transactions[trx_id]

            # Handle request
            self._send_headers(True)
            self.wfile.write(('''
<html>
    <head>
        <title>''' + escape(trx_title) + '''</title>
        <meta http-equiv="refresh"
              content="3;URL=\'''' + escape(trx_url) + '''\'" />
    </head>
    <body style="font-family: sans-serif; color: #777; height: 100vh; display: flex; justify-content: center; align-items: center;">
        Loading&hellip;
    </body>
</html>
''').encode())

            # Signal success to caller
            trx_event.set()


def create_transaction(url, title):
    global server, port
    with lock:
        # Spin up server, if there is none
        if not server:
            server = ThreadingHTTPServer(('127.0.0.1', 0), _HttpRequestHandler)
            port = server.server_address[1]
            thread = threading.Thread(target=server.serve_forever)
            thread.daemon = True
            thread.start()

        # Create a new transaction
        trx_id = uuid.uuid1().hex
        trx_event = threading.Event()
        transactions[trx_id] = (url, title, trx_event)

        return trx_event, 'http://127.0.0.1:{}/{}'.format(port, trx_id)
