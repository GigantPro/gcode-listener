from pathlib import Path
from threading import Thread

from PyQt5 import QtWidgets, uic
import pysine


class Controller(QtWidgets.QMainWindow):
    def __init__(self):
        self.design_path = Path(__file__).parent.joinpath('design/main.ui')
        
        super(Controller, self).__init__()
        uic.loadUi(self.design_path, self)

        self.change_file_button.clicked.connect(self.change_file)
        self.play_button.clicked.connect(self.play)
        
        self.show()
    
    def change_file(self):
        self.path_to_file = Path(QtWidgets.QFileDialog.getOpenFileName()[0])
        
        if self.path_to_file.exists():
            self.file_name.setText(self.path_to_file.name)

            self.text = open(self.path_to_file, 'r').readlines()
            self.gcode_source.clear()
            self.gcode_source.addItems(self.text)
    
    def play(self):
        Player(self).play()

class Player:
    def __init__(self, controller: Controller) -> None:
        self.controller = controller

    def play(self) -> None:
        Thread(target=self.__play).start()
    
    def __play(self) -> None:
        all_items = [str(self.controller.gcode_source.item(i).text())
                     for i in range(self.controller.gcode_source.count())]
        for item_row in range(len(all_items)):
            if not all_items[item_row].strip():
                continue
            
            self.controller.gcode_source.setCurrentRow(item_row)

            timer, frequency = self.__decode_item(all_items[item_row])
            pysine.sine(frequency=frequency, duration=timer / 1000)
    
    def __decode_item(self, item_text: str) -> tuple[float, float]:
        text = item_text.rstrip().lstrip('M300 ')
        items = []
        for item in text.split():
            item = item.replace('P', '').replace('S', '')
            try:
                items.append(float(item.strip()))
            except ValueError:
                continue
        return tuple(items)
