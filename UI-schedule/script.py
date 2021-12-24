
from datetime import datetime, date, time
from PyQt5.QtCore import qInfo
import psycopg2
import sys


conn = psycopg2.connect(database="schedule",
                                user="postgres",
                                password="sql_GH0_Fr1",
                                host="localhost",
                                port="5432")

cursor = conn.cursor()

# dof = int(input("Choice day of week (where 1 - Monday, 6 - Saturday)\n"))

start = date(2021, 9, 1) # Start date
d = datetime.now() # Today
week = d.isocalendar()[1] - start.isocalendar()[1] + 1 # Counting number of week now
if week%2 == 1:
    top_week = True
else:
    top_week = False   
#   timetable.start_time, teachers.full_name, teachers.fk_subject, timetable.id, timetable.room
cursor.execute(f"SELECT * FROM timetable\
                ORDER BY id;")
                # INNER JOIN timetable ON subject.id = timetable.fk_subject\
                # INNER JOIN teachers ON subject.id = teachers.fk_subject\
#                 WHERE dof = {dof} and top_week = {top_week}\
                
records = list(cursor.fetchall())
print(len(records))
# print(records[0][0], records[0][1])
for i in range(29):
    print(f"INSERT INTO timetable (id, dof, top_week, room, start_time, fk_subject) VALUES ({i+1}, {records[i][1]}, {records[i][2]}, \
'{records[i][3]}', '{records[i][4]}', {records[i][5]});" )
