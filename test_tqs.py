import tqs

def test_encode_body_text():
    body_data, body_type = tqs.encode_body("Hello")
    assert body_data == "Hello"
    assert body_type == "text/plain"

def test_decode_body_text():
    body = tqs.decode_body("Hello", "text/plain")
    assert body == "Hello"

def test_encode_body_bytes():
    body_data, body_type = tqs.encode_body(b"Hello")
    assert body_data == "SGVsbG8="
    assert body_type == "application/octet-stream"

def test_decode_body_bytes():
    body = tqs.decode_body("SGVsbG8=", "application/octet-stream")
    assert body == b"Hello"

def test_encode_body_json_array():
    body_data, body_type = tqs.encode_body([1,2,3])
    assert body_data == "[1, 2, 3]"
    assert body_type == "application/json"

def test_decode_body_json_array():
    body = tqs.decode_body("[1, 2, 3]", "application/json")
    assert body == [1,2,3]

def test_encode_body_json_object():
    body_data, body_type = tqs.encode_body({"foo":42})
    assert body_data == '{"foo": 42}'
    assert body_type == "application/json"

def test_decode_body_json_object():
    body = tqs.decode_body('{"foo": 42}', "application/json")
    assert body == {"foo": 42}
