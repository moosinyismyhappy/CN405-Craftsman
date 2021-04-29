import time
from threading import Thread
from PyQt5.QtCore import QThread, pyqtSignal, QCoreApplication

class AThread(Thread):

    def __init__(self):
        super().__init__()
        self.count = 0

    def get_count(self):
        return self.count

    def run(self):
        while True:
            time.sleep(0.1)
            self.count += 1
            print('AThread',self.get_count())


class BThread(QThread):
    finished = pyqtSignal()

    def __init__(self,a):
        super().__init__()
        self.count = 0
        self.a = a

    def run(self):
        while self.count<100:
            time.sleep(0.1)
            print('BThread', self.a.get_count())
            self.count = self.count + 1
        self.finished.emit()


app = QCoreApplication([])
thread1 = AThread()
thread1.start()


thread2 = BThread(thread1)
thread2.start()
thread2.finished.connect(app.exit)
app.exec_()
