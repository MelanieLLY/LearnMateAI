"""Look up the instructor's audience guidelines for a module."""

from sqlalchemy.orm import Session

from src.agents.prompts.audience import combine_audience_context
from src.models.course import Course
from src.models.module import Module


def get_audience_context(db: Session, module: Module) -> str:
    """Return the course- and module-level audience guidelines for ``module``.

    Args:
        db: Active SQLAlchemy database session.
        module: The module being used for generation. Modules without a course
            only contribute their own ``audience_context``.

    Returns:
        The merged guidelines text, or an empty string when neither the course
        nor the module has any.
    """
    course_context = None
    if module.course_id is not None:
        course = db.query(Course).filter(Course.id == module.course_id).first()
        course_context = course.audience_context if course else None
    return combine_audience_context(course_context, module.audience_context)
