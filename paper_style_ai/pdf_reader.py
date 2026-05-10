"""PDF text extraction utilities."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable



@dataclass(frozen=True)
class ExtractedPage:
    """Text extracted from a single PDF page."""

    source: str
    page_number: int
    text: str


def extract_pdf_text(pdf_path: Path) -> list[ExtractedPage]:
    """Extract readable text from every page of one PDF file."""
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError(f"Expected a .pdf file, got: {pdf_path}")

    try:
        from pypdf import PdfReader
    except ModuleNotFoundError as exc:
        raise ModuleNotFoundError(
            "pypdf is required for PDF extraction. Install dependencies with: "
            "python -m pip install -r requirements.txt"
        ) from exc

    reader = PdfReader(str(pdf_path))
    pages: list[ExtractedPage] = []
    for index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        cleaned = "\n".join(line.strip() for line in text.splitlines() if line.strip())
        if cleaned:
            pages.append(ExtractedPage(source=str(pdf_path), page_number=index, text=cleaned))
    return pages


def extract_from_directory(pdf_dir: Path) -> list[ExtractedPage]:
    """Extract text from all PDFs under a directory in deterministic order."""
    if not pdf_dir.exists() or not pdf_dir.is_dir():
        raise NotADirectoryError(f"PDF directory not found: {pdf_dir}")

    pages: list[ExtractedPage] = []
    for pdf_path in sorted(pdf_dir.glob("**/*.pdf")):
        pages.extend(extract_pdf_text(pdf_path))
    return pages


def merge_pages(pages: Iterable[ExtractedPage]) -> str:
    """Merge extracted pages into one annotated corpus string."""
    blocks = [f"[SOURCE: {page.source} | PAGE: {page.page_number}]\n{page.text}" for page in pages]
    return "\n\n".join(blocks)
