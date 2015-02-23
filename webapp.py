#!/usr/bin/env python3

"""
This tornado server creates the client app by serving html/css/js and
it also functions as the wsgi container for accepting survey form post
requests back from the client app.
"""
from sqlalchemy.orm import scoped_session

from tornado.escape import json_encode
import tornado.web
import tornado.ioloop
import tornado.httpserver

import api.aggregation
import api.survey
import api.submission
import api.user
from db import engine
from pages.api.aggregations import AggregationHandler
from pages.auth import LogoutHandler, LoginHandler
from pages.api.submissions import SubmissionsAPIHandler, \
    SingleSubmissionAPIHandler, SubmitAPIHandler
from pages.api.surveys import SurveysAPIHandler, SingleSurveyAPIHandler, \
    CreateSurveyAPIHandler
from pages.util.base import BaseHandler, get_json_request_body
import pages.util.ui
from pages.debug import DebugLoginHandler, DebugLogoutHandler, \
    DebugUserCreationHandler
from pages.view.surveys import ViewHandler
from pages.view.submissions import ViewSubmissionsHandler, \
    ViewSubmissionHandler
from pages.view.visualize import VisualizationHandler
import settings
from utils.logger import setup_custom_logger
from db.survey import SurveyPrefixDoesNotIdentifyASurveyError, \
    SurveyPrefixTooShortError, \
    get_survey_id_from_prefix, get_surveys_by_email


logger = setup_custom_logger('dokomo')


class Index(BaseHandler):
    def get(self, msg=""):
        surveys = get_surveys_by_email(self.db, self.current_user, 10)
        self.render('index.html', message=msg, surveys=surveys)

    def post(self):
        LogoutHandler.post(self)  # TODO move to js
        self.get("You logged out")


class Survey(BaseHandler):
    def get(self, survey_prefix: str):
        try:
            survey_id = get_survey_id_from_prefix(self.db, survey_prefix)
            if len(survey_prefix) < 36:
                self.redirect('/survey/{}'.format(survey_id), permanent=False)
            else:
                survey = api.survey.display_survey(self.db, survey_id)[
                    'result']
                self.render('survey.html',
                            survey=json_encode(survey),
                            survey_title=survey['survey_title'])
        except (SurveyPrefixDoesNotIdentifyASurveyError,
                SurveyPrefixTooShortError):
            raise tornado.web.HTTPError(404)

    def post(self, uuid):
        SubmitAPIHandler.post(self, uuid)  # TODO: Hey Abdi kill this


class APITokenGenerator(BaseHandler):  # pragma: no cover
    @tornado.web.authenticated
    def get(self):
        # self.render('api-token.html')
        self.write(
            api.user.generate_token(self.db, {'email': self.current_user}))

    @tornado.web.authenticated
    def post(self):
        data = get_json_request_body(self)
        self.write(api.user.generate_token(self.db, data))


config = {
    'template_path': 'templates',
    'static_path': 'static',
    'login_url': '/',
    'ui_methods': pages.util.ui,
    'debug': settings.APP_DEBUG
}

use_xsrf_cookies = True
# If TEST_USER is set, don't use XSRF tokens
try:  # pragma: no cover
    _ = settings.TEST_USER
    config['xsrf_cookies'] = False
except AttributeError:
    config['xsrf_cookies'] = True
    config['cookie_secret'] = settings.COOKIE_SECRET

UUID_REGEX = '[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][' \
             'a-f0-9]{3}-?[a-f0-9]{12}'

pages = [
    # Dokomo Forms
    (r'/', Index),

    # View surveys and submissions
    (r'/view/?', ViewHandler),
    (r'/view/({})/?'.format(UUID_REGEX), ViewSubmissionsHandler),
    (r'/view/submission/({})/?'.format(UUID_REGEX),
     ViewSubmissionHandler),

    (r'/visualize/({})/?'.format(UUID_REGEX), VisualizationHandler),

    # Survey Submissions
    (r'/survey/(.+)/?', Survey),

    # Auth
    (r'/user/login/persona/?', LoginHandler),  # Post to Persona here

    # API tokens
    (r'/user/generate-api-token/?', APITokenGenerator),

    # JSON API
    (r'/api/aggregate/({})/?'.format(UUID_REGEX), AggregationHandler),
    (r'/api/surveys/?', SurveysAPIHandler),
    (r'/api/surveys/create/?', CreateSurveyAPIHandler),
    (r'/api/surveys/({})/?'.format(UUID_REGEX),
     SingleSurveyAPIHandler),
    (r'/api/surveys/({})/submit/?'.format(UUID_REGEX),
     SubmitAPIHandler),
    (r'/api/surveys/({})/submissions/?'.format(UUID_REGEX),
     SubmissionsAPIHandler),
    (r'/api/submissions/({})/?'.format(UUID_REGEX),
     SingleSubmissionAPIHandler),
]

if config.get('debug', False):
    pages += [(r'/debug/create/(.+)/?', DebugUserCreationHandler),
              (r'/debug/login/(.+)/?', DebugLoginHandler),
              (r'/debug/logout/?', DebugLogoutHandler), ]


class Application(tornado.web.Application):  # pragma: no cover
    def __init__(self, handlers=None, default_host="", transforms=None,
                 **configs):
        if handlers is None:
            handlers = pages
        if not configs:
            configs = config
        tornado.web.Application.__init__(self, handlers, default_host,
                                         transforms, **configs)

        self.db = engine.connect()


scoped_session
if __name__ == '__main__':  # pragma: no cover
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(settings.WEBAPP_PORT, '0.0.0.0')

    logger.info('starting server on port ' + str(settings.WEBAPP_PORT))

    tornado.ioloop.IOLoop.current().set_blocking_log_threshold(1)
    tornado.ioloop.IOLoop.current().start()
