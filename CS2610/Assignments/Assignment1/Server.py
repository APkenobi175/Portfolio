###############################
#           IMPORTS           #
###############################
import socket
from datetime import datetime
from Endpoints import (
    indexEndpoint,
    aboutEndpoint,
    experienceEndpoint,
    projectsEndpoint,
    infoEndpoint,
)

from Router import makeRouter

ROUTES = {
    "/": indexEndpoint,
    "/about": aboutEndpoint,
    "/experience": experienceEndpoint,
    "/projects": projectsEndpoint,
    "/info": infoEndpoint,

}


###################################
# Parsing and Encoding HTTP Requests
####################################



def parseRequest(rawBytes):

    try:
        text = rawBytes.decode("utf-8")

        head, sep, body = text.partition("\r\n\r\n")
        # break head into lines
        lines = head.splitlines()
        if not lines:
            return None

        # parse Request line
        parts = lines[0].split(" ")
        if len(parts) != 3:
            return None
        method, uri, version = parts

        # parse the headers
        headers = {}
        for line in lines[1:]:
            if ":" in line:
                k, v = line.split(":", 1)
                headers[k.strip()] = v.strip()

        return Request(method, uri, version, body, headers)
    except Exception:
        return "Error something bad happened"


def encodeResponse(response):
    try:
        # start with the status line
        lines = [f"{response.version} {response.code} {response.reason}"]

        # add the headers
        for k, v in response.headers.items():
            lines.append(f"{k}: {v}")

        # add a blank line to separate headers from body
        lines.append("")

        # add the body
        if response.body:
            lines.append(response.body)

        # join all lines with CRLF and encode to bytes
        return "\r\n".join(lines).encode("utf-8")
    except Exception:
        return b"HTTP/1.1 500 Internal Server Error\r\n\r\n"

### NOTE: This github copilot thing is so weird after creating parseRequest it just auto completed encodeResponse
### I guess it learned from the structure of parseRequest
### I wonder if it would have done the same if I had written parseRequest in a different way
### Now its finishing my comments too
### This is both cool and creepy


###################################
# Middleware (NOTE: github copilot also auto completed my little title bar)
###################################


MIME_TYPES = {
    "css": "text/css; charset=utf-8",
    "js": "text/javascript; charset=utf-8", 
    
}

def loggingMiddlewareFactory(next):
    def middleware(req):
        # Log the request with a timestamp
        print(f"[REQ] {req.method} {req.uri} at {datetime.now()}")
        # call the next middleware
        res = next(req)
        # Log the response with a timestamp
        print(f"[RES] {res.code} {res.reason} at {datetime.now()}")
        return res
    return middleware # IMPORTANT: Don't forget to return middleware guys
def staticFilesMiddlewareFactory(next):
    def middleware(req):
        # only GET requests are supported for static content
        if req.method != "GET":
            # call the next middleware
            return next(req)
        uri = req.uri
        # check to see if the uri has a file extentsion Eg. .html
        if "." not in uri:
            # call the next middleware
            return next(req)
        # remove the leading /
        path = uri.lstrip("/")
        if not path.startswith("static/"):
            path = "static/" + path 
        

        # get file extension
        dot = path.rfind(".")
        ext = path[dot+1:] if dot != -1 else ""

        # only allow .css and .js files
        if ext not in ("css", "js"):
            # call the next middleware
            return next(req)
        # alrighty now we can try to read the file
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
        except FileNotFoundError:
            body = "<h1>404 Not Found</h1>"
            return Response(
                version="HTTP/1.1",
                code=404,
                reason="Not Found",
                headers={
                    "Content-Type": "text/html; charset=utf-8",
                    "Content-Length": str(len(body.encode("utf-8"))),
                },
                body=body,
            )
        #BUILD THE RESPONSE
        headers = {
            "Content-Type": MIME_TYPES[ext],
            "Content-Length": str(len(content.encode("utf-8"))),
        }
        return Response(
            version="HTTP/1.1",
            code=200,
            reason="OK",
            headers=headers,
            body=content,
        )
    return middleware # IMPORTANT: Don't forget to return middleware guys
def commonHeadersMiddlewareFactory(next):
    def middleware(req):
        res = next(req)
        # Add common headers
        res.headers["Server"] = "Ammon's Super Cool Server v0.1 alpha pre-release beta edition"
        res.headers["Date"] = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
        res.headers["Connection"] = "close"
        res.headers["Cache-Control"] = "max-age=5"
        if res.body is not None and "Content-Length" not in res.headers:
            res.headers["Content-Length"] = str(len(res.body.encode("utf-8")))
        return res
    return middleware # IMPORTANT: Don't forget to return middleware guys


###################################
# Middleware Chain Setup
###################################

def compose(endResultFunction, middlewareFactoriesList):
    handler = endResultFunction
    for factory in reversed(middlewareFactoriesList):
        handler = factory(handler)
    return handler



router = makeRouter(ROUTES)
handler = compose(
    router,
    [
        loggingMiddlewareFactory,
        staticFilesMiddlewareFactory,
        commonHeadersMiddlewareFactory,
    ],
)

###################################
#         Server Setup         #    
###################################
if __name__ == "__main__":
    print("[BOOT] starting server...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 8000))
        s.listen()
        print("[BOOT] listening on http://127.0.0.1:8000")

        while True:
            conn, addr = s.accept()
            with conn:
                try:
                    raw = conn.recv(8192)
                    if not raw:
                        continue
                    # parse the request
                    req = parseRequest(raw)
                    if req is None:
                        res = Response(
                            "HTTP/1.1", 400, "Bad Request",
                            {"Content-Type": "text/html; charset=utf-8"},
                            "<h1>400 Bad Request</h1>"
                        )
                    else:
                        res = HANDLER(req)
                     # encode and send the response
                    conn.send(encodeResponse(res))
                except Exception as e:
                    print("[ERROR]", repr(e))
                    conn.send(b"HTTP/1.1 500 Internal Server Error\r\nConnection: close\r\n\r\n")