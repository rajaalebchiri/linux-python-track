import requests

def get_links(file_path: str):
    try:
        with open(file_path, "r") as f:
            # Read all lines and strip newlines in one go
            lines = [line.strip() for line in f if line.strip()]
            checks = []
            for line in lines:
                try:
                    r = requests.get(line, timeout=5)
                    checks.append({
                        'href': line,
                        'status': r.status_code
                    })
                except requests.exceptions.Timeout:
                    checks.append({
                        'href': line,
                        'status': "Time Out"
                    })
                except requests.exceptions.RequestException:
                    checks.append({
                        'href': line,
                        'status': "Failed"
                    })

            return checks
    except TimeoutError as ex:
        return [{"href": file_path, "status": "TimeOut"}]
    except FileNotFoundError as ex:
       return [{"href": file_path, "status": "File Not Found"}]