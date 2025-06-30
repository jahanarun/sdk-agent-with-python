# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from fastapi import Request
from microsoft.agents.hosting.aiohttp import (
    CloudAdapter,
    # jwt_authorization_middleware,
    # start_agent_process,
)
from dotenv import load_dotenv
import json
from aiohttp.web import Application, Request, Response, json_response, run_app

from microsoft.agents.builder import (
    Agent,
    RestChannelServiceClientFactory
)
from microsoft.agents.authorization import (
    Connections,
    AccessTokenProviderBase,
    ClaimsIdentity,
)
from microsoft.agents.core.models import (
    Activity,
    DeliveryModes,
)
from microsoft.agents.authentication.msal import MsalAuth

from app.agents.empty.agent import EmptyAgent
from app.config import DefaultConfig

load_dotenv()

AUTH_PROVIDER = MsalAuth(DefaultConfig())


class DefaultConnection(Connections):
    def get_default_connection(self) -> AccessTokenProviderBase:
        pass

    def get_token_provider(
        self, claims_identity: ClaimsIdentity, service_url: str
    ) -> AccessTokenProviderBase:
        return AUTH_PROVIDER

    def get_connection(self, connection_name: str) -> AccessTokenProviderBase:
        pass


CONFIG = DefaultConfig()
CHANNEL_CLIENT_FACTORY = RestChannelServiceClientFactory(CONFIG, DefaultConnection())

# Create adapter.
ADAPTER = CloudAdapter(CHANNEL_CLIENT_FACTORY)

# Create the Agent
AGENT = EmptyAgent()


# Listen for incoming requests on /api/messages
async def messages(req: Request) -> Response:
    try:
        content_type = req.headers.get("Content-Type", "").lower()

        if "application/json" in content_type:
            body = await req.json()
        else:
            print("Invalid content type, returning 415")
            return Response(status=415)

        auth_header = req.headers["Authorization"] if "Authorization" in req.headers else ""
        claims: dict[str, str] = {}
        claims["aud"] = "all"
        claims_identity = ClaimsIdentity(
            claims=claims, is_authenticated=False, authentication_type="Anonymous"
        )

        activity = Activity(**body)
        adapter: CloudAdapter = req.app["adapter"]
        agent: Agent = req.app["agent"]

        invoke_response = await adapter.process_activity(
            activity=activity, claims_identity=claims_identity, callback=agent.on_turn
        )
        if (
            activity.type == "invoke"
            or activity.delivery_mode == DeliveryModes.expect_replies
        ):
            # Invoke and ExpectReplies cannot be performed async, the response must be written before the calling thread is released.
            return json_response(
                data=invoke_response.body, status=invoke_response.status
            )

        return Response(status=202)

    except Exception as error:
        print("Error processing request:", error)
        return Response(
            status=500,
            body=json.dumps({"error": str(error)}),
            headers={"Content-Type": "application/json"},
        )


APP = Application()
# APP = Application(middlewares=[jwt_authorization_middleware])
APP.router.add_post("/api/messages", messages)
APP["agent_configuration"] = CONFIG
APP["adapter"] = ADAPTER
APP["agent"] = AGENT

if __name__ == "__main__":
    try:
        run_app(APP, host="localhost", port=CONFIG.PORT)
    except Exception as error:
        raise error
    except Exception as error:
        raise error
