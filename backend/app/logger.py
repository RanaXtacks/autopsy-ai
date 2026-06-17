import logging
import sys
from flask import has_request_context, request


class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
            record.method = request.method
        else:
            record.url = None
            record.remote_addr = None
            record.method = None
        return super().format(record)


def setup_logging(app):
    log_level = getattr(logging, app.config['LOG_LEVEL'], logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)

    formatter = RequestFormatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(remote_addr)s - %(method)s - %(url)s - %(message)s'
    )
    handler.setFormatter(formatter)

    app.logger.addHandler(handler)
    app.logger.setLevel(log_level)

    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.addHandler(handler)
    werkzeug_logger.setLevel(log_level)

    sqlalchemy_logger = logging.getLogger('sqlalchemy.engine')
    sqlalchemy_logger.addHandler(handler)
    sqlalchemy_logger.setLevel(logging.WARNING)

    return app.logger
