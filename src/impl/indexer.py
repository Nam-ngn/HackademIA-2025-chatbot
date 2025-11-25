import csv
import json
import os
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List

import requests
from ..interface.base_datastore import DataItem
from ..interface.base_indexer import BaseIndexer
from docling.document_converter import DocumentConverter
from docling.chunking import HybridChunker, DocChunk


FIELD_ORDER = [
    "Nom_fr",
    "Description_fr",
    "Adresse",
    "Sites",
    "Email",
    "Facebook",
    "Instagram",
    "X(ex-Twitter)",
    "Telegram",
    "Youtube",
    "LinkedIn",
    "Discord",
    "Github",
    "Logo",
]


class Indexer(BaseIndexer):
    def __init__(self):
        self.converter = DocumentConverter()
        self.chunker = HybridChunker()
        # Disable tokenizers parallelism to avoid OOM errors.
        os.environ["TOKENIZERS_PARALLELISM"] = "false"

    def index(self, document_paths: List[str]) -> List[DataItem]:
        items: List[DataItem] = []
        for document_path in document_paths:
            if self._is_url(document_path):
                items.extend(self._index_http(document_path))
                continue

            suffix = Path(document_path).suffix.lower()
            if suffix == ".csv":
                items.extend(self._index_csv(document_path))
            else:
                items.extend(self._index_document(document_path))
        return items

    def _index_document(self, document_path: str) -> List[DataItem]:
        document = self.converter.convert(document_path).document
        chunks: List[DocChunk] = self.chunker.chunk(document)
        return self._items_from_chunks(chunks)

    def _items_from_chunks(self, chunks: List[DocChunk]) -> List[DataItem]:
        items = []
        for i, chunk in enumerate(chunks):
            content_headings = "## " + ", ".join(chunk.meta.headings)
            content_text = f"{content_headings}\n{chunk.text}"
            source = f"{chunk.meta.origin.filename}:{i}"
            item = DataItem(content=content_text, source=source)
            items.append(item)

        return items

    def _index_csv(self, csv_path: str) -> List[DataItem]:
        with open(csv_path, newline="", encoding="utf-8-sig") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)

        items: List[DataItem] = []
        seen_sources: Dict[str, int] = {}

        for idx, row in enumerate(rows):
            metadata: Dict[str, object] = {}
            for key, value in row.items():
                cleaned_value = self._clean_metadata_value(value)
                if cleaned_value is not None:
                    metadata[key] = cleaned_value

            if not metadata:
                continue

            name = metadata.get("Nom_fr") or metadata.get("Nom") or "Association"
            source = self._build_source(name, idx, seen_sources)
            content = self._build_content(metadata)

            items.append(DataItem(content=content, source=source, metadata=metadata))

        return items

    def _index_http(self, url: str) -> List[DataItem]:
        headers: Dict[str, str] = {}
        token = os.environ.get("PRISMA_API_TOKEN")
        if token:
            headers["Authorization"] = f"Bearer {token}"

        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        payload = response.json()

        if isinstance(payload, list):
            rows: Iterable[Any] = payload
        elif isinstance(payload, dict):
            if "data" in payload and isinstance(payload["data"], list):
                rows = payload["data"]
            else:
                rows = [payload]
        else:
            raise ValueError("Unsupported Prisma payload format; expected list or dict")

        items: List[DataItem] = []
        seen_sources: Dict[str, int] = {}

        for idx, row in enumerate(rows):
            if not isinstance(row, dict):
                # fallback to string representation
                metadata = {"content": str(row)}
            else:
                metadata = {}
                for key, value in row.items():
                    cleaned_value = self._clean_metadata_value(value)
                    if cleaned_value is not None:
                        metadata[key] = cleaned_value

            if not metadata:
                continue

            name = metadata.get("Nom_fr") or metadata.get("Nom") or "Association"
            source = self._build_source(name, idx, seen_sources)
            content = self._build_content(metadata)

            items.append(DataItem(content=content, source=source, metadata=metadata))

        return items

    def _build_source(
        self, name: str, index: int, seen_sources: Dict[str, int]
    ) -> str:
        slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
        if not slug:
            slug = f"association-{index}"

        count = seen_sources.get(slug, 0)
        seen_sources[slug] = count + 1
        if count > 0:
            slug = f"{slug}-{count}"

        return f"associations::{slug}"

    def _build_content(self, metadata: Dict[str, object]) -> str:
        lines: List[str] = []

        ordered_keys = FIELD_ORDER + [
            key for key in metadata.keys() if key not in FIELD_ORDER
        ]

        for key in ordered_keys:
            value = metadata.get(key)
            if not value:
                continue

            display_key = key.replace("_", " ")

            if isinstance(value, list):
                if len(value) == 1:
                    lines.append(f"{display_key}: {value[0]}")
                else:
                    lines.append(f"{display_key}:")
                    lines.extend([f"- {entry}" for entry in value])
            else:
                value_str = str(value)
                if ";" in value_str:
                    entries = [entry.strip() for entry in value_str.split(";") if entry.strip()]
                    if len(entries) > 1:
                        lines.append(f"{display_key}:")
                        lines.extend([f"- {entry}" for entry in entries])
                    elif entries:
                        lines.append(f"{display_key}: {entries[0]}")
                else:
                    lines.append(f"{display_key}: {value_str}")

        return "\n".join(lines)

    def _normalise_value(self, value: str) -> object:
        if ";" in value:
            entries = [entry.strip() for entry in value.split(";") if entry.strip()]
            if len(entries) == 1:
                return entries[0]
            if entries:
                return entries
        if "\n" in value:
            segments = [segment.strip() for segment in value.splitlines() if segment.strip()]
            if len(segments) > 1:
                return segments
        return value

    def _clean_metadata_value(self, value: Any) -> Any:
        if value is None:
            return None
        if isinstance(value, str):
            stripped = value.strip()
            if not stripped:
                return None
            return self._normalise_value(stripped)
        if isinstance(value, list):
            cleaned_list = [self._clean_metadata_value(item) for item in value]
            flattened: List[str] = []
            for item in cleaned_list:
                if not item:
                    continue
                if isinstance(item, list):
                    flattened.extend([str(x) for x in item if x])
                else:
                    flattened.append(str(item))
            if not flattened:
                return None
            if len(flattened) == 1:
                return flattened[0]
            return flattened
        if isinstance(value, (int, float, bool)):
            return str(value)
        if isinstance(value, dict):
            return json.dumps(value, ensure_ascii=False)
        return str(value)

    def _is_url(self, path: str) -> bool:
        return path.startswith("http://") or path.startswith("https://")
