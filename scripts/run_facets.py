import sys
from pathlib import Path

repo_root = str(Path(__file__).resolve().parent.parent)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from scripts.providers.casalinhares import CasaLinharesRentalProvider


def print_section(title: str, items: tuple[str, ...]) -> None:
    """Print an item collection section to stdout."""
    print(f"\n--- {title} ({len(items)}) ---")
    for item in items:
        print(f"  • {item}")


def main() -> None:
    """Main execution function."""
    provider = CasaLinharesRentalProvider.create_default()
    facets = provider.get_facets()
    cities = facets.city_names()
    neighborhoods = facets.neighborhood_names()

    print("\n" + "=" * 65)
    print("Filtros e Localidades Disponíveis para Locação - Casa Linhares")
    print("=" * 65)
    print_section("Cidades", cities)
    print_section("Bairros", neighborhoods)
    print("\n" + "=" * 65 + "\n")


if __name__ == "__main__":
    main()
