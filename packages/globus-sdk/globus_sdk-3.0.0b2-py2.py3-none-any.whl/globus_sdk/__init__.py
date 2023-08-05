import logging

from .authorizers import (
    AccessTokenAuthorizer,
    BasicAuthorizer,
    ClientCredentialsAuthorizer,
    NullAuthorizer,
    RefreshTokenAuthorizer,
)
from .client import BaseClient
from .exc import (
    GlobusAPIError,
    GlobusConnectionError,
    GlobusConnectionTimeoutError,
    GlobusError,
    GlobusSDKUsageError,
    GlobusTimeoutError,
    NetworkError,
)
from .local_endpoint import LocalGlobusConnectPersonal
from .response import GlobusHTTPResponse
from .services import (
    AuthAPIError,
    AuthClient,
    ConfidentialAppAuthClient,
    DeleteData,
    GroupsAPIError,
    GroupsClient,
    IdentityMap,
    NativeAppAuthClient,
    SearchAPIError,
    SearchClient,
    SearchQuery,
    TransferAPIError,
    TransferClient,
    TransferData,
)
from .version import __version__

__all__ = (
    "__version__",
    "BaseClient",
    "GlobusHTTPResponse",
    "GlobusError",
    "GlobusSDKUsageError",
    "GlobusAPIError",
    "AuthAPIError",
    "TransferAPIError",
    "SearchAPIError",
    "GroupsAPIError",
    "NetworkError",
    "GlobusConnectionError",
    "GlobusTimeoutError",
    "GlobusConnectionTimeoutError",
    "NullAuthorizer",
    "BasicAuthorizer",
    "AccessTokenAuthorizer",
    "RefreshTokenAuthorizer",
    "ClientCredentialsAuthorizer",
    "AuthClient",
    "NativeAppAuthClient",
    "ConfidentialAppAuthClient",
    "IdentityMap",
    "TransferClient",
    "TransferData",
    "DeleteData",
    "SearchClient",
    "SearchQuery",
    "GroupsClient",
    "LocalGlobusConnectPersonal",
)


# configure logging for a library, per python best practices:
# https://docs.python.org/3/howto/logging.html#configuring-logging-for-a-library
logging.getLogger("globus_sdk").addHandler(logging.NullHandler())
