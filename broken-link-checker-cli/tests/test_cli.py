from pathlib import Path
from checklinks import check_links

def test_check_links():
    file_path = "links.txt"
    result = check_links(str(file_path))

    assert result == [{'href': 'https://www.google.com', 'status': 200}, {'href': 'https://www.wikipedia.org', 'status': 200}, {'href': 'https://httpstat.us/200', 'status': 200}, {'href': 'https://www.github.com', 'status': 200}, {'href': 'https://httpstat.us/301', 'status': 200}, {'href': 'https://httpstat.us/302', 'status': 200}, {'href': 'https://httpstat.us/401', 'status': 401}, {'href': 'https://httpstat.us/410', 'status': 410}, {'href': 'https://httpstat.us/500', 'status': 500}, {'href': 'https://httpstat.us/504', 'status': 504}, {'href': 'https://httpstat.us/200?sleep=10000', 'status': 'Time Out'}, {'href': 'http://thisdomaindoesnotexist.tld', 'status': 'Failed'}]

def test_file_not_found():
    result = check_links("nonexistent.txt")
    assert result == [{"href": "nonexistent.txt", "status": "File Not Found"}]
