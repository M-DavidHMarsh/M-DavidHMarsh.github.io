from http.server import SimpleHTTPRequestHandler, HTTPServer;
import posixpath
import mimetypes

class CORSHandler(SimpleHTTPRequestHandler):
    extensions_map = _encodings_map_default = {
        '.gz': 'application/gzip',
        '.Z': 'application/octet-stream',
        '.bz2': 'application/x-bzip2',
        '.xz': 'application/x-xz',
        '.wasm': 'application/wasm',
    }

    def guess_type(self, path):
        # if(path.endswith(".gz")):
        #     base, junk = posixpath.splitext(path)
        #     return super().guess_type(base)
        # return super().guess_type(path)

        base, ext = posixpath.splitext(path)
        if ext == ".gz":
            path = base
            base, ext = posixpath.splitext(base)
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        ext = ext.lower()
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        guess, _ = mimetypes.guess_type(path)
        if guess:
            return guess
        return 'application/octet-stream'

    def end_headers(self):
        path = self.translate_path(self.path)
        if path.endswith(".gz"):
            self.send_header('Content-Encoding', 'gzip')
        self.send_header('Access-Control-Allow-Origin', '*'),
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS'),
        self.send_header('Access-Control-Allow-Headers', 'Content-Type'),
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.end_headers()

HTTPServer(('localhost', 8360), CORSHandler).serve_forever()
