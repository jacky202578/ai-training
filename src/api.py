#!/usr/bin/env python3
"""AI交付管理能力培训 — 学习进度API (tiny HTTP server)"""
import json, os, re, sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

USERS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'users')
os.makedirs(USERS_DIR, exist_ok=True)

class Handler(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        
    def do_OPTIONS(self):
        self.send_response(200); self._cors(); self.end_headers()
        
    def do_GET(self):
        qs = parse_qs(urlparse(self.path).query)
        uid = re.sub(r'[^a-zA-Z0-9_-]', '', qs.get('uid', ['guest'])[0])
        fpath = os.path.join(USERS_DIR, f'{uid}.json')
        
        if os.path.exists(fpath):
            with open(fpath) as f:
                data = json.load(f)
        else:
            data = {'uid': uid, 'lessons': {}, 'total_time': 0}
        
        self.send_response(200); self._cors()
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())
        
    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = json.loads(self.rfile.read(length)) if length > 0 else {}
        
        uid = re.sub(r'[^a-zA-Z0-9_-]', '', body.get('uid', 'guest'))
        lesson_id = re.sub(r'[^a-zA-Z0-9_-]', '', body.get('lesson_id', ''))
        data = body.get('data', {})
        
        fpath = os.path.join(USERS_DIR, f'{uid}.json')
        user_data = {'uid': uid, 'lessons': {}, 'total_time': 0}
        if os.path.exists(fpath):
            with open(fpath) as f:
                user_data = json.load(f)
        
        if lesson_id:
            user_data['lessons'].setdefault(lesson_id, {})
            for k, v in data.items():
                user_data['lessons'][lesson_id][k] = v
            if 'completed_at' in data:
                user_data['total_time'] = user_data.get('total_time', 0) + 60
        
        with open(fpath, 'w') as f:
            json.dump(user_data, f, ensure_ascii=False)
        
        self.send_response(200); self._cors()
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'ok': True}).encode())
        
    def log_message(self, format, *args):
        pass  # silence logs

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8100
    HTTPServer(('127.0.0.1', port), Handler).serve_forever()
