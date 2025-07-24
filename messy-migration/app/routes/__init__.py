# Initializes the app package

# app/models/__init__.py

from app.models.user_model import (
    get_all_users,
    get_user_by_id,
    create_user,
    update_user,
    delete_user,
    search_users,
    login_user
)
