import logging
import sys
import traceback
from telegram import Bot, error
import __main__

class TelegramLogHandler(logging.Handler):
    def __init__(self, telegram_id, telegram_key):
        self.bot = Bot(telegram_key)
        self.telegram_id = telegram_id
        logging.Handler.__init__(self)
        self.setLevel(logging.WARNING)
        self.setFormatter(CustomFormatter())

    def emit(self, message):
        msg = self.format(message)
        try:
            self.bot.send_message(self.telegram_id, msg)
        except error.TimedOut:
            pass

class CustomFormatter(logging.Formatter):
    def format(self, record):
        if record.levelno in (logging.WARNING,
                              logging.ERROR,
                              logging.CRITICAL):
            record.msg = 'Process: ' + str(__main__.__file__) + '\n[%s] %s' % (record.levelname, record.msg)
        return super(CustomFormatter, self).format(record)

def log_unhandled(type, value, tb):
    final_tb = ''
    extracted_list = traceback.extract_tb(tb)
    for item in traceback.StackSummary.from_list(extracted_list).format():
        final_tb = final_tb + item + '\n'

    master_logger.exception("\nUncaught exception\nType: {}\nValue: {}\nTB: {}".format(str(type), str(value),
                                                                                       str(final_tb)))
    traceback.print_tb(tb)


def init(telegram_id, telegram_key):
    master_logger = logging.getLogger()

    master_logger.setLevel(logging.DEBUG)
    master_logger.addHandler(TelegramLogHandler(telegram_id, telegram_key))
    sys.excepthook = log_unhandled

    return master_logger