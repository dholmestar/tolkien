from gencontent import extract_title # type: ignore

def test_extract_title_simple():
    assert extract_title("# Hello") == "Hello"

def test_extract_title_multiline():
    markdown = """
some text
# Tolkien Fan Club
more stuff
""".strip()
    assert extract_title(markdown) == "Tolkien Fan Club"