import logging
from logging.handlers import RotatingFileHandler
from flask import has_request_context, request
from datetime import datetime


class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.remote_addr = request.remote_addr
            record.request_path = request.path
        else:
            record.remote_addr = None
            record.request_path = None
        return super().format(record)


def setup_logging(app):
    # Minimal file-based logging with rotation. In production, forward logs to SIEM.
    handler = RotatingFileHandler("audit.log", maxBytes=10 * 1024 * 1024, backupCount=5)
    fmt = (
        "%(asctime)s [%(levelname)s] %(remote_addr)s %(request_path)s %(message)s"
    )
    handler.setFormatter(RequestFormatter(fmt))
    handler.setLevel(logging.INFO)
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(handler)
