"""TaskFlow script for advanced OOP concepts."""
import re
import requests
from abc import ABC, abstractmethod

class EmailException(Exception):
    """Custom exception for email-related errors."""
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

class Task(ABC):
    """Abstract base class for tasks."""
    def __init__(self, input: str):
        self.input = input
    
    @abstractmethod
    def execute(self):
        """Execute the task."""
        pass



class PrintTask(Task):
    """Task to print the input."""

    def execute(self):
        """Execute the task."""
        if not self.input:
            raise ValueError("Input cannot be None")
        print(self.input)
    
    
class EmailTask(Task):
    """Task to send an email."""
    sender: str = "rajaa.lebchiri@gmail.com"
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    
    def __init__(self, recipient: str, subject: str = None, body: str = None):
        if not re.fullmatch(self.email_regex, recipient):
            print(f"Invalid email address: {recipient}")
            raise EmailException("Invalid email address")
        else:
            self.recipient = recipient
            self.body = body
            self.subject = subject

    def execute(self):
        """Execute the task."""
        if not self.recipient:
            raise ValueError("Recipient cannot be None")
        self.sendEmail(recipient=self.recipient, subject=self.subject, body=self.body)

    def sendEmail(self, recipient: str, subject: str, body: str):
        """Simulate sending an email."""
        print(f"Sending email to {recipient} with subject '{subject}' and body '{body}'")

class FileDownloadTask(Task):
    """Task to download a file."""

    def __init__(self, url: str):
        self.url = url

    def execute(self):
        """Execute the task."""
        if not self.url:
            raise ValueError("URL cannot be None")
        print(f"Downloading file from {self.url}")
        self.downloadFile(url=self.url)
    
    def downloadFile(self, url: str):
        """Simulate downloading a file."""
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to download file from {url}. Status code: {response.status_code}")
        if response.headers.get('Content-Type') == 'application/pdf':
            filename = "file.pdf"
        if response.headers.get('Content-Type') != 'application/pdf':
            filename = "file.txt"
        with open(filename, "wb") as file:
            file.write(response.content)
        print(f"File downloaded from {url}")


class Workflow:
    """Class to manage a workflow of tasks."""
    def __init__(self):
        self.tasks = []

    def add_task(self, task: Task):
        """Add a task to the workflow."""
        self.tasks.append(task)

    def execute(self):
        """Execute all tasks in the workflow."""
        for task in self.tasks:
            task.execute()



task = PrintTask(input = "Hello, world!")


task_2 = EmailTask(recipient="devralcomp@gmail.com")


task_3 = FileDownloadTask(url="https://media.geeksforgeeks.org/wp-content/uploads/20240226121023/GFG.pdf")



workflow = Workflow()
workflow.add_task(task)
workflow.add_task(task_2)
workflow.add_task(task_3)
workflow.execute()