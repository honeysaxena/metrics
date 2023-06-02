import pytest
from application.users.models import User
from application import db

@pytest.fixture(scope='module')
def setup():
    session = db.get_session()
    yield session
    q = User.objects.filter(email='test@test.com')
    if q.count() != 0:
        q.delete()
    session.shutdown()

def test_create_user(setup):
    User.create_user(email='test@test.com', password='abc123')

def test_duplicate_user(setup):
    with pytest.raises(Exception):
        User.create_user(email='test@test.com', password='abc123')

def test_invalid_email(setup):
    with pytest.raises(Exception):
        User.create_user(email='test@test', password='abc123')

def test_valid_password(setup):
    q = User.objects.filter(email="test@test.com")
    assert q.count() == 1
    user_obj = q.first()
    assert user_obj.verify_password('abc123') == True
    assert user_obj.verify_password('abc1234') == False                    

def test_assert():
    assert True is True


def test_invalid_assert():
    with pytest.raises(AssertionError):
        assert True is not True    

