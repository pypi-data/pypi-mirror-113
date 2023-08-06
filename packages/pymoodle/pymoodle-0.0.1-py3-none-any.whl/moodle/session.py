import base64
import hashlib
import html
import json
import re
import secrets
import xml.etree.ElementTree
from typing import Any, Container, Dict, Iterable, Mapping, Text, Tuple, Union

from requests.adapters import BaseAdapter
from requests.models import PreparedRequest, Response
from requests.sessions import Session

from moodle.constants import LoginType


class MoodleException(Exception):
    pass


class MoodleAdapter(BaseAdapter):
    def send(
        self,
        request: PreparedRequest,
        stream: bool = False,
        timeout: Union[float, Tuple[float, float], Tuple[float, None]] = None,
        verify: Union[bool, str] = True,
        cert: Union[Union[bytes, Text], Container[Union[bytes, Text]]] = None,
        proxies: Mapping[str, str] = None,
    ) -> Response:
        response = Response()
        response.url = request.url or ""
        response.status_code = 200
        response.reason = "OK"

        return response

    def close(self) -> None:
        return


class MoodleSession(Session):
    def __init__(
        self, moodle_url: str, wstoken: str = "", *, restformat: str = "json"
    ) -> None:
        super().__init__()
        self.mount("moodlemobile://", MoodleAdapter())
        self.moodle_url = moodle_url
        self.wstoken = wstoken
        self.restformat = restformat

        self.public_config = self.ajax(
            [{"methodname": "tool_mobile_get_public_config", "args": {}}]
        )[0]["data"]

        if (
            not self.public_config["enablewebservices"]
            or not self.public_config["enablemobilewebservice"]
        ):
            raise RuntimeError("Cannot work without webservices enabled")

    def login(self, username: str, password: str) -> None:
        if self.public_config["typeoflogin"] == LoginType.LOGIN_VIA_APP:
            raise ValueError("Login type currently not supported")

        redirect_page = self.post(
            self.get(self.public_config["identityproviders"][0]["url"]).url,
            data={
                "j_username": username,
                "j_password": password,
                "_eventId_proceed": "",
            },
        )

        form = re.search(
            r'<form action="(?P<form_submit_url>[^"]*)" method="post">'
            r'.*<input type="hidden" name="RelayState" value="(?P<RelayState>[^"]*)"/>'
            r'.*<input type="hidden" name="SAMLResponse" value="(?P<SAMLResponse>[^"]*)"/>',
            html.unescape(redirect_page.text),
            flags=re.MULTILINE | re.DOTALL,
        )

        if not form:
            raise RuntimeError("Login failed")

        self.post(form["form_submit_url"], data=form.groupdict())

        self.wstoken = self.get_wstoken()

    def get_wstoken(self) -> str:
        passport = secrets.token_urlsafe()

        token_response = self.get(
            self.public_config["launchurl"],
            params={"service": "moodle_mobile_app", "passport": passport},
        )

        token_encoded = token_response.url[len("moodlemobile://token=") :]
        token_decoded = base64.b64decode(token_encoded).decode()
        signature, token, *_ = token_decoded.split(":::")

        signature_content = (self.moodle_url + passport).encode()
        expected_signature = hashlib.md5(signature_content).hexdigest()

        if signature != expected_signature:
            raise ValueError("Invalid signature")

        return token

    def ajax(self, requests: Iterable[Dict[str, Any]]) -> Any:
        indexed_requests = [
            {"index": i, "methodname": req["methodname"], "args": req["args"]}
            for i, req in enumerate(requests)
        ]

        # params={"info": ",".join(req["methodname"] for req in indexed_requests)},
        return self.post(
            f"{self.moodle_url}/lib/ajax/service.php",
            data=json.dumps(indexed_requests),
        ).json()

    def webservice(self, wsfunction: str, data: dict = None) -> Any:
        if data is None:
            data = {}

        data.update()
        response = self.post(
            f"{self.moodle_url}/webservice/rest/server.php",
            data={
                "moodlewsrestformat": self.restformat,
                "wstoken": self.wstoken,
                "wsfunction": wsfunction,
                **flatten(data),
            },
        )

        if self.restformat == "json":
            response_data = response.json()
            if response_data and "exception" in response_data:
                raise MoodleException(response_data)
            return response_data
        if self.restformat == "xml":
            return xml.etree.ElementTree.fromstring(response.text)
        return response


def flatten(data: dict, prefix: str = "") -> Dict[str, Any]:
    formatted_data = {}

    for key, value in data.items():
        new_key = f"{prefix}[{key}]" if prefix else key

        if isinstance(value, dict):
            formatted_data.update(flatten(value, prefix=new_key))
        elif isinstance(value, list) and not isinstance(value, str):
            formatted_data.update(flatten(dict(enumerate(value)), prefix=new_key))
        else:
            formatted_data[new_key] = value

    return formatted_data
