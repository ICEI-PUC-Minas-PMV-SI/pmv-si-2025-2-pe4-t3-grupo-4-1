import hashlib
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse

class ETagListMixinMiddleware(MiddlewareMixin):
    """
    Adds a weak ETag for GET list responses to improve client caching.
    Safe and simple heuristic: if response is JSON and small enough, hash body.
    """
    def process_response(self, request, response: HttpResponse):
        if request.method == "GET" and response.get("Content-Type", "").startswith("application/json") and response.get("ETag") is None:
            body = getattr(response, "content", b"")
            if body and len(body) < 2_000_000:
                etag = 'W/"' + hashlib.md5(body).hexdigest() + '"'
                response["ETag"] = etag
                # Let clients use If-None-Match automatically via Django
        return response
