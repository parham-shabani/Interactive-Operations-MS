from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class JWTConfigs:
    JWT_ALGORITHM: str
    JWT_SECRET: Optional[str] = None
    JWT_PUBLIC_KEY: Optional[str] = None
    JWT_PRIVATE_KEY: Optional[str] = None
    JWT_OPTIONS: Optional[Dict] = None
    JWT_HEADERS: Optional[Dict] = None
    JWT_KWARGS: Optional[Dict] = None
