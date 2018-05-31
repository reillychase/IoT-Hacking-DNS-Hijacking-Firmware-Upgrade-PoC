# adapated from http://www.piware.de/2011/01/creating-an-https-server-in-python/
# generate seperate key+crt files, make sure common name (CN) == ip or hostname
#    openssl req -x509 -sha256 -nodes -days 365 -newkey rsa:2048 -keyout newkey.key -out newkey.crt
# run as follows:
#    python simple-https-server.py

import BaseHTTPServer, SimpleHTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import ssl

# 0.0.0.0 allows connections from anywhere

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', '883')
        self.end_headers()
    def do_HEAD(self):
	f = self.send_head()
	f.close()
    
    def do_GET(self):
        self._set_headers()
        self.wfile.write("<html><body><h1>hi!</h1></body></html>")

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        # Doesn't do anything with posted data


        self._set_headers()

        self.wfile.write('{"vendor":"Hikvision","model":"MOCAM-720-01","version":"V5.1.9 build 170830","type":"Emergency","firmware_filename":"digicap.dav","release_notes_filename":"720P FW Release Notes.docx","firmware_checksum":"3BA72783B7663D2751C7C639D19B82F64D679F2B0ABBF4A691B662D5DCE46B6D","next_version_id":null,"upload_date":"2018-01-07 12:29:16 +0000","file_in_s3_confirmed":true,"info":null,"firmware_size":"8622856","firmware_url":"https://rchase.com/digicap.dav","release_notes_url":"https://prod-peq-a-firmware-uploads.s3.amazonaws.com/firmware/Hikvision/MOCAM-720-01/V5.1.8%20build%20170829/720P%20FW%20Release%20Notes.docx?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAI3CJ5PEMTCV2KBOA%2F20180417%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20180417T145848Z&X-Amz-Expires=604799&X-Amz-SignedHeaders=host&X-Amz-Signature=7c78e75e8ff6fca1790f345d7f8dc5ba4802f47cf7d6896c5c7ab69c550bf254"}')

def run(server_class=HTTPServer, handler_class=S, port=80):
    print 'Starting httpd...'
    handler_class.protocol_version = 'HTTP/1.1'
    httpd = server_class(('0.0.0.0', 443), handler_class)
    httpd.socket = ssl.wrap_socket (httpd.socket, certfile='./cert.pem', keyfile='./key.pem', server_side=True)
    httpd.serve_forever()

if __name__ == "__main__":
    run()
# pempass is cert password
