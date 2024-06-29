from tg_connector import TG_CONNECTOR
import os, inspect
current_file = os.path.basename(__file__)

class Total_Logger(TG_CONNECTOR):
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
                self.handle_exception(f"Error occurred in file '{file_name}', line {line_number}: {exception_message}")

        return wrapper