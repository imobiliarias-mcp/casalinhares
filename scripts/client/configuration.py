"""Configuration settings for Imobzi API client."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ImobziConfiguration:
    """Holds configuration parameters for Imobzi API communication."""

    base_hostname: str = "www.casalinhares.com.br"
    api_base_url: str = "https://api2.imobzi.app/v1"

    def origin_header_value(self) -> str:
        """Return the origin header required by Cloudflare gateway."""
        return f"https://{self.base_hostname}"

    def referer_header_value(self) -> str:
        """Return the referer header value."""
        return f"https://{self.base_hostname}/"
