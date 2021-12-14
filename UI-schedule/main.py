'''
Визуальная часть должна иметь при себе:
a.	Минимум 3 вкладки, в каждой из которых содержится информация из отдельной таблицы в базе данных.
b.	Внутри каждой вкладки информация должна отображаться в виде таблиц.
c.	Внутри каждой вкладки должна отображаться кнопка с обновлением информации.
d.	Внутри каждой таблицы должны отображаться все поля из таблицы в базе данных в виде колонок
e.	Внутри каждой таблицы после каждой строки записи должны быть отображены кнопки изменения и удаления записи
f.	В конце каждой таблицы должна находиться пустая строка с кнопкой для добавления новой записи.
'''

from datetime import datetime, date, time
from PyQt5.QtCore import qInfo
import psycopg2
import sys
from PyQt5.QtWidgets import (QApplication, QCheckBox, QInputDialog, QLineEdit, QSpinBox, QWidget,
                             QTabWidget, QAbstractScrollArea,
                             QVBoxLayout, QHBoxLayout,
                             QTableWidget, QGroupBox,
                             QTableWidgetItem, QPushButton, QMessageBox, QMainWindow)


class MainWindow(QWidget):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.datetime()
        self._connect_to_db()
        self.setWindowTitle("Schedule")

        self.vbox = QVBoxLayout(self)
        self.tabs = QTabWidget(self)
        self.vbox.addWidget(self.tabs)
        
        self._create_schedule_tab()
     
    
    def datetime(self):
        self.row_max = 5
        self.day_name = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        start = date(2021, 9, 1) # Start date
        d = datetime.now() # Today
        self.week = d.isocalendar()[1] - start.isocalendar()[1] + 1 # Counting number of week now
        if self.week%2 == 1:
            self.top_week = True
        else:
            self.top_week = False     
    
    
    def _connect_to_db(self):
        self.conn = psycopg2.connect(database="schedule",
                                     user="postgres",
                                     password="sql_GH0_Fr1",
                                     host="localhost",
                                     port="5432")

        self.cursor = self.conn.cursor()
        

    def _create_schedule_tab(self):
        
        self.schedule_tab = QWidget()
        self.tabs.addTab(self.schedule_tab, "Schedule")
        
        # wid = QSpinBox(self)
        # wid.move(1, 6)
        # print(wid)
        
        self.dof = int(input("Choice day of week (where 1 - Monday, 6 - Saturday)\n"))
        
        self.day_gbox = QGroupBox(f"{self.day_name[self.dof - 1]}")

        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()

        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)

        self.shbox1.addWidget(self.day_gbox)

        self._create_one_day_table()

        self.update_schedule_button = QPushButton("Update")
        self.shbox2.addWidget(self.update_schedule_button)
        self.update_schedule_button.clicked.connect(self._update_day_table)
        
        self.saveButton = QPushButton("Save all")
        self.shbox2.addWidget(self.saveButton)
        self.saveButton.clicked.connect(lambda:self._change_day_from_table(self.row_max))
        self.saveButton.clicked.connect(self._update_day_table)
        
        self.schedule_tab.setLayout(self.svbox)


    def _create_one_day_table(self):
        self.monday_table = QTableWidget()
        self.monday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        # Количесвто колонок 
        self.monday_table.setColumnCount(5)
        self.monday_table.setHorizontalHeaderLabels(["Start time", "Subject", "Full name", "room", "Delete"])

        self._update_day_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.monday_table)
        self.day_gbox.setLayout(self.mvbox)


    def _update_day_table(self):
        self.records = []
        self._connect_to_db()
        self.cursor.execute(f"SELECT subject.subject_name, timetable.start_time, teachers.full_name, teachers.fk_subject, timetable.id, timetable.room\
                        FROM subject\
                        INNER JOIN timetable ON subject.id = timetable.fk_subject\
                        INNER JOIN teachers ON subject.id = teachers.fk_subject\
                        WHERE dof = {self.dof} and top_week = {self.top_week}\
                        ORDER BY timetable.start_time")
        self.records = list(self.cursor.fetchall())
        self.monday_table.setRowCount(self.row_max)
        for i, r in enumerate(self.records):
            r = list(r)
            # Не смог передать на какую именно кнопку нажимать :(
            drop_button1 = QPushButton("Delete")
            drop_button2 = QPushButton("Delete")
            drop_button3 = QPushButton("Delete")
            drop_button4 = QPushButton("Delete")
            drop_button5 = QPushButton("Delete")
            self.monday_table.setItem(i, 0, QTableWidgetItem(str(r[1]))) # time
            self.monday_table.setItem(i, 1, QTableWidgetItem(str(r[0]))) # Subject
            self.monday_table.setItem(i, 2, QTableWidgetItem(str(r[2]))) # Full_name
            self.monday_table.setItem(i, 3, QTableWidgetItem(str(r[5]))) # room
            self.monday_table.setCellWidget(0, 4, drop_button1)
            self.monday_table.setCellWidget(1, 4, drop_button2)
            self.monday_table.setCellWidget(2, 4, drop_button3)
            self.monday_table.setCellWidget(3, 4, drop_button4)
            self.monday_table.setCellWidget(4, 4, drop_button5)
            drop_button1.clicked.connect(lambda:self._delete_row(0)) 
            drop_button2.clicked.connect(lambda:self._delete_row(1)) 
            drop_button3.clicked.connect(lambda:self._delete_row(2)) 
            drop_button4.clicked.connect(lambda:self._delete_row(3)) 
            drop_button5.clicked.connect(lambda:self._delete_row(4)) 
        self.monday_table.resizeRowsToContents()
        print(self.records)
        print("UPDATE sucssed")
        # Clear empty row    
        for j in range(len(self.records), self.row_max):
            self.monday_table.setItem(j, 0, QTableWidgetItem(None)) # Subject
            self.monday_table.setItem(j, 1, QTableWidgetItem(None)) # Subject
            self.monday_table.setItem(j, 2, QTableWidgetItem(None)) # Full_name
            self.monday_table.setItem(j, 3, QTableWidgetItem(None)) # room
        
        
    def _delete_row(self,rowNum):
        try: 
            print(self.records[rowNum])
        except:
            return
        try:
            self.cursor.execute(f"DELETE FROM timetable WHERE id = {self.records[rowNum][4]};")
            self.conn.commit()
            self._update_day_table()
            print("DELETE sucssed")
        except:
            QMessageBox.about(self, "Error", f"Can't delete row = {rowNum+1}")
        self._update_day_table()
    

    def _change_day_from_table(self, rowNum):
        '''       [ 0                            1                    2                   3                 4                 5     ]
        records = [subject.subject_name, timetable.start_time, teachers.full_name, teachers.fk_subject, timetable.id, timetable.room]
        '''
        # Update row  
        for j in range(len(self.records)):
            row = list()
            for i in range(self.monday_table.columnCount()):
                try:
                    row.append(self.monday_table.item(j, i).text())
                except:
                    row.append(None)
            try:
                self.cursor.execute(f"UPDATE timetable SET start_time = '{row[0]}' WHERE id = {self.records[j][4]}")
                self.cursor.execute(f"UPDATE subject SET subject_name = '{row[1]}' WHERE id = {self.records[j][3]}")
                self.cursor.execute(f"UPDATE teachers SET full_name = '{row[2]}' WHERE id = {self.records[j][3]}")
                self.cursor.execute(f"UPDATE timetable SET room = '{row[3]}' WHERE id = {self.records[j][4]}")
                print(f"UPDATE sucssed")
                self.conn.commit()
            except:
                QMessageBox.about(self, "Error", "SQL UPDATE error")
                
        # Insert row      
        for j in range(len(self.records), self.row_max):
            row = list()
            for i in range(self.monday_table.columnCount()-1):
                try:
                    row.append(self.monday_table.item(j, i).text())
                except:
                    row.append(None)
            # print(row)
            
            try:
                print("INSERT", row)
                if None in row or '' in row:
                    print("None in row")
                    self.cursor.execute("error sql injection to stop try-except")

                self.cursor.execute("SELECT id FROM subject ORDER BY id DESC LIMIT 1;")
                self.last_id_sub = self.cursor.fetchall()[0][0] + 1
                self.cursor.execute(f"INSERT INTO subject(id, subject_name) VALUES ({self.last_id_sub}, '{row[1]}');")
                self.cursor.execute("SELECT id FROM timetable ORDER BY id DESC LIMIT 1;")
                self.last_id_tb = self.cursor.fetchall()[0][0] + 1
                self.cursor.execute("SELECT id FROM teachers ORDER BY id DESC LIMIT 1;")
                self.last_id_teach = self.cursor.fetchall()[0][0] + 1
                self.cursor.execute(f"INSERT INTO teachers (id, full_name, fk_subject) VALUES ({self.last_id_teach}, '{row[2]}', {self.last_id_sub});")
                self.cursor.execute(f"INSERT INTO timetable (id, dof, top_week, room, start_time, fk_subject)\
                                        VALUES ({self.last_id_tb}, {self.dof}, {self.top_week}, '{row[3]}', '{row[0]}', {self.last_id_sub})")
                self.conn.commit()
                print(f"INSERT sucssed")
            except:
                pass


app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())