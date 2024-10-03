import sys
import sqlite3
from datetime import datetime, timedelta
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLineEdit, QLabel, QComboBox, QTableWidget, 
                             QTableWidgetItem, QMessageBox, QTabWidget, QSizePolicy, QHeaderView,
                             QCheckBox)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QIcon, QColor, QPalette, QDoubleValidator
import openpyxl

class FinanceTrackerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Finance Tracker")
        self.setGeometry(100, 100, 900, 600)
        
        # Set application icon (.ico file)
        self.setWindowIcon(QIcon('icon.ico'))  # Make sure to have this icon file in your project directory
        
        # Set color scheme
        self.set_color_scheme()
        
        self.init_db()
        self.init_ui()

    def set_color_scheme(self):
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(0, 0, 0))
        palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(245, 245, 245))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 220))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(0, 0, 0))
        palette.setColor(QPalette.ColorRole.Text, QColor(0, 0, 0))
        palette.setColor(QPalette.ColorRole.Button, QColor(240, 240, 240))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(0, 0, 0))
        palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
        palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
        self.setPalette(palette)

    def init_db(self):
        self.conn = sqlite3.connect('finance_tracker.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS records (
                                id INTEGER PRIMARY KEY,
                                type TEXT,
                                amount REAL,
                                description TEXT,
                                date TEXT
                              )''')
        self.conn.commit()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Create tabs
        tabs = QTabWidget()
        tabs.setFont(QFont("Arial", 10))
        main_layout.addWidget(tabs)

        # Add Record Tab
        add_record_tab = QWidget()
        tabs.addTab(add_record_tab, "📝 Add Record")
        self.setup_add_record_tab(add_record_tab)

        # View Records Tab
        view_records_tab = QWidget()
        tabs.addTab(view_records_tab, "👁️ View Records")
        self.setup_view_records_tab(view_records_tab)

        # Generate Report Tab
        generate_report_tab = QWidget()
        tabs.addTab(generate_report_tab, "📊 Generate Report")
        self.setup_generate_report_tab(generate_report_tab)

    def setup_add_record_tab(self, tab):
        layout = QVBoxLayout()
        tab.setLayout(layout)

        self.record_type = QComboBox()
        self.record_type.addItems(["Expense", "Income"])
        self.record_type.setFont(QFont("Arial", 10))
        self.record_type.setFixedHeight(30)
        self.record_type.setStyleSheet("background-color: #E0E0E0; color: black;")
        layout.addWidget(QLabel("💼 Record Type:"))
        layout.addWidget(self.record_type)

        self.amount_input = QLineEdit()
        self.amount_input.setFont(QFont("Arial", 10))
        self.amount_input.setFixedHeight(30)
        self.amount_input.setStyleSheet("background-color: #E0E0E0; color: black;")
        self.amount_input.setValidator(QDoubleValidator(0, 1000000, 2))  # Allow only numeric input
        layout.addWidget(QLabel("💰 Amount:"))
        layout.addWidget(self.amount_input)

        self.description_input = QLineEdit()
        self.description_input.setFont(QFont("Arial", 10))
        self.description_input.setFixedHeight(30)
        self.description_input.setStyleSheet("background-color: #E0E0E0; color: black;")
        layout.addWidget(QLabel("📝 Description:"))
        layout.addWidget(self.description_input)

        add_button = QPushButton("➕ Add Record")
        add_button.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        add_button.setFixedHeight(40)
        add_button.clicked.connect(self.add_record)
        layout.addWidget(add_button)

        layout.addStretch()

    def setup_view_records_tab(self, tab):
        layout = QVBoxLayout()
        tab.setLayout(layout)

        self.records_table = QTableWidget()
        self.records_table.setColumnCount(6)  # Added one more column for checkboxes
        self.records_table.setHorizontalHeaderLabels(["Select", "ID", "Type", "Amount", "Description", "Date"])
        self.records_table.setFont(QFont("Arial", 10))
        self.records_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.records_table.verticalHeader().setVisible(False)
        self.records_table.setEditTriggers(QTableWidget.EditTrigger.DoubleClicked | QTableWidget.EditTrigger.EditKeyPressed)
        layout.addWidget(self.records_table)

        button_layout = QHBoxLayout()
        refresh_button = QPushButton("🔄 Refresh")
        refresh_button.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        refresh_button.setFixedHeight(40)
        refresh_button.clicked.connect(self.refresh_records)
        button_layout.addWidget(refresh_button)

        delete_button = QPushButton("🗑️ Delete Selected")
        delete_button.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        delete_button.setFixedHeight(40)
        delete_button.clicked.connect(self.delete_selected_records)
        button_layout.addWidget(delete_button)

        save_button = QPushButton("💾 Save Changes")
        save_button.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        save_button.setFixedHeight(40)
        save_button.clicked.connect(self.save_changes)
        button_layout.addWidget(save_button)

        layout.addLayout(button_layout)

    def setup_generate_report_tab(self, tab):
        layout = QVBoxLayout()
        tab.setLayout(layout)

        self.period_combo = QComboBox()
        self.period_combo.addItems(["Daily", "Weekly", "Monthly"])
        self.period_combo.setFont(QFont("Arial", 10))
        self.period_combo.setStyleSheet("background-color: #E0E0E0; color: black;")
        self.period_combo.setFixedHeight(30)
        layout.addWidget(QLabel("📅 Report Period:"))
        
        layout.addWidget(self.period_combo)

        generate_button = QPushButton("📊 Generate Report")
        generate_button.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        generate_button.setFixedHeight(40)
        generate_button.clicked.connect(self.generate_report)
        layout.addWidget(generate_button)

        self.report_display = QLabel()
        self.report_display.setFont(QFont("Arial", 10))
        self.report_display.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.report_display.setWordWrap(True)
        layout.addWidget(self.report_display)

        layout.addStretch()

    def add_record(self):
        record_type = self.record_type.currentText().lower()
        try:
            amount = float(self.amount_input.text())
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid amount.")
            return

        description = self.description_input.text()
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.cursor.execute("INSERT INTO records (type, amount, description, date) VALUES (?, ?, ?, ?)",
                            (record_type, amount, description, date))
        self.conn.commit()

        QMessageBox.information(self, "Success", f"{record_type.capitalize()} added successfully!")
        self.amount_input.clear()
        self.description_input.clear()

    def refresh_records(self):
        self.cursor.execute("SELECT * FROM records")
        records = self.cursor.fetchall()

        self.records_table.setRowCount(len(records))
        for row, record in enumerate(records):
            # Add checkbox
            checkbox = QCheckBox()
            self.records_table.setCellWidget(row, 0, checkbox)
            
            for col, value in enumerate(record, start=1):
                item = QTableWidgetItem(str(value))
                if col == 2:  # Type column
                    item.setForeground(QColor(0, 0, 0))  # Set text color to black for both expense and income
                elif col == 3:  # Amount column
                    item = QTableWidgetItem("{:.2f}".format(float(value)))  # Format as currency
                self.records_table.setItem(row, col, item)

    def delete_selected_records(self):
        selected_rows = []
        for row in range(self.records_table.rowCount()):
            if self.records_table.cellWidget(row, 0).isChecked():
                selected_rows.append(row)

        if not selected_rows:
            QMessageBox.warning(self, "No Selection", "Please select records to delete.")
            return

        reply = QMessageBox.question(self, 'Confirm Deletion', 
                                     f"Are you sure you want to delete {len(selected_rows)} record(s)?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            for row in reversed(selected_rows):
                record_id = self.records_table.item(row, 1).text()
                self.cursor.execute("DELETE FROM records WHERE id=?", (record_id,))
            self.conn.commit()

            QMessageBox.information(self, "Success", f"{len(selected_rows)} record(s) deleted successfully!")
            self.refresh_records()

    def save_changes(self):
        changes_made = False
        for row in range(self.records_table.rowCount()):
            record_id = int(self.records_table.item(row, 1).text())
            record_type = self.records_table.item(row, 2).text().lower()
            amount = float(self.records_table.item(row, 3).text())
            description = self.records_table.item(row, 4).text()
            date = self.records_table.item(row, 5).text()

            self.cursor.execute("""
                UPDATE records 
                SET type=?, amount=?, description=?, date=?
                WHERE id=?
            """, (record_type, amount, description, date, record_id))
            
            if self.cursor.rowcount > 0:
                changes_made = True

        if changes_made:
            self.conn.commit()
            QMessageBox.information(self, "Success", "Changes saved successfully!")
        else:
            QMessageBox.information(self, "No Changes", "No changes were made.")

    def generate_report(self):
        period = self.period_combo.currentText().lower()
        today = datetime.now()
        
        if period == 'daily':
            start_date = today.date()
        elif period == 'weekly':
            start_date = (today - timedelta(days=today.weekday())).date()
        elif period == 'monthly':
            start_date = today.replace(day=1).date()

        self.cursor.execute("SELECT * FROM records WHERE date(date) >= ?", (start_date,))
        records = self.cursor.fetchall()

        if records:
            total_expenses = sum([rec[2] for rec in records if rec[1] == 'expense'])
            total_incomes = sum([rec[2] for rec in records if rec[1] == 'income'])
            net_balance = total_incomes - total_expenses

            report = f"<h3>Summary for {period} period:</h3>"
            report += f"<p><b>Total Incomes:</b> ₹{total_incomes:.2f}</p>"
            report += f"<p><b>Total Expenses:</b> ₹{total_expenses:.2f}</p>"
            report += f"<p><b>Net Balance:</b> ₹{net_balance:.2f}</p>"

            self.report_display.setText(report)
            self.export_to_excel(records, period)
        else:
            self.report_display.setText("No records found for the specified period.")

    def export_to_excel(self, records, period):
        file_name = f"finance_report_{period}.xlsx"
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = f"{period.capitalize()} Report"

        headers = ["ID", "Type", "Amount", "Description", "Date"]
        ws.append(headers)

        for record in records:
            ws.append(record)

        wb.save(file_name)
        QMessageBox.information(self, "Report Generated", f"Report saved as {file_name}")

    def closeEvent(self, event):
        self.conn.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    tracker = FinanceTrackerGUI()
    tracker.show()
    sys.exit(app.exec())