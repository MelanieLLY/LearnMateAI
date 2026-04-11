"""Business logic for the StudentNote resource."""

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.models.module import Module
from src.models.student_note import StudentNote
from src.schemas.student_note import StudentNoteCreate


def upload_student_note(
    db: Session,
    module_id: int,
    student_id: int,
    payload: StudentNoteCreate,
) -> StudentNote:
    """Persist a new student note for the given module.

    Args:
        db: Active SQLAlchemy database session.
        module_id: ID of the module the note belongs to.
        student_id: ID of the student uploading the note.
        payload: Validated request body containing the note content.

    Returns:
        The newly created ``StudentNote`` ORM instance.

    Raises:
        HTTPException: 404 if the module does not exist.
    """
    module = db.query(Module).filter(Module.id == module_id).first()
    if module is None:
        raise HTTPException(status_code=404, detail="Module not found")

    note = StudentNote(
        content=payload.content,
        module_id=module_id,
        student_id=student_id,
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return note

def get_student_notes(
    db: Session,
    module_id: int,
    student_id: int,
) -> list[StudentNote]:
    """Retrieve all notes uploaded by a student for a specific module."""
    return (
        db.query(StudentNote)
        .filter(StudentNote.module_id == module_id, StudentNote.student_id == student_id)
        .order_by(StudentNote.uploaded_at.desc())
        .all()
    )
