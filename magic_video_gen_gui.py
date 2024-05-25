import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi
import os
from concurrent.futures import ThreadPoolExecutor
from magic_video_gen import magic_video_render

class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("magic_video_gen_qt5_gui.ui", self)
        self.audio_browse.clicked.connect(lambda: self.browse_files(audio=True, files_read=True))
        self.image_browse.clicked.connect(lambda: self.browse_files(image=True, files_read=True))
        self.render_browse.clicked.connect(lambda: self.get_render_directory())
        self.render.clicked.connect(lambda: self.render_videos())
        self.cancel_render.clicked.connect(lambda: self.run_script(stop=True))
        
        self.__audio_files = None
        self.__image_files = None
        self.__render_directory = None
        
        self.executor = ThreadPoolExecutor(max_workers=1)
        
    def browse_files(self, audio=False, image=False, files_read=True, directory_read=False):
        title = None
        default_open = None
        file_type = None
        
        if audio:
            title = "Open Audio Files"
            default_open = "./"
            file_type = "Audio Files (*.wav)"
        
        if image:
            title = "Open Image Files"
            default_open = "./"
            file_type = "Image Files (*.jpg)"
        
        if files_read:
            files, file_type = QFileDialog.getOpenFileNames(self, title, default_open, file_type)
        
        if image:
            self.__image_files = files
        
        if audio:
            self.__audio_files = files
        
        if directory_read:
            dialog = QFileDialog()
            folder_path = dialog.getExistingDirectory(self, "Select Folder Containing WAV Files")
        
        string = ""
        for i, filename in enumerate(files):
            string += f"{i + 1}: {filename}\n"
        print(string)
        
        try:
            if audio: self.audio_dir.setText(f"{string}")
            if image: self.image_dir.setText(f"{string}")
        except Exception as e:
            print(f"Error: {e}")
        
    
    def get_render_directory(self):
        dialog = QFileDialog()
        folder_path = dialog.getExistingDirectory(self, "Select Render Folder", "./")
        self.__render_directory = folder_path
        self.render_dir.setText(folder_path)
    
    def run_script(self, stop=False):
        # os.system(f'python magic_video_gen.py --audio_list "{self.__audio_files}" --image_list "{self.__image_files}" --render_dir "{self.__render_directory}"')
        if stop:
            raise "Error"
        magic_video_render(audio_list=self.__audio_files, 
                           image_list=self.__image_files, 
                           render_directory=self.__render_directory)
    
    def render_videos(self):
        self.executor.submit(self.run_script)
    
    def closeEvent(self):
        self.executor.shutdown(wait=False, cancel_futures=True)
        

app = QApplication(sys.argv)
mainwindow = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(900)
widget.setFixedHeight(700)
widget.show()
sys.exit(app.exec_())
