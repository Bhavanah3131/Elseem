from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QWidget, QLabel, QMessageBox
from analysis.run import MainWindow
from windows.selectfile_ui import *
from analysis.data_insertion import insert_files
import os
class FileDialogExample(QMainWindow):
    try:
        def __init__(self):
            super().__init__()
            self.ui = Ui_MainWindow()
            self.ui.setupUi(self)    
            self.ui.pushButton.clicked.connect(lambda: self.open_file_dialog(1))
            self.ui.pushButton_2.clicked.connect(lambda: self.open_file_dialog(2))
            self.ui.pushButton_3.clicked.connect(lambda: self.process_data())
            self.file_path_1 = None
            self.file_path_2 = None
            self.file_name_1 = None
            self.file_name_2 = None
            self.file_type_1 = None
            self.file_type_2 = None 
            

        def open_file_dialog(self, button_id):
            #while True:
                # Open the file dialog
                options = QFileDialog.Options()
                options |= QFileDialog.ReadOnly  # Open in read-only mode
                file_path, _ = QFileDialog.getOpenFileName(self, "Select a File", "", "All Files (*);;Text Files (*.txt)", options=options)
                # If a file was selected, show a confirmation message box
                if file_path:
                    reply = QMessageBox.question(self, 'Confirmation', f"Are you sure you want to select this file?\n{file_path}", 
                                                QMessageBox.Yes | QMessageBox.No)
                    if reply == QMessageBox.Yes:
                        if button_id == 1:
                            self.file_path_1 = file_path
                            self.file_name_1 = os.path.basename(self.file_path_1)
                            self.company_name = self.file_name_1.split('_')[0]
                            self.ui.label.setText(f"{self.company_name}")
                        elif button_id == 2:
                            self.file_path_2 = file_path
                            self.file_name_2 = os.path.basename(self.file_path_2)
                            self.company_name = self.file_name_2.split('_')[0]

                            self.ui.label_2.setText(f"{self.company_name}")
                        #break  # Exit the loop if the user confirms the selection
                    else:
                        QMessageBox.information(self, 'No File Selected', 'No files were selected.')
                    #  break  # Exit the loop if the user declines the selection
                    
        def process_data(self):
            if not self.file_path_1 or not self.file_path_2:
                QMessageBox.warning(self,'Files Not Selected', 'please select both file before processing')
            else:
                # print(self.ui.label.text())
                try:
                    insert_files(self.file_path_1, self.file_path_2)
                    self.hide()
                    window = MainWindow(self.file_name_1, self.file_name_2)
                    window.show()
                except Exception as e:
                    QMessageBox.critical(self,'Error Occured', f'An error occurred: Select Exel file only')
    except Exception as e:
        # print(e)
        pass
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = FileDialogExample()
    window.show()
    sys.exit(app.exec_())
