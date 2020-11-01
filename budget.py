import numpy as np
import math


class Category:

    total_withdrawn = 0.0

    def __init__(self, category_name):
        self.name = category_name
        self.balance = 0.0
        self.amount_withdrawn = 0.0
        self.ledger = []

    def deposit(self, amount, description=""):
        """
        Deposites money into the budget category.
        @param amount: The amount to deposit.
        @param description: A description of the deposit (optional).
        """
        self.balance += amount
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description="") -> bool:
        """
        Withdraws money from the budget category.
        @param amount: The amount to with draw.
        @param description: A description of the withdrawal (optional).
        @return: True if the withdraw succeeded, False otherwise.
        """
        if Category.check_funds(self, amount):
            self.balance -= amount
            self.amount_withdrawn += amount
            Category.total_withdrawn += amount
            self.ledger.append({"amount": -amount, "description": description})
            return True
        else:
            return False

    def get_balance(self) -> float:
        """
        Gets the current balance of the budget category.
        @return: The current balance of the budget category.
        """
        return self.balance

    def transfer(self, amount, category) -> object:
        """
        Transfers money between budget categories.
        @param amount: The amount of money to transfer.
        @param category: The category to transfer money to.
        @return: True if the transfer succeeded, False otherwise.
        """
        if Category.check_funds(self, amount):
            self.withdraw(amount, description=f"Transfer to {category.name}")
            category.deposit(amount, description=f"Transfer from {self.name}")
            return True
        else:
            return False

    def check_funds(self, amount) -> bool:
        """
        Verifies whether there are sufficient funds in the budget category for a withdraw or transfer to take place.
        @param amount: The amount of money to check the budget category's balance against.
        @return: True if the amount of money is less than the balance of the budget category, False otherwise.
        """
        return False if amount > self.balance else True

    def __str__(self) -> str:
        """
        Returns information about transactions in a category.
        @return: A string containing the category name and a record of the category's deposits and withdrawals.
        """
        string = ""
        string += f"{self.name.center(30, '*')}\n"
        for item in self.ledger:
            string += f"{item['description']}"[0:23].ljust(23, " ")
            string += f"{item['amount']:.2f}"[0:7].rjust(7, " ")
            string += "\n"
        string += f"Total: {self.balance}"
        return string


def create_spend_chart(categories) -> str:
    """
    Creates a chart visualizing what percentage of all money withdrawn was spent
    in each category.
    @param categories: A list of categories to include in the chart.
    @return: A string representation of the chart.
    """
    def build_array():
        """
        Constructs an array representaition of the spending chart.
        @return: An array reprenstation of the spending chart.
        """

        # gets the longest category name in order to determine how tall the array needs to be
        longest_name = len(max([obj.name for obj in categories], key=len))

        # creates an empty object array
        array = np.empty([longest_name + 12, len(categories) + (len(categories) * 2) + 3], dtype=object)

        # inserts y-axis of chart into array
        for row, num in zip(range(12), range(100, -10, -10)):
            array[row, 0] = num

        # inserts pipe seperators for y-axis and dash seperators for x-axis into array
        array[:11, 1] = "|"
        array[11, 2:] = "-"

        # inserts category names and point markers (represented by the letter "o") into array
        for row in range(3, (len(categories) * 3) + 3, 3):
            obj = categories[(row // 3) - 1]
            percentage_spent = (math.floor((obj.amount_withdrawn / Category.total_withdrawn) * 100) // 10) * 10
            array.T[row, 10 - (percentage_spent // 10):11] = "o"
            for char, index in zip(obj.name.capitalize(), range(12, 12 + longest_name)):
                array.T[row, index] = char
        return array

    def build_string(chart):
        """
        Constructs a string from an array representation of the spendiing chart.
        @param chart: An array representation of the spending chart.
        @return: A string representation of the spending chart.
        """
        string = "Percentage spent by category\n"
        for index, row in enumerate(chart):
            for subdex, cell in enumerate(row):
                if subdex == 0:
                    if index > 0:
                        string += " "
                    if index >= 10:
                        string += " "
                if cell is not None:
                    string += f"{cell}"
                else:
                    string += " "
            if (index + 1) < len(chart):
                string += "\n"
        return string

    chart_array = build_array()
    chart_string = build_string(chart_array)
    return chart_string
