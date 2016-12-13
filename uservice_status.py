#!/usr/bin/env python
"""Minimal service providing proxying for status.lsst.codes with metadata"""
import requests
from apikit import APIFlask as apf


def main():
    """Create the app and then run it."""
    app = apf(name="uservice-status",
              version="0.0.1",
              repository="https://github.com/sqre-lsst/sqre-uservice-status",
              description="API wrapper for status data")

    @app.route("/")
    @app.route("/status.json")
    # pylint: disable=unused-variable
    def get_status():
        """Proxy for status.lsst.codes"""
        # So, yeah, proxying an unauthenticated service, just to add some
        #  metadata.
        return requests.get("https://status.lsst.codes/status.json").text
    app.run()

if __name__ == "__main__":
    main()
