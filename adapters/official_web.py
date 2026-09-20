"""Thin facade over source_engine official_web extraction."""

from source_engine.extract import extract_domains
from source_engine.fetch import fetch

__all__ = ["fetch", "extract_domains"]
