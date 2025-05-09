from PyQt6.QtWidgets import *
from grading_view import *
from grading_model import *

class Controller(QMainWindow, Ui_GradingAlexTarasov):
    def __init__(self) -> None:
        """
        Set up the grade calculator GUI
        """
        super().__init__()
        self.setupUi(self)

        self.labels = [self.label_1, self.label_2, self.label_3, self.label_4]
        self.inputs = [self.scoreInput1, self.scoreInput2, self.scoreInput3, self.scoreInput4]

        for label in self.labels:
            label.setHidden(True)
        for input_box in self.inputs:
            input_box.setHidden(True)

        self.attemptsInput.textChanged.connect(self.update_score_fields)
        self.submitButton.clicked.connect(self.submit)

    def update_score_fields(self) -> None:
        """
        Show score labels and inputs
        """
        value = self.attemptsInput.text().strip()
        if not value.isdigit():
            for i in range(4):
                self.labels[i].setHidden(True)
                self.inputs[i].setHidden(True)
            return

        count = int(value)
        for i in range(4):
            self.labels[i].setHidden(i >= count)
            self.inputs[i].setHidden(i >= count)

    def submit(self) -> None:
        """
        Handle the submit button click
        """
        name = self.studentNamInput.text().strip()
        attempts = self.attemptsInput.text().strip()

        if name == "":
            self.statusMessage.setText("Name is required")
            self.statusMessage.setStyleSheet("color: red")
            return

        if not attempts.isdigit():
            self.statusMessage.setText("Invalid attempt number")
            self.statusMessage.setStyleSheet("color: red")
            return

        count = int(attempts)
        if count < 1 or count > 4:
            self.statusMessage.setText("Attempts must be 1–4")
            self.statusMessage.setStyleSheet("color: red")
            return

        scores = []
        for i in range(count):
            text = self.inputs[i].text().strip()
            if not text.isdigit():
                self.statusMessage.setText("Invalid score")
                self.statusMessage.setStyleSheet("color: red")
                return
            score = int(text)
            if score < 0 or score > 100:
                self.statusMessage.setText("Score must be 0–100")
                self.statusMessage.setStyleSheet("color: red")
                return
            scores.append(score)

        while len(scores) < 4:
            scores.append(0)

        final = get_best_score(scores)
        save_result(name, scores, final)
        self.statusMessage.setText("Submitted")
        self.statusMessage.setStyleSheet("color: green")

        self.studentNamInput.clear()
        self.attemptsInput.clear()
        for input_box in self.inputs:
            input_box.clear()
        self.update_score_fields()
