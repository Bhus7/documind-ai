from langchain_text_splitters import  RecursiveCharacterTextSplitter

def fixed_size_chunking(
        text: str,
        chunk_size: int = 500,
        overlap: int = 50
)-> list[str]:

    if chunk_size <=0:
        raise ValueError("Chunk size must be positive")

    if overlap < 0 or  overlap >= chunk_size:
        raise ValueError("Overlap must be smaller than chunk size")

    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk  = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start = end - overlap

    return chunks

def recursive_chunking(
    text: str,
    chunk_size: int = 500,
    overlap: int = 50
) -> list[str]:

    if chunk_size <= 0:
        raise ValueError("Chunk size must be positive")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("Overlap must be smaller than chunk size")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    return splitter.split_text(text)