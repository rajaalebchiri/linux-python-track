import socket

class ContextManager:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            print(f"An exception occurred: {exc_value}")
        else:
            print("Exiting context without exceptions")
        return True

class FileManagerContext(ContextManager):
    def __init__(self, filename: str):
        self.filename = filename
        self.file = None

    def __enter__(self):
        self.file = open(self.filename, 'w')
        return self.file

    def __exit__(self, exc_type, exc_value, traceback):
        if self.file:
            self.file.close()
        super().__exit__(exc_type, exc_value, traceback)


class NetworkSessionContext(ContextManager):
    def __init__(self, url: str, port: int, data=None, session=None):
        self.url = url
        self.port = port
        self.data = data
        self.session = session
    
    def __enter__(self):
        if not self.url:
            raise ValueError("URL cannot be None")
        if not self.session:
            self.session = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.session.connect((self.url, self.port))
        return self.session

    def __exit__(self, exc_type, exc_value, traceback):
        if self.session:
            self.session.close()
        super().__exit__(exc_type, exc_value, traceback)


with FileManagerContext('example.txt') as file:
    file.write("Hello, World!")
    print("File written successfully.")


with NetworkSessionContext(url="localhost", port=12345) as session:
    session.send(b'Hello, server!')
    data = session.recv(1024)

    print('Received from server:', data.decode())