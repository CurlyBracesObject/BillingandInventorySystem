# Billing and Inventory System (BIS)

**Tech Stack**: Python | PyQt5 | SQLite | Qt Designer | Pandas

A desktop-based billing and inventory management system featuring role-based authentication, transaction tracking, and Excel report generation for enterprise operations.

## Technology Stack

### Backend Technologies
- **Framework**: Python 3.x with modular architecture
- **Database**: SQLite 3 lightweight relational database
- **Data Processing**: Pandas for Excel export and data manipulation
- **Architecture**: Object-oriented design with separation of concerns

### Frontend Technologies
- **GUI Framework**: PyQt5 with QtCore, QtGui, QtWidgets
- **UI Design**: Qt Designer for visual interface creation
- **Components**: QTableWidget, QStackedWidget, custom dialogs
- **Layout Management**: QVBoxLayout, QHBoxLayout for responsive design

### Design Patterns
- **Page Manager Pattern**: Centralized navigation between interfaces
- **Database Manager Pattern**: Unified database operations
- **Observer Pattern**: Signal-slot mechanism for event handling
- **Factory Pattern**: Dynamic page creation and registration

## System Architecture

### Role-Based Access Control System

**Three-Tier User Authentication:**
```python
def logIN(self):
    username = self.ui.textEdit.toPlainText()
    password = self.ui.textEdit_2.toPlainText()
    
    # Admin authentication (perm = 1, 2)
    for admin_info in Admin_info:
        db_username, db_password, perm = admin_info[1], admin_info[2], admin_info[3]
        if username == db_username and password == db_password:
            if perm == 1:
                config.current_prem = perm
                self.switch_page("admin")  # Full access
                return
            elif perm == 2:
                config.current_prem = perm
                self.switch_page("audit")  # Read-only access
                return
    
    # Customer authentication
    for user_info in User_info:
        if username == C_username and password == C_password:
            config.current_user_id = user_info[1]
            self.switch_page("customer")  # Limited access
            return
```

**Page Management with Dynamic Navigation:**
```python
class PageManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.pages = {}
        self.stacked_widget = QStackedWidget(self)
        self.init_pages()
    
    def register_page(self, name, page_class):
        page = page_class(self.switch_page, self)
        self.pages[name] = page
        self.stacked_widget.addWidget(page)
    
    def switch_page(self, name):
        page = self.pages.get(name)
        if page:
            self.stacked_widget.setCurrentWidget(page)
```

### Database Management with CRUD Operations

**Unified Database Manager:**
```python
class DatabaseManager:
    def __init__(self, tableWidget):
        self.tableWidget = tableWidget
        self.conn = None
        self.cur = None
    
    def loadDataFromDatabase(self, table_name, columns, filters=None):
        query = f"SELECT {', '.join(['id'] + columns)} FROM {table_name}"
        if filters:
            filter_conditions = []
            for key, value in filters.items():
                filter_conditions.append(f"{key} = '{value}'")
            filter_clause = " AND ".join(filter_conditions)
            query += f" WHERE {filter_clause}"
        
        self.cur.execute(query)
        data = self.cur.fetchall()
        
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(len(columns))
        self.tableWidget.setHorizontalHeaderLabels(columns)
        
        for row, record in enumerate(data):
            self.addRow(row, record[1:])
```

**Dynamic Search with Filtering:**
```python
def searchData(self, table_name, search_column, keyword, filters=None):
    query = f"SELECT {', '.join(self.exclude_id_column(table_name))} FROM {table_name} WHERE {search_column} LIKE ?"
    params = ['%' + keyword + '%']
    
    if filters:
        for filter_column, filter_value in filters.items():
            query += f" AND {filter_column} = ?"
            params.append(filter_value)
    
    self.cur.execute(query, params)
    data = self.cur.fetchall()
    
    self.tableWidget.setRowCount(0)
    for row, record in enumerate(data):
        self.addRow(row, record)
```

### Payment Processing System

**Bill Payment with Real-time Updates:**
```python
def process_payment(self, bill_id, amount, bill_dict):
    bill_amount, unpaid = bill_dict[bill_id]
    if amount <= bill_amount:
        new_unpaid = unpaid - amount
        
        # Update bill_info table
        update_query_bill_info = "UPDATE bill_info SET unpaid_bill = ? WHERE bill_id = ?"
        self.customerManager.cur.execute(update_query_bill_info, (new_unpaid, bill_id))
        
        # Update transaction_history_info table
        update_query_transaction_history = "UPDATE transaction_history_info SET transaction_history_bill = ? WHERE transaction_history_id = ?"
        self.customerManager.cur.execute(update_query_transaction_history, (new_unpaid, bill_id))
        
        self.customerManager.conn.commit()
        QMessageBox.information(None, "Payment Processed", f"Payment of {amount} processed. New unpaid: {new_unpaid}")
```

**Interactive Payment Dialog:**
```python
def show_bills_to_pay(self):
    bills = self.customerManager.get_bills_to_pay(config.current_user_id)
    if not bills:
        QMessageBox.warning(self, "No Bill to Pay", "No bill to pay for this customer.")
        return
    
    dialog = QDialog(self)
    dialog.setWindowTitle("Bills to Pay")
    layout = QVBoxLayout()
    
    bill_selector = QComboBox()
    bill_dict = {}
    for bill in bills:
        bill_id, bill_amount, unpaid = bill
        bill_amount = float(bill_amount)
        unpaid = float(unpaid)
        amount_due = bill_amount - unpaid
        bill_desc = f"Bill ID: {bill_id}, Amount Due: {amount_due}, Unpaid: {unpaid}"
        bill_selector.addItem(bill_desc, bill_id)
        bill_dict[bill_id] = (bill_amount, unpaid)
    
    amount_input = QSpinBox()
    amount_input.setMaximum(1000000)
    
    button = QPushButton("Pay")
    button.clicked.connect(lambda: self.process_payment(bill_selector.currentData(), amount_input.value(), bill_dict))
```

## Database Schema

### Core Tables Structure
```sql
-- User management with role-based access
CREATE TABLE users (
    id INTEGER PRIMARY KEY, 
    user TEXT, 
    password TEXT, 
    perm INTEGER  -- 1=Admin, 2=Auditor
);

-- Customer information management
CREATE TABLE user_info (
    id INTEGER PRIMARY KEY, 
    customer_id TEXT, 
    customer_name TEXT, 
    customer_mobile TEXT, 
    customer_email TEXT, 
    customer_username TEXT, 
    customer_password TEXT, 
    customer_address TEXT
);

-- Transaction tracking with comprehensive details
CREATE TABLE transaction_info (
    id INTEGER PRIMARY KEY,
    transaction_id TEXT,
    transaction_customer_id TEXT,
    transaction_amount TEXT,
    transaction_bill TEXT,
    transaction_number TEXT,
    transaction_type TEXT,
    transaction_history TEXT,
    transaction_description TEXT
);

-- Bill management with payment tracking
CREATE TABLE bill_info (
    id INTEGER PRIMARY KEY,
    bill_id TEXT,
    bill_customer_id TEXT,
    bill_number TEXT,
    bill_type TEXT,
    bill_receipt TEXT,
    bill_description TEXT,
    bill_amount TEXT,
    unpaid_bill TEXT
);
```

### Database Operations Manager
```python
class DBmanager:
    def __init__(self):
        self.createDatabase()
    
    def createDatabase(self):
        self.conn = sqlite3.connect('management.db')
        self.cur = self.conn.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS users
                           (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')
        self.conn.commit()
    
    def addUserInfo(self, customer_id, name, password):
        self.cur.execute("INSERT INTO user_info (customer_id, customer_username, customer_password) VALUES (?, ?, ?)", 
                        (customer_id, name, password))
        self.conn.commit()
    
    def loadDataFromAdmin(self):
        self.cur.execute("SELECT * FROM users")
        return self.cur.fetchall()
```

## User Interface Implementation

### Admin Interface with Full CRUD Operations
```python
class adminWindow(QWidget):
    def __init__(self, switch_page, parent=None):
        super(adminWindow, self).__init__(parent)
        self.adminManager = DatabaseManager(self.ui.tableWidget)
        self.bind_main_buttons()
        self.bind_crud_buttons()
    
    def bind_main_buttons(self):
        # Customer Management
        self.ui.pushButton_3.clicked.connect(lambda: 
            self.load_table_data('management.db', 'user_info', 
                               ['customer_id', 'customer_name', 'customer_mobile', 
                                'customer_email', 'customer_username', 'customer_password', 'customer_address']))
        
        # Transaction Management
        self.ui.pushButton_5.clicked.connect(lambda: 
            self.load_table_data('management.db', 'transaction_info', 
                               ['transaction_id', 'transaction_customer_id', 'transaction_amount', 
                                'transaction_bill', 'transaction_number', 'transaction_type', 
                                'transaction_history', 'transaction_description']))
        
        # Bill Management
        self.ui.pushButton.clicked.connect(lambda: 
            self.load_table_data('management.db', 'bill_info', 
                               ['bill_id', 'bill_customer_id', 'bill_number', 'bill_type', 
                                'bill_receipt', 'bill_description', 'bill_amount', 'unpaid_bill']))
```

### Customer Interface with Filtered Data Access
```python
class customerWindow(QWidget):
    def bind_main_buttons(self):
        # Bill viewing with customer-specific filtering
        self.ui.billButton.clicked.connect(lambda: 
            self.update_status_and_load_table(
                'management.db', 'bill_info',
                ['bill_id', 'bill_customer_id', 'bill_type', 'bill_receipt', 
                 'bill_description', 'bill_amount', 'unpaid_bill'],
                {'bill_customer_id': config.current_user_id}, 'bill'))
        
        # Transaction viewing with customer-specific filtering
        self.ui.transactionButton.clicked.connect(lambda: 
            self.update_status_and_load_table(
                'management.db', 'transaction_info',
                ['transaction_id', 'transaction_customer_id', 'transaction_amount', 
                 'transaction_bill', 'transaction_number', 'transaction_type', 
                 'transaction_history', 'transaction_description'],
                {'transaction_customer_id': config.current_user_id}, 'transaction'))
```

## Excel Export Functionality

**Multi-Sheet Excel Report Generation:**
```python
def write_to_excel(self, file_path):
    all_data = self.loadAllData()
    with pd.ExcelWriter(file_path) as writer:
        for table_name, (columns, data) in all_data.items():
            df = pd.DataFrame(data, columns=columns)
            df.to_excel(writer, sheet_name=table_name, index=False)
    QMessageBox.information(None, "Excel Export", f"Data successfully exported to {file_path}")

def loadAllData(self):
    tables = {
        'bill_info': ['bill_id', 'bill_customer_id', 'bill_number', 'bill_type', 
                     'bill_receipt', 'bill_description', 'bill_amount', 'unpaid_bill'],
        'transaction_info': ['transaction_id', 'transaction_customer_id', 'transaction_amount', 
                           'transaction_bill', 'transaction_number', 'transaction_type', 
                           'transaction_history', 'transaction_description'],
        'user_info': ['customer_id', 'customer_name', 'customer_mobile', 'customer_email', 
                     'customer_username', 'customer_password', 'customer_address']
    }
    
    all_data = {}
    for table, columns in tables.items():
        query = f"SELECT {', '.join(columns)} FROM {table}"
        self.cur.execute(query)
        data = self.cur.fetchall()
        all_data[table] = (columns, data)
    return all_data
```

## Installation and Setup

### Prerequisites
- Python 3.7 or higher
- PyQt5 library
- Pandas library
- SQLite (included with Python)

### Quick Start
```bash
# Clone repository
git clone https://github.com/username/BillingInventorySystem.git
cd BillingInventorySystem

# Install dependencies
pip install PyQt5 pandas

# Initialize database
python databases.py

# Run application
python main.py
```

### Default Login Credentials
```
Administrator: admin / admin (Permission: 1)
Auditor: audit / audit (Permission: 2)
Customer: Register through user_info table
```

## Project Structure

```
BillingInventorySystem/
├── main.py              # Application entry point and page manager
├── loginWindow.py       # Authentication interface
├── adminWindow.py       # Administrator interface with full CRUD
├── customerWindow.py    # Customer interface with filtered access
├── auditWindow.py       # Auditor interface (read-only)
├── dbmanager.py         # Database operations and management
├── databases.py         # Database schema initialization
├── config.py            # Global configuration and user session
├── management.db        # SQLite database file
└── README.md           # Project documentation
```

## Core Features Implemented

### Multi-Role Management System
- **Administrator**: Full CRUD operations on all tables, Excel export, system management
- **Auditor**: Read-only access to all data, report generation capabilities
- **Customer**: Limited access to personal bills and transactions, payment processing

### Real-Time Data Operations
- **Dynamic Table Loading**: Conditional data filtering based on user roles
- **Live Search**: Real-time search across all columns with role-based filtering
- **Payment Processing**: Immediate database updates with transaction tracking

### Report Generation System
- **Excel Export**: Multi-sheet workbooks with all table data
- **Custom Filtering**: Role-based data access and export permissions
- **Transaction History**: Complete audit trail maintenance

### PyQt5 GUI Implementation
- **Modular Design**: Separate window classes for different user roles
- **Responsive Layout**: Dynamic widget sizing and positioning
- **Signal-Slot Communication**: Event-driven programming with PyQt5 signals

## Project Results

This billing and inventory system successfully demonstrates:

**Complete Desktop Application**: Full-featured GUI application with PyQt5 framework, SQLite database integration, and role-based access control for enterprise billing management.

**Multi-User Architecture**: Three distinct user roles (Administrator, Auditor, Customer) with differentiated access levels, secure authentication, and role-specific interface customization.

**Real-Time Database Operations**: Dynamic CRUD operations, live search functionality, filtered data access, and immediate payment processing with transaction tracking.

**Professional GUI Design**: Qt Designer-based interface creation, responsive layout management, custom dialogs, and intuitive user experience across all modules.

**Export and Reporting**: Pandas-powered Excel export functionality, multi-sheet report generation, and comprehensive data analysis capabilities for business intelligence.

**Modular Code Architecture**: Object-oriented design principles, separation of concerns, reusable database managers, and maintainable codebase structure.

The system demonstrates proficiency in desktop application development, database design, user interface creation, and enterprise software architecture patterns.
