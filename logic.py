from PyQt6.QtWidgets import *
from gui import *
import csv


class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.john_votes: int = 0
        self.jill_votes: int = 0
        self.poll_label.hide()
        self.poll_display_status: bool = False

        self.poll_button.clicked.connect(lambda: self.toggle_poll_display())
        self.submit_button.clicked.connect(lambda: self.submit())

    def toggle_poll_display(self) -> None:
        """
        Function to toggle display of poll results
        """
        if self.poll_display_status:
            self.poll_label.hide()
            self.poll_button.setText('Show current polls:')
            self.poll_display_status = False
        else:
            self.john_votes = 0
            self.jill_votes = 0
            with open('voters.csv', 'r') as file:
                reader = csv.reader(file)
                voter_list = list(reader)
                for line in voter_list:
                    self.john_votes += int(line[1])
                    self.jill_votes += int(line[2])
            self.poll_label.setText(f'John votes: {self.john_votes} \t Jill votes: {self.jill_votes}')
            self.poll_label.show()
            self.poll_button.setText('Hide results:')
            self.poll_display_status = True

    def submit(self) -> None:
        """
        Function to submit vote and update current results
        """
        self.error_label.hide()
        try:
            user_ID: str = str(int(self.id_entry.text()))
            if len(user_ID) < 9:
                raise ValueError
            with open('voters.csv', 'a', newline= '\n') as votercsv:
                content = csv.writer(votercsv)
                with open('voters.csv', 'r') as votercsv_check:
                    for line in votercsv_check:
                        if user_ID in line:
                            raise UnboundLocalError
                    if self.john_button.isChecked():
                        content.writerow([user_ID, 1, 0])
                    elif self.jill_button.isChecked():
                        content.writerow([user_ID, 0, 1])
                    else:
                        raise RuntimeError
            if self.poll_display_status:
                self.toggle_poll_display()



        except ValueError:
            self.error_label.show()
            self.error_label.setText('Enter 9 digit number')
        except UnboundLocalError:
            self.error_label.show()
            self.error_label.setText('ID already registered under vote')
        except RuntimeError:
            self.error_label.show()
            self.error_label.setText('Must Select Candidate')



