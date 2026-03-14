from copy import deepcopy
from datetime import datetime, timedelta, timezone
from json import JSONEncoder
from .types import Token
from .types import Payload
from .types import Headers
from typing import Any, Dict, List, Optional, Type
from jwt import encode
from jwt import decode
import logging

logger = logging.getLogger(__name__)


class JwtManager:
    def __init__(
            self,
            key: str,
            access_token_expire: timedelta,
            refresh_token_expire: timedelta,
            algorithm: str | None = "HS256",
    ) -> None:
        self.key: str = key
        self.algorithm: str | None = algorithm
        self.access_token_expire: timedelta = access_token_expire
        self.refresh_token_expire: timedelta = refresh_token_expire

    def encode(
            self,
            payload: Payload,
            key: str | None = None,
            algorithm: str | None = None,
            headers: Dict | None = None,
            json_encoder: Type[JSONEncoder] | None = None,
    ) -> str:
        return encode(
            payload=payload,
            key=key or self.key,
            algorithm=algorithm or self.algorithm,
            headers=headers,
            json_encoder=json_encoder,
        )

    def decode(
            self,
            jwt: Token,
            key: str | None = None,
            algorithms: List[str] | None = None,
            options: Dict | None = None,
            **kwargs: Any,
    ) -> Dict | Payload:
        algos: List[str] = []
        if self.algorithm:
            algos.append(self.algorithm)
        return decode(
            jwt=jwt,
            key=key or self.key,
            algorithms=algorithms or algos,
            options=options,
            **kwargs,
        )

    def generate_access_token(
            self,
            payload: Payload | Dict[str, str],
            headers: Optional[Headers] = None,
    ) -> str:
        logger.info(
            "Start generate access token method in JwtManager in manager in jwt in extensions in core app"
        )
        logger.info(f"{payload}:{headers}")
        claim: Payload = deepcopy(payload)
        now: datetime = datetime.now(timezone.utc)
        exp: datetime = now + self.access_token_expire
        if now > exp:
            claim.update({"exp": self.access_token_expire})
        else:
            claim.update({"exp": exp})
        return self.encode(payload=claim, headers=headers)

    def generate_refresh_token(
            self,
            payload: Payload,
    ) -> str:
        logger.info("Start generate refresh token method")
        claim: Payload = deepcopy(payload)
        now: datetime = datetime.now(timezone.utc)
        exp: datetime = now + self.refresh_token_expire
        if now > exp:
            claim.update({"exp": self.refresh_token_expire})
        else:
            claim.update({"exp": exp})
        return self.encode(payload=claim)
