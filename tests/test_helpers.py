from src.helpers import methods as m


def test_verify_avi_format_when_is_true() -> None:

    assert m.verify_avi_format("fake_file.avi") == True


def test_verify_avi_format_when_is_false() -> None:

    assert m.verify_avi_format("fake_file.mp4") == False


def test_generate_new_name_works_properly() -> None:

    assert m.generate_new_name("fake_name.avi") == "fake_name.mp4"
