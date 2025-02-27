"""Stripe Agent Toolkit."""

from typing import List
from pydantic import PrivateAttr

from ..api import StripeAPI
from ..tools import tools
from ..configuration import Configuration, is_tool_allowed
from .tool import StripeTool


class StripeAgentToolkit:
    _tools: List = PrivateAttr(default=[])

    def __init__(self, secret_key: str, configuration: Configuration = None):
        super().__init__()

        stripe_api = StripeAPI(secret_key=secret_key)

        filtered_tools = [
            tool for tool in tools if is_tool_allowed(tool, configuration)
        ]

        self._tools = [
            StripeTool(
                name=tool["name"],
                description=tool["description"],
                method=tool["method"],
                stripe_api=stripe_api,
                args_schema=tool.get("args_schema", None),
            )
            for tool in filtered_tools
        ]

    def get_tools(self) -> List:
        """Get the tools in the toolkit."""
        return self._tools
