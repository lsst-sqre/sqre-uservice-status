#!/usr/bin/env python
"""Minimal service providing proxying for status.lsst.codes with metadata."""
import requests
from apikit import APIFlask as APF
from apikit import BackendError
from flask import jsonify


def server(run_standalone=False):
    """Create the app and then run it."""
    # Add "/status" for mapping behind api.lsst.codes
    app = APF(name="uservice-status",
              version="0.0.9",
              repository="https://github.com/sqre-lsst/sqre-uservice-status",
              description="API wrapper for status data",
              route=["/", "/status"])

    @app.route("/")
    def root_route():
        """Add low-overhead route for Ingress healthchecks."""
        return "OK"

    @app.route("/status")
    @app.route("/status/")
    @app.route("/status.json")
    # pylint: disable=unused-variable
    def get_status():
        """Proxy for status.lsst.codes"""
        # So, yeah, proxying an unauthenticated service, just to add some
        #  metadata.
        resp = requests.get("https://status.lsst.codes/status.json")
        if resp.status_code == 200:
            return resp.text
        else:
            raise BackendError(reason=resp.reason,
                               status_code=resp.status_code,
                               content=resp.text)

    @app.errorhandler(BackendError)
    # pylint: disable=unused-variable
    def handle_invalid_usage(error):
        """Custom error handler."""
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response
    if run_standalone:
        app.run(host='0.0.0.0', threaded=True)
    # Otherwise, we're being called under uwsgi, so cough up the app.
    return app


def standalone():
    """Entry point for running as its own executable."""
    server(run_standalone=True)


if __name__ == "__main__":
    standalone()
