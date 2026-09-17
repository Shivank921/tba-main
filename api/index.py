"""Vercel serverless entrypoint.

Vercel's Python runtime auto-detects this file (/api/index.py) as a
serverless function and serves the exported ASGI `app`.
All /api/* traffic is routed here via vercel.json.
"""
import sys
from pathlib import Path

# Make the FastAPI backend importable
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'backend'))

from server import app  # noqa: E402  # FastAPI ASGI app — picked up by Vercel
