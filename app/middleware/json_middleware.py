import falcon

from app.log import get_logger
LOG = get_logger()


class JSONMiddleware:
    def process_request(self, req, resp, resource=None, params=None):
        # for backward compatibility
        LOG.info(req.content_type)
        if req.content_type and falcon.MEDIA_JSON in req.content_type:
            req.context.doc = req.media

    def process_response(self, req, resp, resource, req_succeeded):
        # for backward compatibility
        if 'result' in req.context:
            resp.media = req.context.result
