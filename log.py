import json
from datetime import datetime
from io import BytesIO
from tg_connector import TG_CONNECTOR
import os, inspect
current_file = os.path.basename(__file__)

class Logger():
    def __init__(self) -> None:
        super().__init__()
        self.logs_buffer = []
        # self.all_errors = {}  
        
    def log_to_buffer(self, file_name, line_number, exception_message):
        self.logs_buffer.append((file_name, line_number, exception_message))

    # def log_all_errors(self, file_name, timestamp, exception_message):
    #     if file_name in self.all_errors:
    #         if exception_message not in self.all_errors[file_name]:
    #             self.all_errors[file_name].append((timestamp, exception_message))
    #     else:
    #         self.all_errors[file_name] = [(timestamp, exception_message)]

    def get_logs(self):
        if self.logs_buffer:
            file = BytesIO()
            file.write(str(self.logs_buffer).encode('utf-8'))
            file.name = "logs.txt"
            file.seek(0)
            self.logs_buffer = []
            return file
        return        

class JsonLogger(Logger):
    def __init__(self):
        super().__init__()
        self.json_logs_buffer = []

    def json_to_buffer(self, target, cur_time, data):
        self.json_logs_buffer.append((target, cur_time, data))

    def get_json_data(self):
        # print(self.json_logs_buffer)
        file = BytesIO()
        file.write(json.dumps(self.json_logs_buffer, indent=4).encode('utf-8'))
        file.name = "data.json"
        file.seek(0)
        self.json_logs_buffer = []
        return file

class Total_Logger(JsonLogger, TG_CONNECTOR):
    def __init__(self):
        super().__init__()

    def handle_messagee(self, textt):
        print(textt)
        if self.last_message:
            self.last_message.text = self.connector_func(self.last_message, textt)

    def handle_exception(self, error_message):  
        self.handle_messagee(error_message)

    # //////////////////////////////////////
    def log_exceptions_decorator(self, func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as ex:
                # timestamp = datetime.utcnow()
                current_frame = inspect.currentframe()
                caller_frame = current_frame.f_back
                file_name = caller_frame.f_code.co_filename
                line_number = caller_frame.f_lineno
                exception_message = str(ex)
                error_info = (file_name, line_number, exception_message)
                self.log_to_buffer(*error_info)
                # self.log_all_errors(file_name, timestamp, exception_message)
                self.handle_exception(f"Error occurred in file '{file_name}', line {line_number}: {exception_message}")

        return wrapper