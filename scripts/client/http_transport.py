"""HTTP transport layer for Imobzi API."""

import httpx
from scripts.client.configuration import ImobziConfiguration
from scripts.domain.exceptions import (
    ProviderTransportException,
    PropertyNotFoundException,
)


class ImobziHttpTransport:
    """Handles HTTP requests with mandatory origin headers and error handling."""

    def __init__(
        self,
        configuration: ImobziConfiguration,
        http_client: httpx.Client,
    ) -> None:
        """Initialize transport with configuration and client."""
        self._configuration = configuration
        self._http_client = http_client

    def _build_default_headers(self) -> dict[str, str]:
        """Build origin validation headers required by Imobzi gateway."""
        origin_url = self._configuration.origin_header_value()
        referer_url = self._configuration.referer_header_value()
        agent = "Mozilla/5.0 (Central-Rental-Research-MCP/1.0)"
        return {
            "Origin": origin_url,
            "Referer": referer_url,
            "User-Agent": agent,
        }

    def _check_status(self, response: httpx.Response) -> None:
        """Verify response status code and throw specific domain exceptions."""
        status = response.status_code
        if status == 200:
            return
        if status == 404:
            raise PropertyNotFoundException("Requested resource was not found on Imobzi.")
        message = f"HTTP request failed with status code {status}: {response.text[:120]}"
        raise ProviderTransportException(message)

    def get_json(self, url: str, parameters: dict | None = None) -> dict | list:
        """Execute HTTP GET request and return parsed JSON payload."""
        headers = self._build_default_headers()
        try:
            response = self._http_client.get(url, params=parameters, headers=headers)
        except httpx.HTTPError as error:
            error_message = f"Transport network error: {error}"
            raise ProviderTransportException(error_message) from error
        self._check_status(response)
        return response.json()
