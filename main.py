import csv
import logging
import os.path
from datetime import datetime
from abc import ABC, abstractmethod
import requests
import yfinance as yf


# Create a logger object, format, and file handler
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('debug.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class Stock:
    """Represents a stock holding with a symbol, number of shares, and price per share"""
    def __init__(self, symbol, shares, cost_per_share):
        self.symbol = symbol
        self.shares = shares
        self.cost_per_share = cost_per_share

    def calculate_total_cost(self):
        """Calculates and returns total cost of the stock holding"""
        return self.shares * self.cost_per_share

    def __str__(self):
        return f'Symbol: {self.symbol} Shares: {self.shares} Cost per share: ${self.cost_per_share}'


class Transaction:
    """Represents a buy or sell transaction with number of shares, price per share, and timestamp"""
    def __init__(self, stock, transaction_type, shares, cost_per_share):
        self.stock = stock
        self.transaction_type = transaction_type  # 'buy' or 'sell'
        self.shares = shares
        self.cost_per_share = cost_per_share
        self.timestamp = datetime.now()

    def calculate_transaction_total_cost(self):
        """Calculates and returns the total cost of the transaction"""
        return self.shares * self.cost_per_share

    def __str__(self):
        return f'{self.transaction_type} shares {self.shares} of {self.stock.symbol} at ${self.cost_per_share} per share on {self.timestamp}'


class Portfolio:
    """Represents a collection of stocks and transactions"""
    def __init__(self):
        self.stocks = []
        self.transactions = []

    def add_stock(self, stock):
        """Appends a new stock holding to the portfolio"""
        self.stocks.append(stock)

    def transact(self, stock, transaction_type, shares, cost_per_share):
        """Process buy or sell transaction entered by the user"""

        # TODO Correct data validation - should be done before method is used
        if transaction_type not in ['buy', 'sell']:
            raise ValueError("Invalid transaction type. Use 'buy' or 'sell'.")

        if transaction_type == 'sell' and stock.shares < shares:
            raise ValueError("Not enough shares to sell.")

        # Append transaction to transactions list
        transaction = Transaction(stock, transaction_type, shares, cost_per_share)
        self.transactions.append(transaction)

        # Update the number of shares
        if transaction_type == 'buy':

            # Calculate the new average cost after the buy transaction
            total_cost = (stock.cost_per_share * stock.shares) + (cost_per_share * shares)
            total_quantity = stock.shares + shares
            stock.cost_per_share = total_cost / total_quantity
            stock.shares += shares

        if transaction_type == 'sell':
            stock.shares -= shares

    def calculate_portfolio_value(self):
        """Calculates and returns the total cost of the portfolio"""
        total_value = 0
        for stock in self.stocks:
            total_value += stock.calculate_total_cost()
        return total_value

    def __str__(self):
        portfolio_str = "Portfolio:\n"
        for stock in self.stocks:
            portfolio_str += str(stock) + "\n"
        portfolio_str += f"\nTotal Portfolio Value: ${self.calculate_portfolio_value()}"
        portfolio_str += "\nTransactions entered in current session:\n"
        for transaction in self.transactions:
            portfolio_str += str(transaction) + "\n"

        return portfolio_str


class FileOp(ABC):
    """Represents reading and writing to files"""
    def __init__(self, portfolio, filename):
        self.portfolio = portfolio
        self.filename = filename

    @abstractmethod
    def get_file_name(self):
        pass


class ReadStockFile(FileOp):
    """Represents read the portfolio of stock from a file"""
    def __init__(self, portfolio, filename):
        super().__init__(portfolio, filename)

    def get_file_name(self):
        """Obtain filename from user"""

        # TODO input statement or default
        filename = 'portfolio.csv'

    def read_stocks_from_csv(self):
        """Read previously entered stock holdings into portfolio"""

        # TODO try except block and file management
        with open(self.filename, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            for row in reader:
                symbol, shares, cost_per_share = row
                stock = Stock(symbol, int(shares), float(cost_per_share))
                self.portfolio.stocks.append(stock)
            logger.info(f'Portfolio file: {self.filename} read into memory.')


class WriteStockFile(FileOp):
    """Represents writing the portfolio of stocks to a file"""

    def __init__(self, portfolio, filename):
        super().__init__(portfolio, filename)

    def get_file_name(self):
        """Obtain filename from user"""

        # TODO input statement or default
        filename = 'portfolio.csv'

    def write_stocks_to_csv(self):
        """Write new or updated portfolio of stocks to a file"""

        # TODO try except block and file management
        with open(self.filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Symbol', 'Shares', 'CostPerShare'])
            for stock in self.portfolio.stocks:
                writer.writerow([stock.symbol, stock.shares, stock.cost_per_share])
        logger.info(f'Portfolio file: {self.filename} written to drive.')


class WriteTransactionFile(FileOp):
    """Represents writing the transactions to a file"""

    def __init__(self, portfolio, filename):
        super().__init__(portfolio, filename)

    def get_file_name(self):
        """Obtain filename from user"""

        # TODO input statement or default
        filename = 'portfolio.cvs'

    def write_transactions_to_csv(self):
        """Write new or append transactions to a file"""

        # TODO try except block and file management
        if os.path.isfile(self.filename):
            my_mode = 'a'
        else:
            my_mode = 'w'

            # Create or append transactions to file if it exists
        with open(self.filename, mode=my_mode, newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if my_mode == 'w':
                writer.writerow(['Symbol', 'TransactionType', 'Shares', 'CostPerShare', 'Timestamp'])
            for transaction in self.portfolio.transactions:
                writer.writerow([transaction.stock.symbol, transaction.transaction_type,
                                 transaction.shares, transaction.cost_per_share, transaction.timestamp])
            logger.info(f'Transactions file: {self.filename} written in mode: {my_mode}.')


class WriteGLReportFile:
    """Represents writing the gain loss report to a file"""

    def __init__(self, gl_report, filename):
        self.filename = filename
        self.gl_report = gl_report

    def get_file_name(self):
        """Obtain filename from user"""

        # TODO input statement or default
        filename = 'gain_loss_report.csv'

    def write_gl_report_to_csv(self):
        """Write gain loss report to a file"""

        # TODO try except block and file management
        with open(self.filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Symbol', 'Shares', 'CostPerShare', 'TotalCost', 'CurrentPrice', 'TotalPrice',
                             'UnrealizedGL'])
            for stock in self.gl_report:
                writer.writerow([stock[0], stock[1], stock[2], stock[3], stock[4], stock[5], stock[6]])
        logger.info(f'Portfolio file: {self.filename} written to drive.')


class Report(ABC):
    """Represents parent class of reports"""
    def __init__(self, portfolio):
        self.portfolio = portfolio

    @abstractmethod
    def display_report(self):
        pass


class GainLossReport(Report):
    """Represents gain loss report"""
    def __init__(self, portfolio):
        super().__init__(portfolio)
        self.gl_report = []

    def display_report(self):
        """Displays gain loss report to terminal"""

        # TODO Display on screen better - displays lists without headings
        self.create_gl()
        print('\nGain Loss Report')
        for stock in self.gl_report:
            print(stock)

    def get_price(self, t_symbol):
        """Obtains the share price from yfinance"""
        try:
            latest_price = yf.Ticker(t_symbol).history().iloc[-1, 3]  # work around pulls the current price from history
            # latest_price = float(ticker.info['lastPrice'])  # should work but does not; used the above from reddit
            logger.info(f"The latest price of {t_symbol} is: {latest_price}")
            # print(yf.Ticker(t_symbol).info) # raises except 404; should work but does not; used the above from reddit
            return latest_price
        except requests.RequestException as e:
            logger.error(f"Unable to retrieve the latest price for {t_symbol} - Error: {e}")
            return -1
        except IndexError as e:
            logger.error(f"Unable to retrieve the latest price for {t_symbol} - Error: {e}")
            return -1

    def create_gl(self):
        """Creates the gain loss report row by row"""
        gl_row = []
        for stock in self.portfolio.stocks:
            gl_row.append(stock.symbol)
            gl_row.append(stock.shares)
            gl_row.append(stock.cost_per_share)
            gl_row.append(stock.calculate_total_cost())
            current_price = self.get_price(stock.symbol)
            gl_row.append(current_price)
            total_current_price = current_price * stock.shares
            gl_row.append(total_current_price)
            gl = total_current_price - stock.calculate_total_cost()
            gl_row.append(gl)
            self.gl_report.append(gl_row)
            gl_row = []
        return self.gl_report


class DividendReport(Report):
    """Represents dividends paid for a period of time"""
    def __init__(self, portfolio):
        super().__init__(portfolio)

    def display_report(self):
        """Displays report to terminal"""

        # TODO Need to create this report
        print('\nDividend Report')

    def create_dividend(self):
        """Creates the dividend report"""

        # TODO Need to create this report
        pass


class UI:
    """Represents user interface for updating a stock portfolio"""
    def __init__(self, portfolio):
        self.portfolio = portfolio

    def run_main_menu(self):
        """Starts the command line user interface"""
        print("--- Welcome to Mike's Python Project ---\n")
        while True:
            self.show_main_menu()
            user_selection = input('Enter your choice: ')
            if user_selection == '1':
                print('You chose 1 - under development - chose 2 or skip to 3 adding transactions')

                # TODO clean up main menu
            elif user_selection == '2':
                print('You chose 2')

                # TODO get existing file name from user
                filename = 'portfolio.csv'
                read_file = ReadStockFile(self.portfolio, filename)
                read_file.read_stocks_from_csv()
            elif user_selection == '3':
                print('You chose 3')

                # TODO get transaction data from user; user must chose 1 or 2 before transactions!!!
                self.add_transaction()
            elif user_selection == '4':
                print('You chose 4')
                self.display_portfolio()
            elif user_selection == '5':
                print('You chose 5')

                # TODO get filenames from user or default
                filename = 'portfolio.csv'
                write_portfolio_file = WriteStockFile(self.portfolio, filename)
                write_portfolio_file.write_stocks_to_csv()

                filename = 'transactions.csv'
                write_transaction_file = WriteTransactionFile(self.portfolio, filename)
                write_transaction_file.write_transactions_to_csv()

                filename = 'gain_loss_report.csv'
                gl_r = GainLossReport(self.portfolio)
                write_gl_report_file = WriteGLReportFile(gl_r.create_gl(), filename)
                write_gl_report_file.write_gl_report_to_csv()

                print("Data saved to csv files.")
            elif user_selection == '6':

                # TODO Verify files were saved
                print('You chose 6')
                print('Exiting...')
                break
            else:
                print("Invalid choice. Please try again.")

    def show_main_menu(self):
        """Display the main menu"""
        print('\nMain Menu:')
        print('1. Start new portfolio')
        print('2. Open existing portfolio from file')
        print('3. Add transaction')
        print('4. Display report')
        print('5. Save files')
        print('6. Exit')

    def add_transaction(self):
        """Obtain transaction data from user"""
        self.display_portfolio()

        # Obtain stock symbol from user
        symbol = input('Enter the stock symbol: ')

        def find_stock(s):
            """Returns stock given the symbol"""
            for s in self.portfolio.stocks:
                if s.symbol == symbol:
                    return s

        stock = find_stock(symbol)
        # Create a new stock_holding instance if none is found
        if stock is None:
            print('--- Stock not currently owned ---')
            cont_flag = input('Enter y to add to portfolio or n to go back: ')
            if cont_flag != 'y':
                return
            stock = Stock(symbol, 0, 0 )
            self.portfolio.add_stock(stock)

        # Obtain remaining transaction data from user
        transaction_type = input("Enter transaction type ('buy' or 'sell'): ")
        shares = int(input('Enter the number of shares: '))
        cost_per_share = float(input('Enter cost per share: '))

        # Call transact portfolio method
        self.portfolio.transact(stock, transaction_type, shares, cost_per_share)
        print('Transaction completed')

    def display_portfolio(self):
        """Displays current portfolio to the terminal"""
        print(self.portfolio)

        # Works but takes too long to run
        # gl_r = GainLossReport(self.portfolio)
        # gl_r.display_report()


# Initialize portfolio and UI instance
my_portfolio = Portfolio()
ui = UI(my_portfolio)

if __name__ == '__main__':
    ui.run_main_menu()


# TODO Clean up display report , maybe delete? - takes time to run

# TODO Create dividend report for a given time period

# TODO Cleanup Print Statements
# Format numbers when printing to terminal
# Remove unneeded print statements

# TODO Data Validation
# Keep all stock symbols lower case, including saving to the file; but display them in all upper case
# Sell too much should not stop the program - allow user to reenter

# TODO File Management
# see above os and os.path

# TODO Exception Handling
# especially reading and writing files

# TODO User Interface
# Rework main menu
# Add GUI - tkinter

# TODO Prevent user from reading portfolio in after entering transactions
# User testing indicates that if transactions are enter menu choice 3 - then the portfolio is read in choice 2
# incorrect data will result

# TODO Testing

# TODO Implement pandas DataFrames
# Not until version 3.0!
