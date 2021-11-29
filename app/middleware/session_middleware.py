import logging
import sqlalchemy.orm.scoping as scoping
from sqlalchemy.exc import SQLAlchemyError
from falcon import HTTPInternalServerError


class SessionMiddleware(object):
    def __init__(self, db_session):
        self._session_factory = db_session
        self._scoped = isinstance(db_session, scoping.ScopedSession)

    def process_request(self, req, res, resource=None, params=None):
        """
        Handle post-processing of the response (after routing).
        """
        req.context.session = self._session_factory()

    def process_response(self, req, res, resource=None, req_succeeded=True):
        """
        Handle post-processing of the response (after routing).
        """
        if 'session' not in req.context:
            return

        session = req.context.session
        # auto-commit changes
        try:
            if req_succeeded:
                session.commit()
        except SQLAlchemyError as ex:
            logging.getLogger('API').error(ex, exc_info=True)
            session.rollback()
            raise HTTPInternalServerError(
                title='Database Error', description='Please check logs') from ex

        if self._scoped:
            session.rollback()
        else:
            session.close()
