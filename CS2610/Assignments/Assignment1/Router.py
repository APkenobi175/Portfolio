from datetime import datetime
from RequestandResponse import Response

#################################
#          Router Maker         #
#################################
def makeRouter(routes):
    def router (req):
        endpoint = routes.get(req.uri)
        if endpoint is None:
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
        return endpoint(req)
    return router

