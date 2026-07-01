import argparse
import sys
import os
import json
import yaml
import xmltodict
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, 
                             QLabel, QFileDialog, QMessageBox)
from PyQt6.QtCore import QThread, pyqtSignal

def load_data(file_path):
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    if ext == '.json':
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            raise ValueError(f"Błąd pliku JSON: {e}")
    elif ext in ['.yml', '.yaml']:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            raise ValueError(f"Błąd pliku YAML: {e}")
    elif ext == '.xml':
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return xmltodict.parse(f.read())
        except Exception as e:
            raise ValueError(f"Błąd pliku XML: {e}")
    else:
        raise ValueError(f"Format {ext} nie jest obsługiwany.")

def save_data(data, file_path):
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    if ext == '.json':
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    elif ext in ['.yml', '.yaml']:
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
    elif ext == '.xml':
        if not isinstance(data, dict) or len(data) != 1:
            data = {'root': data}
        xml_data = xmltodict.unparse(data, pretty=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(xml_data)
    else:
        raise ValueError(f"Format {ext} nie jest obsługiwany przy zapisie.")


#Wielowątkowość dla interfejsu
class ConversionWorker(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str)
    success = pyqtSignal(str)

    def __init__(self, input_path, output_path):
        super().__init__()
        self.input_path = input_path
        self.output_path = output_path

    def run(self):
        try:
            data = load_data(self.input_path)
            save_data(data, self.output_path)
            self.success.emit("Konwersja zakończona pomyślnie!")
        except Exception as e:
            self.error.emit(str(e))
        finally:
            self.finished.emit()


# Interfejs Graficzny
class ConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Konwerter Danych IT")
        self.resize(400, 200)
        self.input_path = None
        self.output_path = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label_info = QLabel("Wybierz pliki do konwersji (.json, .yml, .xml)")
        layout.addWidget(self.label_info)

        self.btn_input = QPushButton("1. Wybierz plik wejściowy")
        self.btn_input.clicked.connect(self.select_input)
        layout.addWidget(self.btn_input)

        self.btn_output = QPushButton("2. Wybierz miejsce zapisu")
        self.btn_output.clicked.connect(self.select_output)
        layout.addWidget(self.btn_output)

        self.btn_convert = QPushButton("3. Konwertuj (W tle)!")
        self.btn_convert.clicked.connect(self.run_conversion)
        self.btn_convert.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        layout.addWidget(self.btn_convert)

        self.setLayout(layout)

    def select_input(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Wybierz plik wejściowy")
        if file_path:
            self.input_path = file_path
            self.btn_input.setText(f"Wejście: {os.path.basename(file_path)}")

    def select_output(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Wybierz miejsce zapisu")
        if file_path:
            self.output_path = file_path
            self.btn_output.setText(f"Wyjście: {os.path.basename(file_path)}")

    def run_conversion(self):
        if not self.input_path or not self.output_path:
            QMessageBox.warning(self, "Błąd", "Wybierz oba pliki przed konwersją!")
            return

        # Uruchomienie wątku roboczego
        self.btn_convert.setEnabled(False)
        self.btn_convert.setText("Przetwarzanie...")
        
        self.worker = ConversionWorker(self.input_path, self.output_path)
        self.worker.success.connect(self.on_success)
        self.worker.error.connect(self.on_error)
        self.worker.finished.connect(self.on_finished)
        self.worker.start()

    def on_success(self, message):
        QMessageBox.information(self, "Sukces", message)

    def on_error(self, message):
        QMessageBox.critical(self, "Błąd", message)

    def on_finished(self):
        self.btn_convert.setEnabled(True)
        self.btn_convert.setText("3. Konwertuj (W tle)!")


def main():
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(description="Program do konwersji danych")
        parser.add_argument("input_file", help="Ścieżka do pliku wejściowego")
        parser.add_argument("output_file", help="Ścieżka do pliku wyjściowego")
        args = parser.parse_args()

        if not os.path.isfile(args.input_file):
            print(f"Błąd: Plik '{args.input_file}' nie istnieje!")
            sys.exit(1)
            
        try:
            data = load_data(args.input_file)
            save_data(data, args.output_file)
            print("Konwersja z konsoli zakończona pomyślnie.")
        except Exception as e:
            print(e)
            sys.exit(1)
    else:
        app = QApplication(sys.argv)
        window = ConverterApp()
        window.show()
        sys.exit(app.exec())

if __name__ == "__main__":
    main()