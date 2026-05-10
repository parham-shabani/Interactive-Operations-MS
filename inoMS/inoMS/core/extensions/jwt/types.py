from __future__ import annotations
from typing import Any, Dict, NewType, Type

Token = NewType("Token", str)
Payload = NewType("Payload", Dict[str, Any])
Headers = NewType("Headers", Dict[str, Any])
AccessToken = NewType("AccessToken", Token)
RefreshToken = NewType("RefreshToken", Token)
