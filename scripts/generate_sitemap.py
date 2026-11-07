"""Regenerate sitemap; opt in to inserting missing static canonical annotations."""
from seo import cli

if __name__ == "__main__":
    raise SystemExit(cli("generate"))
