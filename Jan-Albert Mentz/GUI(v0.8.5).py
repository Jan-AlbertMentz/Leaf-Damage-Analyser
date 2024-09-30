import sys
from PyQt5.QtWidgets import (
    QApplication, QLabel, QPushButton, QWidget, QMessageBox, 
    QFileDialog, QListWidget, QVBoxLayout, QLineEdit,
    QDateEdit, QListWidgetItem, QStackedWidget, QTableWidget,
    QTableWidgetItem, QScrollArea, QHeaderView)
from PyQt5.QtGui import QFont, QPixmap, QPalette, QBrush, QIcon
from PyQt5.QtCore import Qt, QDate, QSize

import psycopg2
from psycopg2 import sql


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("BCASAA")
        self.setGeometry(100, 100, 1300, 780)
        self.stacked_widget = QStackedWidget(self)

        #CREATE PAGES
        self.main_page = MainPage(self)
        self.new_sample_page = NewSamplePage(self)
        self.data_review_page = DataReviewPage(self)
        self.output_page = OutputPage(self)

        #ADD TO STACK
        self.stacked_widget.addWidget(self.main_page)
        self.stacked_widget.addWidget(self.new_sample_page)
        self.stacked_widget.addWidget(self.data_review_page)
        self.stacked_widget.addWidget(self.output_page)

        # Set layout to hold the stacked widget
        layout = QVBoxLayout(self)
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

        #BUTTONS FOR NAVIGATION        
        self.main_page.new_sample_button.clicked.connect(self.show_new_sample_page)
        self.main_page.data_review_button.clicked.connect(self.show_data_review_page)
        self.new_sample_page.home_button.clicked.connect(self.show_main_page)
        self.new_sample_page.next_button.clicked.connect(self.show_output_page)
        self.data_review_page.home_button.clicked.connect(self.show_main_page)
        self.data_review_page.next_button.clicked.connect(self.show_output_page)
        self.output_page.home_button.clicked.connect(self.show_main_page)

    def show_main_page(self):
        self.stacked_widget.setCurrentWidget(self.main_page)

    def show_new_sample_page(self):
        self.stacked_widget.setCurrentWidget(self.new_sample_page)
        
    def show_data_review_page(self):
        self.stacked_widget.setCurrentWidget(self.data_review_page)
        
    def show_output_page(self):
        self.stacked_widget.setCurrentWidget(self.output_page)
   
#HOME PAGE
class MainPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setGeometry(20, 20, 1280, 720)  #SETS SIZE OF APPLICATION
        self.set_background_image()
        
        #MAIN TITLE
        self.title_label = QLabel(self)
        self.title_label.setText("Welcome to the BioControl Agent\n"+
                                 "Statistical Analysis Application")
        self.title_label.setWordWrap(True)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setGeometry(100, 20, 1080, 300)
        self.title_label.setStyleSheet("""
            QLabel {
                font-family: 'Inter';
                font-style: italic;
                font-weight: 600;
                font-size: 50px;
                line-height: 80px;
                text-align: center;
                color: #000000;
            }
        """)
        
        #NEW SAMPLE BUTTON
        self.new_sample_button = QPushButton('New Sample', self)
        self.new_sample_button.setFont(QFont('Inter', 35))
        self.new_sample_button.setGeometry(250, 350, 300, 100)
        self.new_sample_button.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(spread:pad, x1:0.493, y1:1, x2:0.471, y2:0, stop:0 rgba(217, 217, 217, 255), stop:0.8125 rgba(255, 255, 255, 255));
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                color: #000000;
            }
            QPushButton:hover {
                background-color: #d9d9d9;
            }
        """)

        #DATA REVIEW BUTTON
        self.data_review_button = QPushButton('Data Review', self)
        self.data_review_button.setFont(QFont('Inter', 35))
        self.data_review_button.setGeometry(700, 350, 300, 100)
        self.data_review_button.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(spread:pad, x1:0.493, y1:1, x2:0.471, y2:0, stop:0 rgba(217, 217, 217, 255), stop:0.8125 rgba(255, 255, 255, 255));
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                color: #000000;
            }
            QPushButton:hover {
                background-color: #d9d9d9;
            }
        """)

        #INSTRUCTIONS BUTTON
        self.instructions_button = QPushButton(self)
        self.instructions_button.setGeometry(1210, 20, 50, 50)
        self.instructions_button.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(spread:pad, x1:0.493, y1:1, x2:0.471, y2:0, stop:0 rgba(217, 217, 217, 255), stop:0.8125 rgba(255, 255, 255, 255));
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                padding: 3px;
            }
            QPushButton:hover {
                background-color: #d9d9d9;
            }
        """)
        icon = QIcon("./Images/book_icon.png")
        self.instructions_button.setIcon(icon)
        self.instructions_button.setIconSize(QSize(44,44))
        self.instructions_button.clicked.connect(self.show_instructions)

        #CREDITS SECTION
        self.credit_label = QLabel(self)
        self.credit_label.setText(
            "Credits:\n"
            "Group names D Giovannoni - Project Supervisor\n"
            "Dr. K English - Project Sponsor\n"
            "Belgium ITversity, RSA Center of Biological Control, Rhodes University, US"
        )
        self.credit_label.setFont(QFont('Inter', 20))
        self.credit_label.setAlignment(Qt.AlignCenter)
        self.credit_label.setGeometry(20, 480, 1240, 220)
        self.credit_label.setStyleSheet("""
            QLabel {
                background-color: qlineargradient(spread:pad, x1:0.474459, y1:1, x2:0.476, y2:0, stop:0 rgba(167, 210, 167, 230), stop:0.813312 rgba(255, 255, 255, 200));
                border-radius: 10px;
                border: 2px solid rgba(255, 255, 255, 0.4);
                color: #000000;
                font-family: 'Inter';
                font-style: normal;
                font-weight: 400;
                font-size: 20px;
                line-height: 36px;
                text-align: center;
            }
        """)
        self.credit_label.setWordWrap(True)

    def set_background_image(self):
        palette = QPalette()
        background = QPixmap("./Images/BG.jpg")
        scaled_background = background.scaled(QSize(1280, 720), Qt.KeepAspectRatioByExpanding)
        palette.setBrush(QPalette.Background, QBrush(scaled_background))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

    #CREATES POP-UP WITH INSTRUCTIONS WIP
    def show_instructions(self):
        instructions = (
            "Instructions for Using the Application:\n\n"
            "1. Click 'New Sample' to input new data samples.\n"
            "2. Click 'Data Review' to review existing data and analysis.\n"
            "3. Credits are listed at the bottom for project contributors."
        )
        QMessageBox.information(self, "Instructions", instructions)

#NEW SAMPLE PAGE
class NewSamplePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("BCASAA")
        self.setGeometry(100, 100, 1280, 720)
        self.set_background_image()

        # Samples Image Preview section
        self.sample_label = QLabel(self)
        self.sample_label.setText("Samples:")
        self.sample_label.setAlignment(Qt.AlignLeft)
        self.sample_label.setGeometry(20, 20, 720, 640)
        self.sample_label.setStyleSheet("""
            QLabel {
                background-color: qlineargradient(spread:pad, x1:0.474459, y1:1, x2:0.476, y2:0, stop:0 rgba(167, 210, 167, 230), stop:0.813312 rgba(255, 255, 255, 200));
                border-radius: 10px;                
                border: 2px solid rgba(255, 255, 255, 0.4);
                padding: 10px;
                color: #000000;
                font-family: 'Inter';
                font-style: italic;
                font-weight: 600;
                font-size: 20px;
                line-height: 36px;
            }
        """)
        self.image_preview_area = QListWidget(self)
        self.image_preview_area.setGeometry(40, 60, 680, 580)
        self.image_preview_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.image_preview_area.setStyleSheet("""
            QListWidget {
                background-color: rgb(250, 250, 250);
                border-radius: 10px;
            }
        """)

        #ADD IMAGE BUTTON
        self.add_image_button = QPushButton('Add Images', self)
        self.add_image_button.setFont(QFont('Inter', 20))
        self.add_image_button.setGeometry(20, 680, 720, 60)
        self.add_image_button.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(spread:pad, x1:0.493, y1:1, x2:0.471, y2:0, stop:0 rgba(217, 217, 217, 255), stop:0.8125 rgba(255, 255, 255, 255));
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                color: #000000;
                }                           
        """)
        self.add_image_button.clicked.connect(self.open_image_dialog)

        #DATA INPUT SECTION
        self.dataInput_label = QLabel(self)
        self.dataInput_label.setGeometry(800, 90, 460, 570)
        self.dataInput_label.setAlignment(Qt.AlignLeft)        
        self.dataInput_label.setText("Please input the relevant data below:")
        self.dataInput_label.setStyleSheet("""
            QLabel {
                background-color: qlineargradient(spread:pad, x1:0.474459, y1:1, x2:0.476, y2:0, stop:0 rgba(167, 210, 167, 230), stop:0.813312 rgba(255, 255, 255, 200));
                border-radius: 10px;                
                border: 2px solid rgba(255, 255, 255, 0.4);
                padding: 10px;
                color: #000000;
                font-family: 'Inter';
                font-style: italic;
                font-weight: 400;
                font-size: 20px;
            }
        """)
        
        #LOCATION
        self.location_label = QLabel(self)
        self.location_label.setGeometry(820, 130, 400, 30)
        self.location_label.setText("Location:")
        self.location_label.setStyleSheet("""
            QLabel {
                font-family: 'Inter';
                font-style: none;
                font-weight: 400;
                font-size: 15px;
            }
        """)
        self.location_input = QLineEdit(self)
        self.location_input.setGeometry(820, 160, 400, 40)
        self.location_input.setPlaceholderText("Enter Location") 
        
        #DATE
        self.date_label = QLabel(self)
        self.date_label.setGeometry(820, 210, 400, 30)
        self.date_label.setText("Date:")
        self.date_label.setStyleSheet("""
            QLabel {
                font-family: 'Inter';
                font-style: none;
                font-weight: 400;
                font-size: 15px;
            }
        """)
        self.date_input = QDateEdit(self)
        self.date_input.setGeometry(820, 240, 400, 40)
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())

        #NEXT BUTTON
        self.next_button = QPushButton('Next', self)
        self.next_button.setFont(QFont('Inter', 20))
        self.next_button.setGeometry(800, 680, 460, 60) 
        self.next_button.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(spread:pad, x1:0.493, y1:1, x2:0.471, y2:0, stop:0 rgba(217, 217, 217, 255), stop:0.8125 rgba(255, 255, 255, 255));
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                color: #000000;
                }                           
        """)
        
        #INSTRUCTIONS BUTTON
        self.instructions_button = QPushButton(self)
        self.instructions_button.setGeometry(1210, 20, 50, 50)
        self.instructions_button.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(spread:pad, x1:0.493, y1:1, x2:0.471, y2:0, stop:0 rgba(217, 217, 217, 255), stop:0.8125 rgba(255, 255, 255, 255));
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                padding: 3px;
            }
            QPushButton:hover {
                background-color: #d9d9d9;
            }
        """)
        icon = QIcon("./Images/book_icon.png")
        self.instructions_button.setIcon(icon)
        self.instructions_button.setIconSize(QSize(44, 44))
        self.instructions_button.clicked.connect(self.show_instructions)
        
        #HOME BUTTON
        self.home_button = QPushButton(self)
        self.home_button.setGeometry(1150, 20, 50, 50)
        self.home_button.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(spread:pad, x1:0.493, y1:1, x2:0.471, y2:0, stop:0 rgba(217, 217, 217, 255), stop:0.8125 rgba(255, 255, 255, 255));
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                padding: 3px;
            }
            QPushButton:hover {
                background-color: #d9d9d9;
            }
        """)
        icon = QIcon("./Images/home_icon.png")
        self.home_button.setIcon(icon)
        self.home_button.setIconSize(QSize(44, 44))

    def set_background_image(self):
        palette = QPalette()
        background = QPixmap("./Images/BG.jpg")
        scaled_background = background.scaled(QSize(1280, 720), Qt.KeepAspectRatioByExpanding)
        palette.setBrush(QPalette.Background, QBrush(scaled_background))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

    def open_image_dialog(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("Images (*.png *.jpg)")
        if file_dialog.exec_():
            file_paths = file_dialog.selectedFiles()
            for file_path in file_paths:
                self.add_image_thumbnail(file_path)

    def add_image_thumbnail(self, file_path):
        pixmap = QPixmap(file_path)
        thumbnail = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        item = QListWidgetItem()
        item.setIcon(thumbnail)
        self.image_preview_area.addItem(item)
            
    #CREATES POP-UP WITH INSTRUCTIONS WIP
    def show_instructions(self):
        instructions = (
            "Instructions for New Sample Page:\n\n"
            "1. Use 'Add Images' to upload image files (.png, .jpg).\n"
            "2. Fill out the location and date fields.\n"
            "4. Click 'Next' to proceed to the next step."
        )
        QMessageBox.information(self, "Instructions", instructions)

#DATA REVIEW PAGE
class DataReviewPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("BCASAA")
        self.setGeometry(100, 100, 1280, 720)
        self.set_background_image()

        #DATA SET TABLE
        self.dataSets_label = QLabel(self)
        self.dataSets_label.setText("Data Sets:")
        self.dataSets_label.setAlignment(Qt.AlignLeft)
        self.dataSets_label.setGeometry(20, 100, 1240, 570)
        self.dataSets_label.setStyleSheet("""
            QLabel {
                background-color: qlineargradient(spread:pad, x1:0.474459, y1:1, x2:0.476, y2:0, stop:0 rgba(167, 210, 167, 230), stop:0.813312 rgba(255, 255, 255, 200));
                border-radius: 10px;                
                border: 2px solid rgba(255, 255, 255, 0.4);
                padding: 10px;
                color: #000000;
                font-family: 'Inter';
                font-style: italic;
                font-weight: 600;
                font-size: 20px;
                line-height: 36px;
            }
        """)
        self.dataSets_table = QTableWidget(self)
        self.dataSets_table.setGeometry(40, 140, 1200, 510)
        self.dataSets_table.setColumnCount(3)
        header = self.dataSets_table.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.dataSets_table.setHorizontalHeaderLabels(['Date', 'Location', 'Miscellaneous'])
        self.dataSets_table.setSortingEnabled(True)  #CAN SORT BY COLUMN
        self.load_table_data()

        #SELECT SAMPLE BUTTON
        self.selectSample_button = QPushButton('Select Sample', self)
        self.selectSample_button.setFont(QFont('Inter', 20))
        self.selectSample_button.setGeometry(20, 680, 720, 60)
        self.selectSample_button.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(spread:pad, x1:0.493, y1:1, x2:0.471, y2:0, stop:0 rgba(217, 217, 217, 255), stop:0.8125 rgba(255, 255, 255, 255));
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                color: #000000;
            }
        """)
        self.selectSample_button.clicked.connect(self.fetch_selected_sample)
        
        #NEXT BUTTON
        self.next_button = QPushButton('Next', self)
        self.next_button.setFont(QFont('Inter', 20))
        self.next_button.setGeometry(800, 680, 460, 60) 
        self.next_button.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(spread:pad, x1:0.493, y1:1, x2:0.471, y2:0, stop:0 rgba(217, 217, 217, 255), stop:0.8125 rgba(255, 255, 255, 255));
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                color: #000000;
                }                           
        """)
        
        #INSTRUCTIONS BUTTON
        self.instructions_button = QPushButton(self)
        self.instructions_button.setGeometry(1210, 20, 50, 50)
        self.instructions_button.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(spread:pad, x1:0.493, y1:1, x2:0.471, y2:0, stop:0 rgba(217, 217, 217, 255), stop:0.8125 rgba(255, 255, 255, 255));
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                padding: 3px;
            }
            QPushButton:hover {
                background-color: #d9d9d9;
            }
        """)
        icon = QIcon("./Images/book_icon.png")
        self.instructions_button.setIcon(icon)
        self.instructions_button.setIconSize(QSize(44, 44))
        self.instructions_button.clicked.connect(self.show_instructions)
        
        #HOME BUTTON
        self.home_button = QPushButton(self)
        self.home_button.setGeometry(1150, 20, 50, 50)
        self.home_button.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(spread:pad, x1:0.493, y1:1, x2:0.471, y2:0, stop:0 rgba(217, 217, 217, 255), stop:0.8125 rgba(255, 255, 255, 255));
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                padding: 3px;
            }
            QPushButton:hover {
                background-color: #d9d9d9;
            }
        """)
        icon = QIcon("./Images/home_icon.png")
        self.home_button.setIcon(icon)
        self.home_button.setIconSize(QSize(44, 44))

    def set_background_image(self):
        palette = QPalette()
        background = QPixmap("./Images/BG.jpg")
        scaled_background = background.scaled(QSize(1280, 720), Qt.KeepAspectRatioByExpanding)
        palette.setBrush(QPalette.Background, QBrush(scaled_background))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

    # Function to connect to the PostgreSQL database
    def connect_to_db(self):
        try:
            # Connect to PostgreSQL database
            conn = psycopg2.connect(
                host="localhost",  # DB HOST NAME
                database="Year Project",  # DB NAME
                user="postgres",  # DB USER
                password="1234"  # DB PASSWORD
            )
            return conn
        except psycopg2.Error as e:
            QMessageBox.critical(self, "Database Error", f"Error connecting to the database: {e}")
            print(f"Database error: {e}")
            return None

    def write_blob(self, image_id, ld_id, back_image_path, front_image_path):
        try:
            # Read the back and front image files
            image_back = open(back_image_path, 'rb').read()
            image_front = open(front_image_path, 'rb').read()

            # Connect to the database
            conn = self.connect_to_db()  # Assuming create_connection() is defined elsewhere to return the connection and cursor
            cursor = conn.cursor
            try:
                # Insert the data into the Images table
                cursor.execute("""
                    INSERT INTO Images (Image_ID, LD_ID, Image_Path_Back, Image_Path_Front) 
                    VALUES (%s, %s, %s, %s)
                    """,
                               (image_id, ld_id, psycopg2.Binary(image_back), psycopg2.Binary(image_front))
                               )

                # Commit the transaction
                conn.commit()
                print("Images inserted successfully.")

            except (Exception, psycopg2.DatabaseError) as error:
                print("Error while inserting data into Images table:", error)

            finally:
                # Close the cursor and connection
                cursor.close()
                conn.close()

        except Exception as error:
            print(f"Error reading image files: {error}")

    # Example of how to use this function
    # Create an instance of the DataReviewPage class
    def add_image(self):
        # Call the write_blob method within the class
        self.write_blob(1, 1, 'ImagesForDatabase/ImageData.png', 'ImagesForDatabase/data1.png')

    # Loads all samples from the DB for the table
    def load_table_data(self):
        try:
            # Connect to the DB
            conn = self.connect_to_db()
            if conn is None:
                return

            cursor = conn.cursor()

            # Fetch data
            cursor.execute('SELECT "LD_ID", "Location", "Date" FROM "Location_Date"')

            rows = cursor.fetchall()

            # Populate table
            self.dataSets_table.setRowCount(len(rows))
            for row_idx, row_data in enumerate(rows):
                for col_idx, data in enumerate(row_data):
                    item = QTableWidgetItem(str(data))
                    self.dataSets_table.setItem(row_idx, col_idx, item)

            conn.close()

        except psycopg2.Error as e:
            QMessageBox.critical(self, "Database Error", f"Error fetching data: {e}")
            print(f"Database error: {e}")

    # Selects specific data set from the DB
    def fetch_selected_sample(self):
        selected_row = self.dataSets_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Selection Error", "Please select a data set from the table.")
            return

        # Get selected values from the table
        LD_ID = self.dataSets_table.item(selected_row, 0).text()
        print(f"LD_ID: {LD_ID}")
        LD_ID = int(LD_ID)  # This converts the value to integer if required
        self.add_image()
        try:
            # Connect to the DB
            conn = self.connect_to_db()
            if conn is None:
                return

            cursor = conn.cursor()

            # Query to fetch the specific dataset
            query = sql.SQL('SELECT * FROM "Images" WHERE "LD_ID" = %s')
            cursor.execute(query, (LD_ID))

            # Placeholder code to test
            result = cursor.fetchone()
            if result:
                QMessageBox.information(self, "Sample Selected", f"Data: {result}")
            else:
                QMessageBox.warning(self, "No Data", "No matching data found in the database.")

            conn.close()

        except psycopg2.Error as e:
            QMessageBox.critical(self, "Database Error", f"Error fetching data from the database: {e}")
            print(f"Database error: {e}")

    #CREATES POP-UP WITH INSTRUCTIONS WIP
    def show_instructions(self):
        instructions = (
            "Instructions for New Sample Page:\n\n"
            "1. Use 'Add Images' to upload image files (.png, .jpg).\n"
            "2. Fill out the location and date fields.\n"
            "4. Click 'Next' to proceed to the next step."
        )
        QMessageBox.information(self, "Instructions", instructions)

#OUTPUT PAGE
class OutputPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("BCASAA")
        self.setGeometry(100, 100, 1280, 720)
        self.set_background_image()

        #STARTS IMAGE ARRAY
        self.images = []  #IMAGES STORED AS STRINGS/FILE PATHS
        
        # Samples Image Preview section
        self.sample_label = QLabel(self)
        self.sample_label.setText("Samples:")
        self.sample_label.setAlignment(Qt.AlignLeft)
        self.sample_label.setGeometry(20, 20, 500, 640)
        self.sample_label.setStyleSheet("""
            QLabel {
                background-color: qlineargradient(spread:pad, x1:0.474459, y1:1, x2:0.476, y2:0, stop:0 rgba(167, 210, 167, 230), stop:0.813312 rgba(255, 255, 255, 200));
                border-radius: 10px;                
                border: 2px solid rgba(255, 255, 255, 0.4);
                padding: 10px;
                color: #000000;
                font-family: 'Inter';
                font-style: italic;
                font-weight: 600;
                font-size: 20px;
                line-height: 36px;
            }
        """)
        self.image_preview_area = QListWidget(self)
        self.image_preview_area.setGeometry(40, 60, 460, 580)
        self.image_preview_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.image_preview_area.setSelectionMode(QListWidget.MultiSelection)
        self.image_preview_area.setStyleSheet("""
            QListWidget {
                background-color: rgb(250, 250, 250);
                border-radius: 10px;
            }
        """)
        self.refresh_image_preview()
        
        #REMOVE SELECTED BUTTON
        self.remove_image_button = QPushButton('Remove Selected', self)
        self.remove_image_button.setFont(QFont('Inter', 20))
        self.remove_image_button.setGeometry(20, 680, 500, 60)
        self.remove_image_button.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(spread:pad, x1:0.493, y1:1, x2:0.471, y2:0, stop:0 rgba(217, 217, 217, 255), stop:0.8125 rgba(255, 255, 255, 255));
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                color: #000000;
            }
            QPushButton:hover {
                background-color: #d9d9d9;
            }
        """)
        self.remove_image_button.clicked.connect(self.remove_selected_images)
        
        
        
        #INDIVIDUAL IMAGE RESULTS AREA
        self.imageResults_label = QLabel(self)
        self.imageResults_label.setText("Individual Results:")
        self.imageResults_label.setAlignment(Qt.AlignLeft)
        self.imageResults_label.setGeometry(540, 80, 350, 580)
        self.imageResults_label.setStyleSheet("""
            QLabel {
                background-color: qlineargradient(spread:pad, x1:0.474459, y1:1, x2:0.476, y2:0, stop:0 rgba(167, 210, 167, 230), stop:0.813312 rgba(255, 255, 255, 200));
                border-radius: 10px;                
                border: 2px solid rgba(255, 255, 255, 0.4);
                padding: 10px;
                color: #000000;
                font-family: 'Inter';
                font-style: italic;
                font-weight: 600;
                font-size: 20px;
                line-height: 36px;
            }
        """)
        self.imageResults_area = QScrollArea(self)
        self.imageResults_area.setGeometry(550, 120, 330, 530)
        self.imageResults_area.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
        """)
        
        #AVERAGE RESULTS AREA
        self.avgResults_label = QLabel(self)
        self.avgResults_label.setText("Averaged Results:")
        self.avgResults_label.setAlignment(Qt.AlignLeft)
        self.avgResults_label.setGeometry(910, 80, 350, 580)
        self.avgResults_label.setStyleSheet("""
            QLabel {
                background-color: qlineargradient(spread:pad, x1:0.474459, y1:1, x2:0.476, y2:0, stop:0 rgba(167, 210, 167, 230), stop:0.813312 rgba(255, 255, 255, 200));
                border-radius: 10px;                
                border: 2px solid rgba(255, 255, 255, 0.4);
                padding: 10px;
                color: #000000;
                font-family: 'Inter';
                font-style: italic;
                font-weight: 600;
                font-size: 20px;
                line-height: 36px;
            }
        """)
        self.avg_results_area = QScrollArea(self)
        self.avg_results_area.setGeometry(920, 120, 330, 530)
        self.avg_results_area.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
        """)
        
        #SAVE DATA BUTTON
        self.save_button = QPushButton("Save Data", self)
        self.save_button.setFont(QFont('Inter', 20))
        self.save_button.setGeometry(910, 680, 350, 60)
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(spread:pad, x1:0.493, y1:1, x2:0.471, y2:0, stop:0 rgba(217, 217, 217, 255), stop:0.8125 rgba(255, 255, 255, 255));
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                color: #000000;
            }
            QPushButton:hover {
                background-color: #d9d9d9;
            }
        """)
        #self.save_button.clicked.connect(self.save_data_to_db)
        
        
        
        
        
        #INSTRUCTIONS BUTTON
        self.instructions_button = QPushButton(self)
        self.instructions_button.setGeometry(1210, 20, 50, 50)
        self.instructions_button.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(spread:pad, x1:0.493, y1:1, x2:0.471, y2:0, stop:0 rgba(217, 217, 217, 255), stop:0.8125 rgba(255, 255, 255, 255));
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                padding: 3px;
            }
            QPushButton:hover {
                background-color: #d9d9d9;
            }
        """)
        icon = QIcon("./Images/book_icon.png")
        self.instructions_button.setIcon(icon)
        self.instructions_button.setIconSize(QSize(44, 44))
        self.instructions_button.clicked.connect(self.show_instructions)
        
        #HOME BUTTON
        self.home_button = QPushButton(self)
        self.home_button.setGeometry(1150, 20, 50, 50)
        self.home_button.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(spread:pad, x1:0.493, y1:1, x2:0.471, y2:0, stop:0 rgba(217, 217, 217, 255), stop:0.8125 rgba(255, 255, 255, 255));
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                padding: 3px;
            }
            QPushButton:hover {
                background-color: #d9d9d9;
            }
        """)
        icon = QIcon("./Images/home_icon.png")
        self.home_button.setIcon(icon)
        self.home_button.setIconSize(QSize(44, 44))
    
    #REFRESHES IMAGE PREVIEW AREA    
    def refresh_image_preview(self):
        self.image_preview_area.clear()  # Clear the QListWidget
        for image in self.images:
            item = QListWidgetItem(image)
            self.image_preview_area.addItem(item)

    #PROMPTS USER FOR CONFIRMATION
    def remove_selected_images(self):
        selected_items = self.image_preview_area.selectedItems()        
        if not selected_items:
            return #NO IMAGES SELECTED

        #CONFIRMATION DIALOG BOX
        confirmation = QMessageBox.question(self, 'Confirmation', 
                                            "Are you sure you want to delete the selected images?",
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if confirmation == QMessageBox.Yes:
            for item in selected_items:
                image_name = item.text()
                if image_name in self.images:
                    self.images.remove(image_name)
            self.refresh_image_preview()
            
            
    """        
    def display_avg_results(self):
        stats = get_stats()
        layout = QGridLayout()
        row = 0

        for key, value in stats.items():
            label_key = QLabel(f"{key}:")
            label_value = QLabel(f"{value}")
            layout.addWidget(label_key, row, 0)
            layout.addWidget(label_value, row, 1)
            row += 1

        content_widget = QWidget()
        content_widget.setLayout(layout)
        self.avg_results_area.setWidget(content_widget)

    def display_individual_results(self, selected_images):
        layout = QVBoxLayout()
        for image in selected_images:
            results = get_image_results(image)
            for key, value in results.items():
                result_label = QLabel(f"{key}: {value}")
                layout.addWidget(result_label)

        content_widget = QWidget()
        content_widget.setLayout(layout)
        self.individual_results_area.setWidget(content_widget)

    def save_data_to_db(self):
        connection = psycopg2.connect(
            dbname="your_db", user="your_user", password="your_password", host="localhost"
        )
        cursor = connection.cursor()
        
        for image in self.images:
            results = get_image_results(image)
            for key, value in results.items():
                cursor.execute(
                    "INSERT INTO image_results (image_name, result_key, result_value) VALUES (%s, %s, %s)",
                    (image, key, value)
                )
        
        connection.commit()
        cursor.close()
        connection.close()"""
    
    
    
    def set_background_image(self):
        palette = QPalette()
        background = QPixmap("./Images/BG.jpg")
        scaled_background = background.scaled(QSize(1280, 720), Qt.KeepAspectRatioByExpanding)
        palette.setBrush(QPalette.Background, QBrush(scaled_background))
        self.setAutoFillBackground(True)
        self.setPalette(palette)    
        
    #CREATES POP-UP WITH INSTRUCTIONS WIP
    def show_instructions(self):
        instructions = (
            "Instructions for New Sample Page:\n\n"
            "1. Use 'Add Images' to upload image files (.png, .jpg).\n"
            "2. Fill out the location and date fields.\n"
            "4. Click 'Next' to proceed to the next step."
        )
        QMessageBox.information(self, "Instructions", instructions)
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())