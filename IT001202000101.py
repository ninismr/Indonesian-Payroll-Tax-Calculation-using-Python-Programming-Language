from PyQt5.QtWidgets import (
    QApplication, QFileDialog, QWidget, QLabel, QAction,
    QPushButton, QFormLayout, QTextEdit, QMenuBar, QMessageBox
)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setUI()


    def setUI(self):
        self.menubar = QMenuBar()
        self.menubar.setNativeMenuBar(False)
        self.menubar.show()

        self.file_menu = self.menubar.addMenu('File')
        self.help_menu = self.menubar.addMenu('Help')

        self.action_save = QAction('Save', self)
        self.action_save.setShortcut('Ctrl+S')
        
        self.action_open = QAction('Open', self)
        self.action_open.setShortcut('Ctrl+O')

        self.action_about = QAction('About', self)
        
        self.action_quit = QAction('Quit', self)
        self.action_quit.setShortcut('Ctrl+Q')
        
        self.file_menu.addAction(self.action_save)
        self.file_menu.addAction(self.action_open)
        self.help_menu.addAction(self.action_about)
        self.help_menu.addSeparator()
        self.help_menu.addAction(self.action_quit)
        
        self.editor = QTextEdit()
        self.editor.setPlaceholderText('Please input your Annual Gross Income in the first row and your Non-Taxable Income in the second row!')
        self.file_name = ""
        self.Calc_button = QPushButton('Calculate')
        AGI_label = QLabel('Annual Gross Income:')
        self.AGI_result = QLabel('')
        NTI_label = QLabel('Non-Taxable Income:')
        self.NTI_result = QLabel('')
        TI_label = QLabel('Taxable Income:')
        self.TI_result = QLabel('')
        AIT_label = QLabel('Annual Income Tax:')
        self.AIT_result = QLabel('')

        form_layout = QFormLayout()
        form_layout.addRow(self.menubar)
        form_layout.addRow(self.editor)
        form_layout.addRow(self.Calc_button)
        form_layout.addRow(AGI_label, self.AGI_result)
        form_layout.addRow(NTI_label, self.NTI_result)
        form_layout.addRow(TI_label, self.TI_result)
        form_layout.addRow(AIT_label, self.AIT_result)

        self.action_save.triggered.connect(self.Save_input)
        self.action_open.triggered.connect(self.Open_file)
        self.action_about.triggered.connect(self.about)
        self.action_quit.triggered.connect(self.quit)
        self.Calc_button.clicked.connect(self.calculate)

        self.resize(370, 250)
        self.show()
        self.setLayout(form_layout)
        self.setWindowTitle('Annual Income Tax Calculation')
        self.setStyleSheet('background-color: #AFEEEE;')
        self.menubar.setStyleSheet('background-color: #FFFFF0;')
        self.editor.setStyleSheet('background-color: #FFEFD5;')
        self.Calc_button.setStyleSheet('background-color: #FFEFD5;')


    def calculate(self):
        Input = self.editor.toPlainText()
        AGI,NTI,*_ = Input.split('\n') + [None]

        if AGI and NTI:
            if AGI.isnumeric() and NTI.isnumeric():
                TI = int(AGI) - int(NTI)

                if TI <= 0:
                    AIT = 0
                elif TI <= 50000000:
                    AIT = TI * 0.05
                elif TI > 50000000 and TI <= 250000000:
                    AIT = (0.05 * 50000000) + (TI - 50000000) * 0.15
                elif TI > 250000000 and TI <= 500000000:
                    AIT = (0.05 * 50000000) + (0.15 * 200000000) + (TI - 250000000) * 0.25
                elif TI > 500000000:
                    AIT = (0.05 * 50000000) + (0.15 * 200000000) + (0.25 * 250000000) + (TI - 500000000) * 0.3
                
                AGI_in = '{:,.2f}'.format(int(AGI))
                NTI_in = '{:,.2f}'.format(int(NTI))   
                TI_res = '{:,.2f}'.format(int(TI))
                AIT_res = '{:,.2f}'.format(int(AIT))

                self.AGI_result.setText(str("IDR " + AGI_in))
                self.NTI_result.setText(str("IDR " + NTI_in))
                self.TI_result.setText(str("IDR " + TI_res))
                self.AIT_result.setText(str("IDR " + AIT_res))

            else:
                self.AGI_result.setText('Please enter the number only!')
                self.NTI_result.setText('Please enter the number only!')
                self.TI_result.setText('Please enter the number only!')
                self.AIT_result.setText('Please enter the number only!')


    def Save_input(self):
        name, _ = QFileDialog.getSaveFileName(self, 'Save', self.file_name, 'TXT(*.txt)')
        if name:  
            self.file_name = name  
            file = open(name, 'w')  
            text = self.editor.toPlainText()
            file.write(text)
            file.close()  


    def Open_file(self):
        name, _ = QFileDialog.getOpenFileName(self, 'Open', '', 'TXT(*.txt)')
        if name: 
            self.file_name = name 
            file = open(name, 'r')  
            with file:  
                data = file.read()
                self.editor.setPlainText('')
                self.editor.setPlainText(data)
            file.close() 
            self.calculate()


    def about(self):
        msg = QMessageBox()
        msg.setText('This app helps you to more easily calculate your annual income tax ^_^')
        msg.exec_()


    def quit(self):
        QApplication.quit()


app = QApplication([])
window = MainWindow()
window.show()
app.exec_()