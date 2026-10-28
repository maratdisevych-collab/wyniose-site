"""Serve the site folder like Netlify does: applies the _headers file, serves 404.html for missing paths. Usage: python3 serve.py <dir> <port>"""
import http.server, os, sys, fnmatch
ROOT = sys.argv[1]; PORT = int(sys.argv[2])
rules = []; cur = None
for line in open(os.path.join(ROOT, '_headers'), encoding='utf-8'):
    if not line.strip(): continue
    if not line.startswith(' '): cur = (line.strip(), []); rules.append(cur)
    else: k, v = line.strip().split(':', 1); cur[1].append((k.strip(), v.strip()))
class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=ROOT, **k)
    def end_headers(self):
        path = self.path.split('?')[0]
        for pat, hs in rules:
            if fnmatch.fnmatch(path, pat):
                for k, v in hs: self.send_header(k, v)
        super().end_headers()
    def send_error(self, code, message=None, explain=None):
        if code == 404:
            body = open(os.path.join(ROOT, '404.html'), 'rb').read()
            self.send_response(404); self.send_header('Content-Type', 'text/html; charset=utf-8'); self.send_header('Content-Length', str(len(body))); self.end_headers(); self.wfile.write(body); return
        super().send_error(code, message, explain)
    def log_message(self, *a): pass
http.server.ThreadingHTTPServer(('127.0.0.1', PORT), H).serve_forever()
