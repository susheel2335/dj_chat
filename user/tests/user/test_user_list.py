"""
test list users
"""

# third-party
import pytest

# local Django
from django.contrib.auth.models import User

from user.serializers import UserHeavySerializer

# permitir acceso a db
pytestmark = [pytest.mark.django_db, pytest.mark.users_views]


@pytest.mark.users_list
def test_get_all_user(admin_client):
    """
    ...
    """
    response = admin_client.get('/api/users/')
    serializer = UserHeavySerializer(
        User.objects.all(),
        many=True
    )
    assert response.status_code == 200
    assert serializer.data == response.data


@pytest.mark.users_list
def test_list_users_only_for_super_users(staff_client):
    """
    ...
    """
    response = staff_client.get('/api/users/')
    assert response.status_code == 403
