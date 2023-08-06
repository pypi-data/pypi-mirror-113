"""Module with the About resources."""

from flask_restx import Resource

from notelist.apis import about_api
from notelist.resources import (
    ResponseData, get_response_data, get_response_codes)


API_NAME = "Notelist"
API_VERSION = "0.2.2"
API_DESCRIPTION = "Tag based note taking REST API"
API_AUTHOR = "Jose A. Jimenez"
API_INFO_RETRIEVED = "API information retrieved."


@about_api.route("/about")
class AboutResource(Resource):
    """About resource."""

    @about_api.doc(responses=get_response_codes(200, 500))
    def get(self) -> ResponseData:
        """Get information about the API."""
        info = {
            "name": API_NAME,
            "version": API_VERSION,
            "description": API_DESCRIPTION,
            "author": API_AUTHOR}

        return get_response_data(API_INFO_RETRIEVED, info), 200
