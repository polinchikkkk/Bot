class Session:
    def __init__(self, set_errors: set, last_open_file: str, line_for_check: int):
        self.last_open_file = last_open_file
        self.set_errors = set_errors
        self.line_for_check = line_for_check

    def new_file(self, file_for_check: str):
        if self.last_open_file != file_for_check:
            self.last_open_file = file_for_check
            self.line_for_check = 0
            self.set_errors.clear()