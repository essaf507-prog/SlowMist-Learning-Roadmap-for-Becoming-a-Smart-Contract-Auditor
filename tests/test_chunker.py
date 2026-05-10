from paper_style_ai.chunker import split_into_chunks


def test_split_into_chunks_preserves_text_and_limits_size():
    text = " ".join(f"This is sentence {i}." for i in range(80))

    chunks = split_into_chunks(text, max_tokens=80, overlap_tokens=10)

    assert len(chunks) > 1
    assert chunks[0].chunk_id == 1
    assert all(chunk.text for chunk in chunks)
    assert all(chunk.token_estimate <= 110 for chunk in chunks)
