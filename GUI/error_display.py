from PyQt5.QtWidgets import QMessageBox


def displayError(msg, advice="Unknown Error"):
    box = QMessageBox()
    box.setIcon(QMessageBox.Critical)
    box.setText(str(msg))
    box.setInformativeText(advice)
    box.setWindowTitle("Error")
    box.exec_()
