"""
Stage 2 of the pipeline: splitting documents into chunks.

⚠️ THIS IS THE FILE YOU CHANGE IN MILESTONE 3.

`split_documents` below is deliberately plain. It cuts every document into
fixed-size pieces with a fixed overlap and pays no attention to where sentences
or paragraphs end. It works, and it is not good.

On a corpus of short posts it may not cut anything at all: `campus_life` comes
out as 88 documents and 88 chunks, because almost nothing in it reaches 800
characters. That is the baseline, not a bug — Milestone 3 is where you decide
whether one post should stay one chunk.

Your job in Milestone 3 is to replace the *body* of `split_documents` with a
strategy that fits the documents you actually read in Milestone 1. Keep the
name and the shape of what it returns — the rest of the pipeline calls it, and
your README has to name the function that produced your chunks.

If you get stuck for 30 minutes, `fallback_split` is the original. Switch back
to it, write down what you saw, and move on. That's a real observation about
your pipeline, not giving up.
"""

import re
from dataclasses import dataclass

import config
from ingest import Document


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


def split_documents(documents: list[Document]) -> list[Chunk]:
    """Split short post documents on paragraph boundaries while keeping chunks under a target length."""
    chunk_size = config.CHUNK_SIZE
    overlap = config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        text = doc.text.strip()
        if not text:
            continue

        paragraphs = [p.strip() for p in re.split(r"\n\s*\n+", text) if p.strip()]
        if not paragraphs:
            paragraphs = [text]

        index = 0
        i = 0
        while i < len(paragraphs):
            collected: list[str] = []
            current_length = 0
            end = i

            while end < len(paragraphs):
                paragraph = paragraphs[end]
                paragraph_length = len(paragraph)
                next_length = current_length + (1 if collected else 0) + paragraph_length
                if collected and next_length > chunk_size:
                    break
                collected.append(paragraph)
                current_length = next_length
                end += 1

            if not collected:
                collected = [paragraphs[i]]
                end = i + 1

            chunk_text = "\n\n".join(collected)
            if len(chunk_text) > chunk_size * 1.5:
                # A single long paragraph still needs to be split on sentences.
                sentence_pattern = re.compile(r"(?<=[.!?])\s+")
                sentences = [s.strip() for s in sentence_pattern.split(chunk_text) if s.strip()]
                sentence_buffer: list[str] = []
                sentence_chars = 0
                for sentence in sentences:
                    next_chars = sentence_chars + (1 if sentence_buffer else 0) + len(sentence)
                    if sentence_buffer and next_chars > chunk_size:
                        chunks.append(
                            Chunk(
                                text=" ".join(sentence_buffer),
                                source=doc.source,
                                index=index,
                                produced_by="chunker.py::split_documents",
                            )
                        )
                        index += 1
                        sentence_buffer = [sentence]
                        sentence_chars = len(sentence)
                    else:
                        sentence_buffer.append(sentence)
                        sentence_chars = next_chars
                if sentence_buffer:
                    chunks.append(
                        Chunk(
                            text=" ".join(sentence_buffer),
                            source=doc.source,
                            index=index,
                            produced_by="chunker.py::split_documents",
                        )
                    )
                    index += 1
                i = end
                continue

            chunks.append(
                Chunk(
                    text=chunk_text,
                    source=doc.source,
                    index=index,
                    produced_by="chunker.py::split_documents",
                )
            )
            index += 1

            if end >= len(paragraphs):
                break
            overlap_paragraphs = max(1, min(2, len(collected) // 2))
            i = max(i + 1, end - overlap_paragraphs)

    return chunks


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
