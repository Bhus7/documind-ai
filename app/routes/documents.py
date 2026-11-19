
from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    HTTPException,
    Depends
)
from sqlalchemy.orm import Session
from io import BytesIO
from pypdf import PdfReader

from app.db.database import get_db
from app.models.document import Document
from app.services.chunking import (
    fixed_size_chunking,
    recursive_chunking
)
from app.services.embedding import generate_embeddings
from app.services.vector_store import store_embeddings

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    chunking_strategy: str = Form("recursive"),
    db: Session = Depends(get_db)
):

    allowed_extensions = {".pdf", ".txt"}
    file_extension = file.filename.rsplit(".", 1)[-1].lower()

    if f".{file_extension}" not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and TXT files are allowed"
        )

    if chunking_strategy not in {"fixed", "recursive"}:
        raise HTTPException(
            status_code=400,
            detail="Invalid chunking strategy. Choose 'fixed' or 'recursive'."
        )

    file_content = await file.read()

    extracted_text = extract_text(
        file_content,
        f".{file_extension}"
    )

    # Apply selected chunking strategy
    if chunking_strategy == "fixed":
        chunks = fixed_size_chunking(extracted_text)
    else:
        chunks = recursive_chunking(extracted_text)

    if not chunks:
        raise HTTPException(
            status_code=400,
            detail="No text could be extracted from the document"
        )

    # Generate embeddings for all chunks
    embeddings = generate_embeddings(chunks)

    # Save document metadata in PostgreSQL
    document = Document(
        filename=file.filename,
        file_type=f".{file_extension}"
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    # Store embeddings and chunk information in Qdrant
    store_embeddings(
        chunks=chunks,
        embeddings=embeddings,
        document_id=document.id,
        filename=file.filename
    )

    return {
        "document_id": document.id,
        "filename": file.filename,
        "content_type": file.content_type,
        "chunking_strategy": chunking_strategy,
        "total_chunks": len(chunks),
        "total_embeddings": len(embeddings),
        "message": "Document processed and stored successfully"
    }


def extract_text(file_content: bytes, file_extension: str) -> str:

    if file_extension == ".txt":
        return file_content.decode("utf-8")

    elif file_extension == ".pdf":
        pdf_reader = PdfReader(BytesIO(file_content))

        extracted_text = ""

        for page in pdf_reader.pages:
            extracted_text += page.extract_text() or ""

        return extracted_text

    return ""
