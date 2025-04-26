import os
import sys
import detect
# import qdarkstyle
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtWidgets import QMessageBox

import detect_video
import face_recognition
import cv2

class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__(parent)
        self.timer_detect = QtCore.QTimer()
        self.setupUi(self)
        self.init_logo()
        self.init_slots()
        self.file_path = None
        self.model_path = None
        self.result_path = "result"

        # 初始化人脸识别模块
        self.known_faces_encodings = {}
        self.load_known_faces()

    # 加载已知的人脸
    def load_known_faces(self):
        # 假设已知人脸图片存放在一个名为 'known_faces' 的文件夹中
        for filename in os.listdir('known_faces'):
            if filename.endswith('.jpg'):
                path = os.path.join('known_faces', filename)
                image = face_recognition.load_image_file(path)
                encoding = face_recognition.face_encodings(image)[0]
                self.known_faces_encodings[filename] = encoding

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)  # 布局的左、上、右、下到窗体边缘的距离
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_img = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_img.sizePolicy().hasHeightForWidth())
        self.pushButton_img.setSizePolicy(sizePolicy)
        self.pushButton_img.setMinimumSize(QtCore.QSize(150, 40))
        self.pushButton_img.setMaximumSize(QtCore.QSize(150, 40))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        self.pushButton_img.setFont(font)
        self.pushButton_img.setObjectName("pushButton_img")
        self.verticalLayout.addWidget(self.pushButton_img, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout.addStretch(5)  # 增加垂直盒子内部对象间距
        self.pushButton_model = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_model.sizePolicy().hasHeightForWidth())
        self.pushButton_model.setSizePolicy(sizePolicy)
        self.pushButton_model.setMinimumSize(QtCore.QSize(150, 40))
        self.pushButton_model.setMaximumSize(QtCore.QSize(150, 40))
        self.pushButton_model.setFont(font)
        self.pushButton_model.setObjectName("pushButton_model")
        self.verticalLayout.addWidget(self.pushButton_model, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout.addStretch(5)

        self.pushButton_detect = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_detect.sizePolicy().hasHeightForWidth())
        self.pushButton_detect.setSizePolicy(sizePolicy)
        self.pushButton_detect.setMinimumSize(QtCore.QSize(150, 40))
        self.pushButton_detect.setMaximumSize(QtCore.QSize(150, 40))
        self.pushButton_detect.setFont(font)
        self.pushButton_detect.setObjectName("pushButton_detect")
        self.verticalLayout.addWidget(self.pushButton_detect, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout.addStretch(5)
        self.pushButton_video_detect = QtWidgets.QPushButton(self.centralwidget)

        # 增加人脸识别
        self.pushButton_face_recognize = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_face_recognize.setMinimumSize(QtCore.QSize(150, 40))
        self.pushButton_face_recognize.setMaximumSize(QtCore.QSize(150, 40))
        self.pushButton_face_recognize.setFont(font)
        self.pushButton_face_recognize.setObjectName("pushButton_face_recognize")
        self.verticalLayout.addWidget(self.pushButton_face_recognize, 0, QtCore.Qt.AlignHCenter)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_video_detect.sizePolicy().hasHeightForWidth())
        self.pushButton_video_detect.setSizePolicy(sizePolicy)
        self.pushButton_video_detect.setMinimumSize(QtCore.QSize(150, 40))
        self.pushButton_video_detect.setMaximumSize(QtCore.QSize(150, 40))
        self.pushButton_video_detect.setFont(font)
        self.pushButton_video_detect.setObjectName("pushButton_video_detect")
        self.verticalLayout.addWidget(self.pushButton_video_detect, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout.addStretch(50)

        self.pushButton_showdir = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_showdir.sizePolicy().hasHeightForWidth())
        self.pushButton_showdir.setSizePolicy(sizePolicy)
        self.pushButton_showdir.setMinimumSize(QtCore.QSize(220, 50))
        self.pushButton_showdir.setMaximumSize(QtCore.QSize(150, 50))
        self.pushButton_showdir.setFont(font)
        self.pushButton_showdir.setObjectName("pushButton_showdir")
        self.verticalLayout.addWidget(self.pushButton_showdir, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout.setStretch(2, 1)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 3)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.label.setStyleSheet("border: 1px solid white;")  # 添加显示区域边框
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # def face_recognize(self):
    #     if self.file_path:
    #         image = face_recognition.load_image_file(self.file_path)
    #         face_locations = face_recognition.face_locations(image)
    #         unknown_face_encodings = face_recognition.face_encodings(image, face_locations)
    #
    #         # 对于每一个检测到的面部，检查是否与已知面部匹配
    #         results = []
    #         for unknown_face_encoding in unknown_face_encodings:
    #             matches = face_recognition.compare_faces(list(self.known_faces_encodings.values()),
    #                                                      unknown_face_encoding)
    #             name = "Unknown"
    #             if True in matches:
    #                 first_match_index = matches.index(True)
    #                 name = list(self.known_faces_encodings.keys())[first_match_index]
    #             results.append(name)
    #
    #         # 打印或展示识别结果
    #         print("Found {} face(s) in this photograph.".format(len(face_locations)))
    #         for result in results:
    #             print("Recognized: {}".format(result))

    def face_recognize(self):
        if self.file_path:
            # 读取图像
            image = face_recognition.load_image_file(self.file_path)
            # 使用 OpenCV 转换颜色空间以适用于显示
            image_cv = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # 获取人脸位置和编码
            face_locations = face_recognition.face_locations(image)
            unknown_face_encodings = face_recognition.face_encodings(image, face_locations)

            # 对于每一个检测到的面部，检查是否与已知面部匹配
            results = []
            for face_location, unknown_face_encoding in zip(face_locations, unknown_face_encodings):
                matches = face_recognition.compare_faces(list(self.known_faces_encodings.values()),
                                                         unknown_face_encoding)
                name = "Unknown"
                if True in matches:
                    first_match_index = matches.index(True)
                    name = list(self.known_faces_encodings.keys())[first_match_index].split('.')[0]  # 去掉文件扩展名

                # 绘制人脸框
                top, right, bottom, left = face_location
                cv2.rectangle(image_cv, (left, top), (right, bottom), (0, 0, 255), 2)  # 红色框

                # 绘制人名标签
                cv2.rectangle(image_cv, (left, bottom - 20), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(image_cv, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)  #识别出的人脸矩形框的底部绘制人脸的名称标签

            # 将处理后的图像转换为QPixmap以便显示在Qt界面中
            height, width, channel = image_cv.shape
            bytesPerLine = 3 * width
            qImg = QImage(image_cv.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
            pixmap = QPixmap.fromImage(qImg)

            # 将pixmap设置到界面的某个QLabel中
            self.label.setPixmap(pixmap)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "人脸识别系统"))
        self.pushButton_img.setText(_translate("MainWindow", "打开图片"))
        self.pushButton_model.setText(_translate("MainWindow", "加载权重"))
        self.pushButton_detect.setText(_translate("MainWindow", "目标检测"))
        self.pushButton_face_recognize.setText(_translate("MainWindow", "人脸识别"))
        self.pushButton_video_detect.setText(_translate("MainWindow", "视频检测"))
        self.pushButton_showdir.setText(_translate("MainWindow", "打开输出文件夹"))

        self.label.setText(_translate("MainWindow", "TextLabel"))

    def init_slots(self):
        self.pushButton_img.clicked.connect(self.load_img)
        self.pushButton_model.clicked.connect(self.select_model)
        self.pushButton_detect.clicked.connect(self.target_detect)
        self.pushButton_showdir.clicked.connect(self.show_dir)
        self.pushButton_video_detect.clicked.connect(self.video_detect)

        self.pushButton_face_recognize.clicked.connect(self.face_recognize)

    def init_logo(self):
        pix = QtGui.QPixmap('')
        self.label.setScaledContents(True)
        self.label.setPixmap(pix)

    def load_img(self):
        print('打开图片')
        img_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "打开图片", "img", "All Files(*)")
        print(img_path)
        self.file_path = img_path
        pixmap = QPixmap(img_path)
        pixmap = pixmap.scaled(self.label.size(), Qt.IgnoreAspectRatio)
        self.label.setPixmap(pixmap)
        self.pushButton_img.setText(self.file_path.split('/')[-1])
        # 清空result文件夹内容
        for i in os.listdir(self.result_path):
            file_data = self.result_path + "/" + i
            os.remove(file_data)

    def select_model(self):
        model_path = QtWidgets.QFileDialog.getOpenFileName(self, "选择模型", "weights", "Model files(*.pt)")
        self.model_path = model_path
        self.pushButton_model.setText(self.model_path[0].split('/')[-1])

    def target_detect(self):
        detect_size = 640
        if self.check_file():
            self.pushButton_img.setEnabled(False)
            self.pushButton_model.setEnabled(False)
            self.pushButton_detect.setEnabled(False)
            self.thread = DetectionThread(self.file_path, self.model_path, detect_size)
            self.thread.start()
            self.thread.signal_done.connect(self.flash_target)

    def check_file(self):
        if self.file_path is None:
            QMessageBox.information(self, '提示', '请先导入数据')
            return False
        if self.model_path is None:
            QMessageBox.information(self, '提示', '请先选择模型')
            return False
        return True

    def flash_target(self):
        img_path = os.getcwd() + '/result/' + [f for f in os.listdir('result')][0]
        pixmap = QPixmap(img_path)
        pixmap = pixmap.scaled(self.label.size(), Qt.IgnoreAspectRatio)
        self.label.setPixmap(pixmap)
        # 刷新完之后恢复按钮状态
        self.pushButton_img.setEnabled(True)
        self.pushButton_model.setEnabled(True)
        self.pushButton_detect.setEnabled(True)

    def show_dir(self):
        path = os.getcwd() + '/' + 'result'
        os.system(f"start explorer {path}")

    def video_detect(self):
        print('打开视频')
        # print(self.label.size())  # (657, 554)
        video_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "打开视频", "video", "All Files(*)")
        self.Video_thread = VideoDetectionThread(self.label, video_path)
        self.Video_thread.start()


class DetectionThread(QThread):

    signal_done = pyqtSignal(int)  # 是否结束信号

    def __init__(self, file_path, model_path, detect_size):
        super(DetectionThread, self).__init__()
        self.file_path = file_path
        self.model_path = model_path
        self.detect_size = detect_size
        self.process = 0
        self.total = 0

    def run(self):
        detect.run(source=self.file_path, weights=self.model_path[0],
                   imgsz=(self.detect_size, self.detect_size))
        self.signal_done.emit(1)  # 发送结束信号


class VideoDetectionThread(QThread):
    signal_done = pyqtSignal(int)

    def __init__(self, label, video_path):
        super(VideoDetectionThread, self).__init__()
        self.label = label
        self.video_path = video_path

    def run(self):
        detect_video.run(weights='weights/best.pt', source=self.video_path, show_label=self.label)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()
    sys.exit(app.exec_())
