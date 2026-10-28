"""Shared validation for browser settings and server-side model clients."""

import os

MIN_CHUNK_SIZE = 256
MAX_CHUNK_SIZE = 8192
MAX_CHUNK_OVERLAP = 2048

CHAT_MODES = {
    "compact",
    "refine",
    "tree_summarize",
    "simple_summarize",
    "accumulate",
    "compact_accumulate",
}


def bounded_integer(value, minimum, maximum, label):
    # Limit input length before integer conversion.
    if isinstance(value, bool) or not isinstance(value, (int, str)):
        raise ValueError(f"{label} must be an integer.")
    if isinstance(value, str) and (
        len(value) > 5 or not value.isascii() or not value.isdecimal()
    ):
        raise ValueError(f"{label} must be an integer.")
    number = int(value)
    if not minimum <= number <= maximum:
        raise ValueError(f"{label} must be between {minimum} and {maximum}.")
    return number


def validate_chunk_settings(chunk_size, chunk_overlap):
    size = bounded_integer(chunk_size, MIN_CHUNK_SIZE, MAX_CHUNK_SIZE, "Chunk Size")
    overlap = bounded_integer(chunk_overlap, 0, MAX_CHUNK_OVERLAP, "Chunk Overlap")
    if overlap > size // 2:
        raise ValueError("Chunk Overlap must be at most half of Chunk Size.")
    return size, overlap
