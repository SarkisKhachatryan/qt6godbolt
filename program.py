import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QComboBox, QHBoxLayout, QLabel
from PyQt6.QtCore import QTimer
import subprocess
import tempfile
import os


class CPPToASMConverter(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create text boxes
        self.cpp_code_box = QTextEdit(self)
        self.asm_code_box = QTextEdit(self)
        self.asm_code_box.setReadOnly(True)

        # Create combo boxes for compiler and optimization level selection
        self.compiler_box = QComboBox(self)
        self.compiler_box.addItems(["g++", "clang++"])
        self.compiler_box.currentIndexChanged.connect(self.compile_code)

        self.optimization_box = QComboBox(self)
        self.optimization_box.addItems(["-O0", "-O1", "-O2", "-O3", "-Os"])
        self.optimization_box.currentIndexChanged.connect(self.compile_code)

        # Create layout for the combo boxes
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel("Compiler:"))
        hbox.addWidget(self.compiler_box)
        hbox.addWidget(QLabel("Optimization Level:"))
        hbox.addWidget(self.optimization_box)

        # Create main layout
        layout = QVBoxLayout()
        layout.addLayout(hbox)
        layout.addWidget(self.cpp_code_box)
        layout.addWidget(self.asm_code_box)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Set up a timer to compile the code in real-time
        self.timer = QTimer(self)
        self.timer.setInterval(1000)  # 1 second delay
        self.timer.timeout.connect(self.compile_code)
        self.timer.start()

    def compile_code(self):
        compiler = self.compiler_box.currentText()
        optimization_level = self.optimization_box.currentText()
        cpp_code = self.cpp_code_box.toPlainText()

        with tempfile.NamedTemporaryFile(suffix=".cpp") as cpp_file:
            cpp_file.write(cpp_code.encode())
            cpp_file.flush()

            output_file = tempfile.mktemp()
            cmd = f"{compiler} {optimization_level} -S {cpp_file.name} -o {output_file}"
            try:
                subprocess.run(cmd, shell=True, check=True)
                with open(output_file, 'r') as asm_file:
                    asm_code = asm_file.read()
                os.unlink(output_file)
                self.asm_code_box.setPlainText(asm_code)
            except subprocess.CalledProcessError as e:
                self.asm_code_box.setPlainText("Compilation failed")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = CPPToASMConverter()
    main_window.setWindowTitle('C++ to Assembly Converter')
    main_window.resize(800, 600)
    main_window.show()

    sys.exit(app.exec())
