
from typing import Dict, List
from jwt import DecodeError, ExpiredSignatureError, decode
from .exceptions import BearerInvalidTokenError
from .exceptions import InvalidTokenError
from .exceptions import ExpiredTokenError
from .configs import JWTConfigs
from .interfaces import TokenInterface
from .utils import decode64
import logging

logger = logging.getLogger(__name__)


class BearerToken(TokenInterface):
    def configure(self, configs: Dict) -> JWTConfigs:
        logger.info(
            "BearerToken:configure"
        )
        logger.info(f"{configs}")
        if (
                "SECRET_KEY" not in configs
                or "PUBLIC_KEY" not in configs
                or "PRIVATE_KEY" not in configs
        ):
            logger.info("Need secret key")
            raise RuntimeError(f"{self.__class__.__name__} need secret key")
        return JWTConfigs(
            JWT_ALGORITHM=configs["JWT_ALGORITHM"],
            JWT_SECRET=configs.get("SECRET_KEY", None),
            JWT_PRIVATE_KEY=configs.get("PRIVATE_KEY", None),
            JWT_PUBLIC_KEY=configs.get("PUBLIC_KEY", None),
            JWT_OPTIONS=configs.get("JWT_OPTIONS", None),
            JWT_KWARGS=configs.get("JWT_KWARGS", {}),
        )

    def parse_token(self, token: str) -> str:
        logger.info("BearerToken:parse_token")
        _token: List[str] = token.split(" ")
        bearer, token_value = _token
        if bearer.lower() != "bearer":
            logger.info("Bearer invalid token error.")
            raise BearerInvalidTokenError("Invalid Token")
        return token_value

    def get_data(self, token: str) -> Dict:
        logger.info("BearerToken:get_data")
        try:
            # logger.info("In try part.")
            configs: JWTConfigs = self.config
            key = (
                configs.JWT_SECRET
                if not configs.JWT_PUBLIC_KEY
                else configs.JWT_PUBLIC_KEY
            )
            claim: dict = decode(
                token,
                key=key,
                algorithms=[configs.JWT_ALGORITHM],
                options=configs.JWT_OPTIONS,
                audience=configs.JWT_KWARGS.get("JWT_AUDIENCE", None),
                issuer=configs.JWT_KWARGS.get("JWT_ISSUER", None),
            )
            return claim
        except DecodeError:
            logger.info("Decode error.")
            raise InvalidTokenError
        except ExpiredSignatureError:
            logger.info("Expired signature error.")
            raise ExpiredTokenError

    def __call__(self, token: str) -> Dict:
        logger.info("BearerToken:__call__")
        _token: str = self.parse_token(token)
        claim: dict = self.get_data(token=_token)
        return claim


class BasicToken(TokenInterface):
    def configure(self, configs: Dict) -> None:
        logger.info("BasicToken:configure")
        pass

    def parse_token(self, token: bytes) -> str:
        logger.info("BasicToken:parse_token")
        message: str = decode64(token)
        _token: List[str] = message.split(" ")
        bearer, token_value = _token
        if bearer.lower() != "basic":
            raise InvalidTokenError("Invalid Token")
        return token_value

    def get_token(self, token: str) -> Dict:
        logger.info("BasicToken:get_token")
        username, password = token.split(":")
        return dict(username=username, password=password)

    def __call__(self, token: bytes) -> Dict:
        logger.info("BasicToken:__call__")
        _token: str = self.parse_token(token)
        claim: dict = self.get_data(token=_token)
        return claim
