# Import libraries
from flask import Flask, request, jsonify, url_for, render_template, redirect
# Instantiate Flask functionality
app = Flask(__name__)
# Sample data
transactions = [
    {'id' : 1, 'date': '2025-07-25', 'amount' : 100},
    {'id' : 2, 'date' : '2025-07-26', 'amount' : 200},
    {'id' : 3, 'date' : '2025-07-27', 'amount' : 300},
    {'id' : 4, 'date' : '2025-07-28', 'amount' : 400},
    {'id' : 5, 'date' : '2025-07-29', 'amount' : 500}
]


# Read operation
# This function containing the render_template function will list all transactions once the user hits the base URL
@app.route("/")
def get_transactions():
    return render_template('transactions.html', transactions=transactions)
    

# Create operation
@app.route("/add", methods=["GET", "POST"])
def add_transaction():
    if request.method == "POST":
        # Create new transaction values using the field values
        transaction = {
                  'id': len(transactions) + 1,
                  'date': request.form['date'],
                  'amount': float(request.form['amount'])
                 }
        # Append the created transaction to the list of existing ones
        transactions.append(transaction)

        # Redirect to the transaction list page after adding the new transaction
        return redirect(url_for("get_transactions"))
        # If the return method is GET, we render the form template to display the add transaction form page
    return render_template("form.html")


# Update operation
@app.route("/edit/<int:transaction_id>", methods = ["GET", "POST"])
def edit_transaction(transaction_id):
    if request.method == "POST":
        # Access form data
        date = request.form['date']
        amount = float(request.form['amount'])

        # Find the transaction with the matching ID"
        for transaction in transactions:
            if transaction["id"] == transaction_id:
                transaction['date'] = date
                transaction['amount'] = amount
                break                               # Exit the loop once the transaction is found and updated
        return redirect(url_for("get_transactions"))
    # If the request method is GET, find the transaction with the matching ID and render the edit form
    for transaction in transactions:
        if transaction["id"] == transaction_id:
            return render_template("edit.html", transaction=transaction)
    return {"message" : "Transaction not found"}, 404

# Delete operation
@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
        for transaction in transactions:
            if transaction["id"] == transaction_id:
                transactions.remove(transaction)
                break # Exit the loop once the transaction with the ID is found
        return redirect(url_for("get_transactions"))
        return {"message" : "Transaction not found"}, 404


# Search transactions
@app.route("/search", methods = ["GET", "POST"])
def search_transactions():
    if request.method == "POST":
        try: 
            min_amount = float(request.form["min_amount"])
            max_amount = float(request.form["max_amount"])
            filtered_transactions = [
            transaction for transaction in transactions
            if min_amount <= transaction["amount"] <= max_amount
        ]
            # Walrus operator implementation of list comprehension with variable assignment inside - ADVANCED
            # filtered_transactions = [
            #     transaction for transaction in transactions
            #     if(amount := transaction["amount"]) and min_amount <= amount <= max_amount
            # ]
            return render_template("transactions.html", transactions = filtered_transactions)
        except(ValueError):
            return jsonify({"message" : "Input valid values. Please enter numbers only"}, 400)
    return render_template("search.html")
    
# Total Balance
@app.route("/balance")
def total_balance():
    pass


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)