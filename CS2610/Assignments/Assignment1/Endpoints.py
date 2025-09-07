from RequestandResponse import Response

def readTemplate(fileName):
    path = "templates/" + fileName
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "<h1>Template not FOund</h1>"
def indexEndpoint(req):
    body = readTemplate("index.html")
    return Response(
        version="HTTP/1.1",
        code=200,
        reason="OK",
        headers={
            "Content-Type": "text/html; charset=utf-8",
            "Content-Length": str(len(body.encode("utf-8"))),
        },
        body=body,
    )

def aboutEndpoint(req):
    body = readTemplate("about.html")
    return Response(
        version="HTTP/1.1",
        code=200,
        reason="OK",
        headers={
            "Content-Type": "text/html; charset=utf-8",
            "Content-Length": str(len(body.encode("utf-8"))),
        },
        body=body,
    )
def experienceEndpoint(req):
    body = readTemplate("experience.html")
    return Response(
        version="HTTP/1.1",
        code=200,
        reason="OK",
        headers={
            "Content-Type": "text/html; charset=utf-8",
            "Content-Length": str(len(body.encode("utf-8"))),
        },
        body=body,
    )
def projectsEndpoint(req):
    body = readTemplate("projects.html")
    return Response(
        version="HTTP/1.1",
        code=200,
        reason="OK",
        headers={
            "Content-Type": "text/html; charset=utf-8",
            "Content-Length": str(len(body.encode("utf-8"))),
        },
        body=body,
    )

def infoEndpoint(req):
    # 301 redirect to /about
    return Response(
        version="HTTP/1.1",
        code=301,
        reason="Moved Permanently",
        headers={
            "Location": "/about",
            "Content-Length": "0",
        },
        body="",
    )