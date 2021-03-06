"""
user tests edit profile
"""

# standard library
# import json
from typing import Any, Dict

# third-party
import pytest
# local Django
from django.contrib.auth.models import User

from user.serializers import UserHeavySerializer

# permitir acceso a db
pytestmark = [pytest.mark.django_db, pytest.mark.users_views]


@pytest.mark.users_profile
def test_user_update_profile(admin_client):
    """
    ...
    """
    user_id: int = 1
    oldvalues = UserHeavySerializer(User.objects.get(id=user_id))
    newdata: Dict[str, Any] = {
        'username': 'NEW',
        'first_name': 'new name',
        'last_name': 'new name2',
    }
    response = admin_client.post(
        '/api/user/profile/',
        newdata
    )
    newvalues = UserHeavySerializer(User.objects.get(id=user_id))
    assert response.status_code == 200
    assert newvalues.data != oldvalues.data
    assert newvalues.data == response.data


@pytest.mark.users_profile
def test_user_update_profile_invalid_params(admin_client):
    """
    ...
    """
    user_id: int = 1
    oldvalues = UserHeavySerializer(User.objects.get(id=user_id))
    newdata: Dict[str, Any] = {
        'usernames': 'NEW',
        'first_names': 'new name',
    }
    response = admin_client.post(
        '/api/user/profile/',
        newdata
    )
    newvalues = UserHeavySerializer(User.objects.get(id=user_id))
    assert response.status_code == 400
    assert newvalues.data == oldvalues.data
