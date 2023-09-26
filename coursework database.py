from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem, QDialog, QDialogButtonBox, QFormLayout
import pyodbc

#создаём подключение к нашей БД
connection = pyodbc.connect(
                      'Driver={SQL Server};'
                      'Server=LAPTOP-NQN12GMG\SQLEXPRESS;'
                      'Database=Uni;'
                      'Trusted_Connection=yes;')
#класс для формы добавления информации в таблицу
class AddRowDialog(QDialog):
    def __init__(self, table_name, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Добавить строку в {table_name}")
        self.layout = QVBoxLayout(self)

        self.form_layout = QFormLayout()
        self.layout.addLayout(self.form_layout)

        self.table_name = table_name
        self.input_fields = []

        self.setup_ui()

    def setup_ui(self):
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {self.table_name}")
        columns = cursor.description
        #формируем поля для ввода на основании таблицы, в которую нужно добавить запись
        for column in cursor.description:
            if(column is not cursor.description[0]):
                column_name = column[0]
                label = QLabel(column_name)
                line_edit = QLineEdit()
                self.input_fields.append(line_edit)
                self.form_layout.addRow(label, line_edit)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        self.layout.addWidget(button_box)
    #функция записи информации из полей ввода, формируется список значений
    def get_input_data(self):
        data = []
        for line_edit in self.input_fields:
            data.append(line_edit.text())
        return data
#класс для обновления информации в таблице
class UpdateDialog(QDialog):
    def __init__(self, table_name, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Обновить данные")
        self.layout = QVBoxLayout(self)

        self.form_layout = QFormLayout()
        self.layout.addLayout(self.form_layout)

        self.table_name = table_name
        self.input_fields = []
        self.labels = []
        self.label_input = {}
        self.setup_ui()

    def setup_ui(self):
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {self.table_name}")
        columns = cursor.description

        id_label = QLabel("ID записи для обновления")
        id_line_edit = QLineEdit()
        self.input_fields.append(id_line_edit)
        self.labels.append(id_label)
        self.label_input.update({"ID": id_line_edit})
        self.form_layout.addRow(id_label, id_line_edit)
        #формируем поля для ввода на основании таблицы, в которую нужно внести запись
        for column in cursor.description:
            if(column is not cursor.description[0]):
                column_name = column[0]
                label = QLabel(column_name)
                line_edit = QLineEdit()
                self.input_fields.append(line_edit)
                self.labels.append(label)
                self.label_input.update({column_name: line_edit})
                self.form_layout.addRow(label, line_edit)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        self.layout.addWidget(button_box)
    #собираем информацию из полей, в ней вызываем update, которая совершит запрос на обновление
    def generate_query_for_update(self):
        data = {}
        for column, value in self.label_input.items():
            if(value.text() != ''):
                data.update({f"{column}": f"{value.text()}"})
        return data

#главный класс с главным меню
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Uni")
        self.setGeometry(100, 100, 1200, 700)
        self.setup_ui()
    
    def setup_ui(self):
        #создаются элементы, нужные для правильного отображения других элементов интерфейса
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)


        self.toolbar_layout = QVBoxLayout()
        self.layout.addLayout(self.toolbar_layout)
        
        self.toolbar_row_1 = QHBoxLayout()
        self.toolbar_row_2 = QHBoxLayout()
        self.toolbar_row_3 = QHBoxLayout()
        self.toolbar_row_4 = QHBoxLayout()
        self.toolbar_layout.addLayout(self.toolbar_row_1)
        self.toolbar_layout.addLayout(self.toolbar_row_2)
        self.toolbar_layout.addLayout(self.toolbar_row_3)
        self.toolbar_layout.addLayout(self.toolbar_row_4)
        #создаётся таблица (но сразу не отображается)
        self.table_widget = QTableWidget()
        self.layout.addWidget(self.table_widget)
        #кнопки для вывода информации из таблиц
        self.create_button("Teachers", "TEACHERS", self.toolbar_row_1)
        self.create_button("Teacher's Load", "TEACHERS_LOAD", self.toolbar_row_1)
        self.create_button("Potoks", "GROUPS_POTOKS", self.toolbar_row_1)
        self.create_button("Kafedra Load", "KAFEDRA_LOAD", self.toolbar_row_1)
        self.create_button("Load Type", "LOAD_TYPES", self.toolbar_row_1)
        #кнопки для добавления информации
        self.create_button_for_add("Добавить новую запись", "TEACHERS", self.toolbar_row_2)
        self.create_button_for_add("Добавить новую запись", "TEACHERS_LOAD", self.toolbar_row_2)
        self.create_button_for_add("Добавить новую запись", "GROUPS_POTOKS", self.toolbar_row_2)
        self.create_button_for_add("Добавить новую запись", "KAFEDRA_LOAD", self.toolbar_row_2)
        self.create_button_for_add("Добавить новую запись", "LOAD_TYPES", self.toolbar_row_2)

        self.create_button_for_update("Обновить запись", "TEACHERS", self.toolbar_row_3)
        self.create_button_for_update("Обновить запись", "TEACHERS_LOAD", self.toolbar_row_3)
        self.create_button_for_update("Обновить запись", "GROUPS_POTOKS", self.toolbar_row_3)
        self.create_button_for_update("Обновить запись", "KAFEDRA_LOAD", self.toolbar_row_3)
        self.create_button_for_update("Обновить запись", "LOAD_TYPES", self.toolbar_row_3)
        #кнопки для вывода запросов
        button_q1=QPushButton("Нагрузка кафедры отсутсвующая у преподавателей")
        button_q1.clicked.connect(lambda checked: self.query1())
        self.toolbar_row_4.addWidget(button_q1)

        button_q2 = QPushButton("Количество часов каждого типа нагрузки у преподавателей")
        button_q2.clicked.connect(lambda checked: self.query2())
        self.toolbar_row_4.addWidget(button_q2)
        
    #функции для облегчения создания кнопок, здесь мы назначаем для них обработчики и добавляем на экран
    def create_button(self, text, table_name, layout, slot=None):
        button = QPushButton(text)
        if slot:
            button.clicked.connect(slot)
        else:
            button.clicked.connect(lambda checked, name=table_name: self.show_table_data(name))
        layout.addWidget(button)
    
    def create_button_for_add(self, text, table_name, layout, slot=None):
        button = QPushButton(text)
        if slot:
            button.clicked.connect(slot)
        else:
            button.clicked.connect(lambda checked, name=table_name: self.open_add_row_dialog(name))
        layout.addWidget(button)

    def create_button_for_update(self, text, table_name, layout, slot=None):
        button = QPushButton(text)
        if slot:
            button.clicked.connect(slot)
        else:
            button.clicked.connect(lambda checked, name=table_name: self.open_update_row_dialog(name))
        layout.addWidget(button)


    #функции для вывода запросов
    def query1(self):
        self.table_widget.clear()
        self.table_widget.setColumnCount(0)
        self.table_widget.setRowCount(0)

        cursor = connection.cursor()
        cursor.execute(f"SELECT D.ID, D.Load_Type, D.Potok, D.Semester, D.Year, D.Hours FROM Kafedra_Load D LEFT JOIN Teachers_Load T ON D.Load_Type = T.Load_Type AND D.Potok = T.Potok AND D.Semester = T.Semester AND D.Year = T.Year WHERE T.ID IS NULL OR D.Hours > T.Hours; ")
        result = cursor.fetchall()

        column_list = [description[0] for description in cursor.description]
        self.table_widget.setRowCount(len(result))
        self.table_widget.setColumnCount(len(result[0]))
        self.table_widget.setHorizontalHeaderLabels(column_list)
        self.table_widget.setVerticalHeaderLabels(['' for i in range(len(result))])
        for row in range(len(result)):
            for column in range(len(result[0])):
                item = QTableWidgetItem(str(result[row][column]))
                self.table_widget.setItem(row, column, item)
    
    def query2(self):
        self.table_widget.clear()
        self.table_widget.setColumnCount(0)
        self.table_widget.setRowCount(0)


        cursor = connection.cursor()
        cursor.execute(f"SELECT Teachers.Name, Load_Types.Name AS Load_Type, SUM(Teachers_Load.Hours) AS Total_Hours FROM Teachers INNER JOIN Teachers_Load ON Teachers.ID = Teachers_Load.Teacher INNER JOIN Load_Types ON Teachers_Load.Load_Type = Load_Types.ID GROUP BY Teachers.Name, Load_Types.Name;")
        result = cursor.fetchall()

        column_list = [description[0] for description in cursor.description]
        self.table_widget.setRowCount(len(result))
        self.table_widget.setColumnCount(len(result[0]))
        self.table_widget.setHorizontalHeaderLabels(column_list)
        self.table_widget.setVerticalHeaderLabels(['' for i in range(len(result))])
        for row in range(len(result)):
            for column in range(len(result[0])):
                item = QTableWidgetItem(str(result[row][column]))
                self.table_widget.setItem(row, column, item)
    #функция для вывода информации из таблицы
    def show_table_data(self, name):
        self.table_widget.clear()
        self.table_widget.setColumnCount(0)
        self.table_widget.setRowCount(0)
        #делаем запрос на извлечение информации из таблицы
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {name}")
        result = cursor.fetchall()
        #формируем на оснвое таблицы из БД таблицу в интерфейсе
        column_list = [description[0] for description in cursor.description]
        self.table_widget.setRowCount(len(result))
        self.table_widget.setColumnCount(len(result[0]))
        self.table_widget.setHorizontalHeaderLabels(column_list)
        self.table_widget.setVerticalHeaderLabels(['' for i in range(len(result))])
        #заполняем таблицу в интерфейсе информацией из запроса к таблице
        for row in range(len(result)):
            for column in range(len(result[0])):
                item = QTableWidgetItem(str(result[row][column]))
                self.table_widget.setItem(row, column, item)
    #открытие формы для добавления информации
    def open_add_row_dialog(self, table_name):
        dialog = AddRowDialog(table_name, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_input_data()
            self.insert_data(table_name, data)
    #открытие формы для обновления информации
    def open_update_row_dialog(self, table_name):
        dialog = UpdateDialog(table_name, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.generate_query_for_update()
            self.update_data(table_name, id_of_record, data)
    #запрос для вставки информации в таблицу
    def insert_data(self, table_name, data):
        cursor = connection.cursor()
        #делаем запрос на получение названия колонок в таблице для того чтобы подставить их в запрос на добавление информации
        cursor.execute(f"SELECT * FROM {table_name}")
        columns = [description[0] for description in cursor.description if(description is not cursor.description[0])]
        #создаём запрос, в который подставляем название таблицы, названия колонок и значения 
        insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['?'] * len(data))})"
        #выполняем запрос, подставляя нашу строку. На места ? подставятся значения из кортежа tuple(data)
        cursor.execute(insert_query, tuple(data))

        connection.commit()
        
        QMessageBox.information(self, "Успех", "Данные добавлены в таблицу.")
    #запрос на обновление информации в таблице
    def update_data(self, table_name, id, data):
        #создаём заготовку для запроса
        query = f"UPDATE {table_name} SET "
        values = []
        #получаем id записи, которую нужно обновить 
        id = data.get("ID")
        id = int(id.replace("'", ""))
        #добавляем в запрос таблицы, которые хочет изменить пользователь
        for column_name, value in data.items():
            if column_name != "ID":
                query += f"{column_name} = ?, "
                values.append(value)
        query = query.rstrip(", ")
        values.append(id)
        #добавляем условие
        query += f" WHERE ID = ?"
        

        cursor = connection.cursor()
        #на места знаков вопросов в строке с запросом подставятся значения values
        cursor.execute(query, values)
        QMessageBox.information(self, "Успех", "Данные обновлены в таблицу.")

class InputWindow(MainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 400, 300)
        self.setup_ui()
    def setup_ui(self):
        return 0
    def input_data(self, table_name):
        self.show()
        
app = QApplication([])
main_window = MainWindow()
input_window = InputWindow()
main_window.show()
app.exec()