from src.helpers import methods as m


def test_verify_avi_format_when_is_true() -> None:

    test_name = "fake_file.avi"

    assert m.verify_avi_format(test_name) == True


def test_verify_avi_format_when_is_false() -> None:

    test_name = "fake_file.mp4"

    assert m.verify_avi_format(test_name) == False


def test_generate_new_name_works_properly() -> None:

    assert m.generate_new_name("fake_name.avi") == "fake_name.mp4"
