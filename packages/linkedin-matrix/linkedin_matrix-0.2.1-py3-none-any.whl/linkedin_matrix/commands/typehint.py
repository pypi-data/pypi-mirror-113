from typing import TYPE_CHECKING

from mautrix.bridge.commands import CommandEvent as BaseCommandEvent

if TYPE_CHECKING:
    from ..__main__ import LinkedInBridge
    from ..user import User


class CommandEvent(BaseCommandEvent):
    bridge: "LinkedInBridge"
    sender: "User"
