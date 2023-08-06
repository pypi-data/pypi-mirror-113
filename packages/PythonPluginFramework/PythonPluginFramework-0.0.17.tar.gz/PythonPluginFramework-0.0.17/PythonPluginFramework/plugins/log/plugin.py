

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import time
import logging
logging.getLogger().setLevel(logging.DEBUG)


_logexplore_view = None
log_widget_handler = None
context = None
data_service = None

def init(context_):
    global context
    context = context_
    # 获取所有日志处理扩展
    exts = context.find_extension("Core::Log::Handler")
    for ext in exts:
        logging.getLogger().addHandler(ext)
    context.add_subscribe("*", OnEvent)

class QTextEditLogger(logging.Handler, QObject):
    appendPlainText = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        QObject.__init__(self)
    def emit(self, record):
        msg = self.format(record)
        self.appendPlainText.emit(msg)

log_widget_handler = QTextEditLogger()

class LogExploreView(QDockWidget):
    def __init__(self):
        super().__init__()

        global log_widget_handler
        self.text_widget = QPlainTextEdit(self)
        self.text_widget.setReadOnly(True)
        log_widget_handler.appendPlainText.connect(self.text_widget.appendPlainText)

        
        self.setWidget(self.text_widget)

class LogExploreExtension:
    def add_pane(self, frame):
        global _logexplore_view
        self._dock1 = LogExploreView()
        _logexplore_view = self._dock1
        self._dock1.setWindowTitle('LogExplore')
        frame.addDockWidget(Qt.BottomDockWidgetArea, self._dock1)

        global _frame
        _frame = frame

def OnEvent(event, value1 = None, value2 = None, value3 = None, value4 = None, value5 = None):
    print("-----------on event------------------")
    print(event)
    if value1:
        print(value1)
    if value2:
        print(value2)
    if value3:
        print(value3)
    if value4:
        print(value4)
    if value5:
        print(value5)

LogHandlerExtension = '''
import logging
logging.Handler
'''

config = {
    'pluginid': 'Core::Log',
    "extensions_def" : [
        {
            "name": "Core::Log::Handler",
            "define": LogHandlerExtension
        }
    ],
    "extensions" : [
        {
            "name": "PL::Basic::Pane",
            "id": "PL::Basic::Pane::LogExplore",
            "impl": LogExploreExtension()
        },
        {
            "name": "Core::Log::Handler",
            "id": "Core::Log::Handler::StreamHandler",
            "impl": logging.StreamHandler()
        },
        {
            "name": "Core::Log::Handler",
            "id": "Core::Log::Handler::FileHandler",
            "impl": logging.FileHandler(filename="log.txt", mode="w+")
        },
        {
            "name": "Core::Log::Handler",
            "id": "Core::Log::Handler::PlainTextWidgetHandler",
            "impl": log_widget_handler
        },
        
    ]
    
}