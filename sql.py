import sqlite3

connection=sqlite3.connect("student.db")

cursor=connection.cursor()

table_info="""
Create table STUDENT(NAME VARCHAR(25),CLASS VARCHAR(25),
SECTION VARCHAR(25),MARKS INT);
"""

cursor.execute(table_info)

insert_info="""
Insert into STUDENT(NAME,CLASS,SECTION,MARKS) 
values
('John Doe','computer Science','A',85),
('Jane Smith','Artificial Intelligence','B',90),
('Alice Johnson','Data Science','A',95),
('Bob Brown','Data Science','B',80),
('Charlie Davis','Information Technology','A',88),
('David Wilson','Data Science','B',92);
"""
cursor.execute(insert_info)


print("The isnerted records are")
data=cursor.execute('''Select * from STUDENT''')
for row in data:
    print(row)

connection.commit()
connection.close()