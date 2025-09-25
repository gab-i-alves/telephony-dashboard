from app.services.call import parse_duration_to_seconds

def test_parse_duration_to_seconds():
    assert parse_duration_to_seconds("00:02:20") == 140
    assert parse_duration_to_seconds("01:00:00") == 3600
    assert parse_duration_to_seconds("00:00:00") == 0
    assert parse_duration_to_seconds(None) == 0
    assert parse_duration_to_seconds("invalid-string") == 0