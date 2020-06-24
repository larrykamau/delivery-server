from ..celeryconf import app
from ..core.utils import create_thumbnails
from .models import CustomUser


@app.task
def create_user_avatar_thumbnails(user_id):
    """Create thumbnails for user avatar."""
    create_thumbnails(
        pk=user_id, model=CustomUser, size_set="user_avatars", image_attr="avatar"
    )
