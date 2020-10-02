from datetime import datetime, timedelta
import json
import os

from aiohttp import ClientSession
import betamax
import pytest

from xbox.webapi.api.client import XboxLiveClient
from xbox.webapi.authentication.manager import AuthenticationManager
from xbox.webapi.authentication.models import XSTSDisplayClaims, XSTSResponse

current_dir = os.path.dirname(__file__)

with betamax.Betamax.configure() as config:
    config.cassette_library_dir = os.path.join(current_dir, "data/cassettes")
    config.default_cassette_options["record_mode"] = "none"


@pytest.fixture(scope="session")
def redirect_url():
    return (
        "https://login.live.com/oauth20_desktop.srf?lc=1033#access_token=AccessToken&token_type=bearer&"
        "expires_in=86400&scope=service::user.auth.xboxlive.com::MBI_SSL&refresh_token=RefreshToken&"
        "user_id=1005283eaccf208b"
    )


@pytest.fixture(scope="session")
def jwt():
    return (
        "eyJlSGVsbG9JYW1BVGVzdFRva2VuSnVzdEZvclRoZXNlVW5pdFRlc3Rz"
        "X0hvcGVmdWxseUFsbFRoZVRlc3RzVHVybk91dEdvb2RfR29vZEx1Y2s="
    )


@pytest.fixture(scope="session")
def token_datetime():
    return datetime(year=2099, month=10, day=11, hour=1)


@pytest.fixture(scope="session")
def token_timestring():
    return "2099-10-11T01:00:00.000000Z"


@pytest.fixture(scope="session")
def token_expired_timestring():
    return "2000-10-11T01:00:00.000000Z"


@pytest.fixture(scope="session")
def windows_live_authenticate_response():
    filepath = os.path.join(current_dir, "data", "wl_auth_response.html")
    with open(filepath) as f:
        return f.read()


@pytest.fixture(scope="session")
def windows_live_authenticate_response_two_js_obj():
    filepath = os.path.join(current_dir, "data", "wl_auth_response_two_js_obj.html")
    with open(filepath) as f:
        return f.read()


@pytest.fixture(scope="session")
def tokens_filepath():
    filepath = os.path.join(current_dir, "data", "tokens.json")
    return filepath


@pytest.fixture(scope="session")
def tokens_json(tokens_filepath):
    with open(tokens_filepath) as f:
        return json.load(f)


@pytest.fixture(scope="session")
def xsts_token():
    return XSTSResponse(
        issue_instant=datetime.utcnow(),
        not_after=datetime.utcnow() + timedelta(hours=16),
        token="123456789",
        display_claims=XSTSDisplayClaims(
            xui=[{"xid": "2669321029139235", "uhs": "abcdefg"}]
        ),
    )


@pytest.fixture(scope="function")
async def xbl_client(event_loop):
    auth_mgr = AuthenticationManager(
        ClientSession(loop=event_loop), "abc", "123", "http://localhost"
    )
    auth_mgr.xsts_token = XSTSResponse(
        issue_instant=datetime.utcnow(),
        not_after=datetime.utcnow() + timedelta(hours=16),
        token="123456789",
        display_claims=XSTSDisplayClaims(
            xui=[{"xid": "2669321029139235", "uhs": "abcdefg"}]
        ),
    )
    return XboxLiveClient(auth_mgr)
