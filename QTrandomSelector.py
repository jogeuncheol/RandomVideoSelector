import os
import sys
import random
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import QStandardItem


# UI파일 연결
# 단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    # 출처: https://editor752.tistory.com/140 [CF::LF:티스토리]
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


# form = resource_path('randomOpen.ui')
form = resource_path('randomPlay.ui')
form_class = uic.loadUiType(form)[0]


# 화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class):
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.path = ''
        self.dir_list = []
        self.format_lsit = ['mp4', 'avi', 'mkv', 'wmv', 'mov', 'flv', 'webm',
                           'gif', 'm4p', 'mpg', 'mpeg', 'svi']

        # 버튼에 기능을 연결하는 코드
        # self.pathButton.clicked.connect(self.dir_path_button)
        self.toolButton.clicked.connect(self.dir_path_button)
        # self.findButton.clicked.connect(self.random_play)
        self.playButton.clicked.connect(self.random_play)

    def find_video(self):
        video_list = []
        for video_name in self.dir_list:
            if '.' in video_name:
                if video_name.split('.')[-1] in self.format_lsit:
                    video_list.append(video_name)
            else:
                continue
        if len(video_list):
            self.dir_list.clear()
            self.dir_list = video_list
            return True
        else:
            QMessageBox.question(self, 'Error', '해당 경로에 영상파일이 없습니다.', QMessageBox.Ok, QMessageBox.NoButton)
            return False

    def set_view(self):
        model = QStandardItemModel()
        for video in self.dir_list:
            model.appendRow(QStandardItem(video))
        self.listView.setModel(model)

    def dir_path_button(self):
        backup_path = self.path
        backup_list = self.dir_list
        self.path = QFileDialog.getExistingDirectory(self, 'Select Directory')
        if self.path:
            self.dir_list = os.listdir(self.path)
            if self.find_video():
                self.set_view()
                self.pathText.setText(self.path)
            else:
                self.path = backup_path
                self.dir_list = backup_list

    def random_play(self):
        # path 설정이 되어있지 않으면 리턴
        if not self.path:
            return
        # 지정한 경로의 파일 수 만큼 랜덤 인덱스
        random_idx = random.randint(0, len(self.dir_list) - 1)
        # 파일의 확장자가 동영상 인지 확인
        if self.dir_list[random_idx].split('.')[1] not in self.format_lsit:
            return
        # 경로와 파일 이름 붙여 실행하기
        random_video = self.path + '/' + self.dir_list[random_idx]
        os.startfile(random_video)
        self.videoName.setText(self.dir_list[random_idx])


if __name__ == "__main__" :
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    # WindowClass의 인스턴스 생성
    myWindow = WindowClass()

    # 프로그램 화면을 보여주는 코드
    myWindow.show()

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
