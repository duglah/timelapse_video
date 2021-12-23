from datetime import datetime

class TimelapsePhoto:
    def __init__(self, name: str) -> None:
        self.name = name
        self.datetime = datetime.strptime(
            name.split(".")[0], '%Y-%m-%d_%H-%M-%S')