from datetime import datetime, timezone

from sqlalchemy import event
from sqlalchemy.orm import Session

from cuztomisable.context import current_user_id


@event.listens_for(Session, "before_flush")
def set_audit_fields(session, flush_context, instances):
    user_id = current_user_id.get()
    # Set created_by field for new objects
    for obj in session.new:
        # Set created_by field for new objects
        if hasattr(obj, "created_by") and obj.created_by is None:
            obj.created_by = user_id
    # Set updated_by field for modified objects
    for obj in session.dirty:
        # Soft delete handling
        if hasattr(obj, "deleted_at") and hasattr(obj, "deleted_by"):
            if obj.deleted_at is not None and obj.deleted_by is None:
                obj.deleted_by = user_id
    # Handle soft delete for deleted objects
    for obj in list(session.deleted):
        if hasattr(obj, "deleted_at"):
            session.expunge(obj)
            obj.deleted_at = datetime.now(timezone.utc)
            obj.deleted_by = user_id
            session.add(obj)
