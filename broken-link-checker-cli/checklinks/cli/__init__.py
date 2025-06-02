from checklinks.core import get_links

def check_links(file_path: str):
    lines = get_links(file_path)
    print(lines)
    return lines