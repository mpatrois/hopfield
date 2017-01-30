#!/usr/bin/env python
#-*- coding:utf-8 -*-

# from PyQt4 import QtCore, QtGui

# class MyDialog(QtGui.QDialog):
#     def __init__(self, parent=None):
#         super(MyDialog, self).__init__(parent)

#         self.buttonBox = QtGui.QDialogButtonBox(self)
#         self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
#         self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)

#         self.textBrowser = QtGui.QTextBrowser(self)
#         self.textBrowser.append("This is a QTextBrowser!")

#         self.verticalLayout = QtGui.QVBoxLayout(self)
#         self.verticalLayout.addWidget(self.textBrowser)
#         self.verticalLayout.addWidget(self.buttonBox)

# class MyWindow(QtGui.QWidget):
#     def __init__(self, parent=None):
#         super(MyWindow, self).__init__(parent)

#         self.pushButtonWindow = QtGui.QPushButton(self)
#         self.pushButtonWindow.setText("Click Me!")
#         self.pushButtonWindow.clicked.connect(self.on_pushButton_clicked)

#         self.layout = QtGui.QHBoxLayout(self)
#         self.layout.addWidget(self.pushButtonWindow)

#         self.dialogTextBrowser = MyDialog(self)

#     @QtCore.pyqtSlot()
#     def on_pushButton_clicked(self):
#         self.dialogTextBrowser.exec_()


# if __name__ == "__main__":
#     import sys

#     app = QtGui.QApplication(sys.argv)
#     app.setApplicationName('MyWindow')

#     main = MyWindow()
#     main.show()

#     sys.exit(app.exec_())



    

# import sys
# from PyQt4.QtCore import *
# from PyQt4.QtGui import *


# data = {'col1':['','',''], 'col2':['','',''], 'col3':['','','']}
 
# class MyTable(QTableWidget):
#     def __init__(self, data, *args):
#         QTableWidget.__init__(self, *args)
#         self.data = data
#         self.setmydata()
#         self.resizeColumnsToContents()
#         self.resizeRowsToContents()
#         self.verticalHeader().hide();
#         self.horizontalHeader().hide();
#         self.setFixedSize(self.horizontalHeader().length(), self.verticalHeader().length());

#         self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff);
#         self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff);
 
#     def setmydata(self):
#         for n, key in enumerate(sorted(self.data.keys())):
#             print(key)
#             for m, item in enumerate(self.data[key]):
#                 newitem = QTableWidgetItem(item)
#                 newitem.setBackground(QColor(100,100,150))
#                 newitem.setFlags(Qt.NoItemFlags)
#                 self.setItem(m, n, newitem)

#         # self.setItem(0,1,QTableWidgetItem(str(237)))

# class Example(QWidget):
    
#     def __init__(self):
#         super(Example, self).__init__()
        
#         self.initUI()
        
#     def initUI(self):
        
#         title = QLabel('Title')
#         author = QLabel('Author')
#         review = QLabel('Review')

#         titleEdit = QLineEdit()
#         authorEdit = QLineEdit()
#         reviewEdit = QTextEdit()

#         table  = MyTable(data, 5, 5)
#         table2 = MyTable(data, 5, 5)
#         table3 = MyTable(data, 5, 5)
#         # table = MyTable(data, 1, 3)
       

#         grid = QGridLayout()
#         grid.setSpacing(0)

#         grid.addWidget(table, 0, 0)
#         grid.addWidget(table2, 0, 1)
#         grid.addWidget(table3, 0, 2)

#         # grid.addWidget(title, 1, 0)
#         # grid.addWidget(titleEdit, 1, 1)

#         # grid.addWidget(author, 2, 0)
#         # grid.addWidget(authorEdit, 2, 1)

#         # grid.addWidget(review, 3, 0)
#         # grid.addWidget(reviewEdit, 3, 1, 5, 1)
        
#         self.setLayout(grid) 
        
#         self.setGeometry(300, 300, 350, 300)
#         self.setWindowTitle('Review')    
#         self.show()
        
# def main():
    
#     app = QApplication(sys.argv)
#     ex = Example()
#     sys.exit(app.exec_())


# if __name__ == '__main__':
#     main()
#     
#     

# from PyQt4 import QtGui

# class Window(QtGui.QWidget):
#     def __init__(self, val):
#         QtGui.QWidget.__init__(self)
#         mygroupbox = QtGui.QGroupBox('this is my groupbox')
#         myform = QtGui.QFormLayout()
#         labellist = []
#         combolist = []
#         for i in range(val):
#             labellist.append(QtGui.QLabel('mylabel'))
#             combolist.append(QtGui.QComboBox())
#             myform.addRow(labellist[i],combolist[i])
#         mygroupbox.setLayout(myform)
#         scroll = QtGui.QScrollArea()
#         scroll.setWidget(mygroupbox)
#         scroll.setWidgetResizable(True)
#         scroll.setFixedHeight(400)
#         layout = QtGui.QVBoxLayout(self)
#         layout.addWidget(scroll)

# if __name__ == '__main__':

#     import sys
#     app = QtGui.QApplication(sys.argv)
#     window = Window(25)
#     window.setGeometry(500, 300, 300, 400)
#     window.show()
#     sys.exit(app.exec_())