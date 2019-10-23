import logging
import sys
import traceback
import __main__
from telogram.telegramapi import send

class TelegramLogHandler(logging.Handler):
    def __init__(self, telegram_id, token):
        self.token = token
        self.telegram_id = telegram_id
        logging.Handler.__init__(self)
        self.setLevel(logging.WARNING)
        self.setFormatter(CustomFormatter())

    def emit(self, message):
        msg = self.format(message)
        send(self.token, self.telegram_id, msg)

class CustomFormatter(logging.Formatter):
    def format(self, record):
        if record.levelno in (logging.WARNING,
                              logging.ERROR,
                              logging.CRITICAL):
            try:
                file = str(__main__.__file__)
            except AttributeError:
                file = "Interactive shell"
            record.msg = 'Process: ' + file + '\n[%s] %s' % (record.levelname, record.msg)
        return super(CustomFormatter, self).format(record)

def log_unhandled(type, value, tb):
    final_tb = ''
    extracted_list = traceback.extract_tb(tb)
    for item in traceback.StackSummary.from_list(extracted_list).format():
        final_tb = final_tb + item + '\n'

    logging.getLogger().exception("\nUncaught exception\nType: {}\nValue: {}\nTB: {}".format(str(type), str(value),
                                                                                       str(final_tb)))
    traceback.print_tb(tb)


def init(telegram_id, token):
    master_logger = logging.getLogger()

    master_logger.setLevel(logging.DEBUG)
    master_logger.addHandler(TelegramLogHandler(telegram_id, token))
    sys.excepthook = log_unhandled

    return master_logger