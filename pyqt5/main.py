import sys
import openai
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QLineEdit, QLabel, QTextEdit, QMessageBox

from knowledgegpt.utils.utils_pdf import process_pdf, process_pdf_page
from knowledgegpt.extractors.pdf_extractor import PDFExtractor

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'File Selection'
        self.left = 100
        self.top = 100
        self.width = 800
        self.height = 600
        self.initUI()
        self.pdf_extractor = None

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.api_key_label = QLabel(self)
        self.api_key_label.move(50, 50)
        self.api_key_label.setText('Enter your OpenAI API key: ')

        self.api_key_textbox = QLineEdit(self)
        self.api_key_textbox.move(200, 50)

        self.file_label = QLabel(self)
        self.file_label.move(50, 100)
        self.file_label.setText('Selected file: ')

        self.file_path = QLineEdit(self)
        self.file_path.setGeometry(150, 100, 400, 25)
        self.file_path.setReadOnly(True)

        self.select_file_button = QPushButton('Select File', self)
        self.select_file_button.setToolTip('Click to select file')
        self.select_file_button.setGeometry(570, 100, 100, 25)
        self.select_file_button.clicked.connect(self.on_file_select)

        self.query_label = QLabel(self)
        self.query_label.setGeometry(50, 150, 150, 25)
        self.query_label.setText('Enter a question: ')

        self.query_textbox = QLineEdit(self)
        self.query_textbox.setGeometry(200, 150, 520, 25)

        self.ask_button = QPushButton('Ask', self)
        self.ask_button.setToolTip('Click to ask')
        self.ask_button.setGeometry(690, 150, 100, 25)
        self.ask_button.clicked.connect(self.on_ask)

        self.answer_label = QLabel(self)
        self.answer_label.setGeometry(50, 200, 150, 25)
        self.answer_label.setText('Answer: ')

        self.answer_textbox = QTextEdit(self)
        self.answer_textbox.setGeometry(200, 200, 590, 300)
        self.answer_textbox.setReadOnly(True)

        self.quit_button = QPushButton('Quit', self)
        self.quit_button.setGeometry(690, 550, 100, 25)
        self.quit_button.clicked.connect(self.close)

        self.show()

    def on_file_select(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open file', '', 'PDF files (*.pdf)')
        self.file_path.setText(file_path)

    def on_ask(self):
        openai.api_key = self.api_key_textbox.text()
        pdf_file_path = self.file_path.text()
        query = self.query_textbox.text()

        if self.pdf_extractor is None:
            self.pdf_extractor = PDFExtractor(pdf_file_path, extraction_type="paragraph", embedding_extractor="hf", model_lang="en", is_turbo=True)
        answer, prompt, messages = self.pdf_extractor.extract(query, max_tokens=1500)

        self.answer_textbox.setPlainText(answer)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', "Are you sure you want to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
