from django.utils.translation import gettext_lazy as _
from core.exceptions import exceptions as base_exceptions
import re
import ipaddress
import logging

logger = logging.getLogger(__name__)


def is_valid_ip_ipv4_or_ipv6(query: str) -> bool:
    """
    Checks whether the input value is a valid IP address (IPv4 or IPv6).

    Args:
        query (str): Input value to check

    Returns:
        bool: `True` if the address is valid, `False` otherwise
    """
    try:
        ipaddress.ip_address(query)
        return True
    except ValueError:
        return False
