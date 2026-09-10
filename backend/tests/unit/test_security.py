from app.core.security import hash_password, verify_password, create_access_token, decode_access_token


def test_password_hash_is_not_plaintext():
    hashed = hash_password("mypassword123")
    assert hashed != "mypassword123"


def test_verify_correct_password():
    hashed = hash_password("mypassword123")
    assert verify_password("mypassword123", hashed) is True


def test_verify_incorrect_password():
    hashed = hash_password("mypassword123")
    assert verify_password("wrongpassword", hashed) is False


def test_jwt_encode_decode_roundtrip():
    token = create_access_token(data={"sub": "42"})
    payload = decode_access_token(token)
    assert payload is not None
    assert payload["sub"] == "42"


def test_jwt_decode_rejects_garbage_token():
    payload = decode_access_token("this.is.not.a.valid.token")
    assert payload is None