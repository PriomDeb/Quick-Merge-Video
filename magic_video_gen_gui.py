import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi
import os
from concurrent.futures import ThreadPoolExecutor
from magic_video_gen import magic_video_render

APP_NAME = "Magic Video Gen"
VERSION = "1.0"
DEVELOPER = "Priom Deb"
WINDOW_NAME = f"{APP_NAME} v{VERSION} by {DEVELOPER}"

class EmittingStream(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))

    def flush(self):
        pass

class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("magic_video_gen_qt5_gui.ui", self)
        self.audio_browse.clicked.connect(lambda: self.browse_files(audio=True, files_read=True))
        self.image_browse.clicked.connect(lambda: self.browse_files(image=True, files_read=True))
        self.render_browse.clicked.connect(lambda: self.get_render_directory())
        self.render.clicked.connect(lambda: self.render_videos())
        self.cancel_render.clicked.connect(lambda: self.run_script(stop=True))
        # self.button.clicked.connect(self.button_clicked)
        self.track_number.setMaximum(1000)
        # self.warning.setVisible(False)
        # self.button.setVisible(False)
        self.log_output.setVisible(False)
        self.close_log.setVisible(False)
        self.close_log.clicked.connect(self.close_log_window)
        
        self.__audio_files = None
        self.__image_files = None
        self.__render_directory = None
        
        self.executor = ThreadPoolExecutor(max_workers=1)
        
        self.log_output.setReadOnly(True)
        sys.stdout = EmittingStream(textWritten=self.normal_output_written)
    
    def normal_output_written(self, text):
        cursor = self.log_output.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.log_output.setTextCursor(cursor)
        self.log_output.ensureCursorVisible()
    
    def close_log_window(self):
        self.close_log.setVisible(False)
        self.log_output.setVisible(False)
    
    def button_clicked(self):
        album = self.album.text()
        track = self.track.text()
        artist = self.artist.text()
        credit = self.credit.text()
        track_number = self.track_number.text()
        
        print(f"Album: {album} \nTrack: {track} \nArtist: {artist} \nCredit: {credit} \nTrack Number: {track_number}")
        
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
        
        album = self.album.text()
        track = self.track.text()
        artist = self.artist.text()
        credit = self.credit.text()
        track_number = self.track_number.text()
        print(f"Album: {album} \nTrack: {track} \nArtist: {artist} \nCredit: {credit} \nTrack Number: {track_number}")
        
        magic_video_render(audio_list=self.__audio_files, 
                           image_list=self.__image_files, 
                           render_directory=self.__render_directory,
                           video_album_title=album,
                           video_track_title=track,
                           artist_name=artist,
                           track_number_start=track_number,
                           credit_text=credit
                           )
        print(f"{len(self.__audio_files)} Videos Rendered Successfully. \nThank you for using Magic Video Gen by Priom Deb.")
    
    def render_videos(self):
        self.log_output.setVisible(True)
        self.close_log.setVisible(True)
        self.executor.submit(self.run_script)
    
    def closeEvent(self):
        self.executor.shutdown(wait=False, cancel_futures=True)
        

app = QApplication(sys.argv)
mainwindow = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(920)
widget.setFixedHeight(800)
widget.setWindowTitle(WINDOW_NAME)
# widget.resize(920, 800)
widget.show()
sys.exit(app.exec_())

# https://coolors.co/a49e8d-504136-689689-b2e6d4-83e8ba
# pyinstaller --onefile --icon=batteryfyAppIcon.ico -w magic_video_gen_gui.py
# pyinstaller --onefile -w magic_video_gen_gui.py
