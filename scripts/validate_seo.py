"""Read-only validation of canonical pages, sitemap freshness and robots policy."""
from seo import cli

if __name__ == "__main__":
    raise SystemExit(cli("validate"))
