from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Global variables to store budget and expenses
budget = 0
expenses = []

@app.route("/")
def index():
    """Render the main page."""
    return render_template("index.html")

@app.route("/set_budget", methods=["POST"])
def set_budget():
    """Set the monthly budget."""
    global budget
    data = request.get_json()
    try:
        budget = float(data["budget"])
        return jsonify({"message": "Budget set successfully!", "remaining_budget": budget})
    except ValueError:
        return jsonify({"message": "Invalid budget value provided."}), 400

@app.route("/add_expense", methods=["POST"])
def add_expense():
    """Add a new expense and update the remaining budget."""
    global expenses
    data = request.get_json()
    try:
        # Extract data from request
        date = data["date"]
        amount = float(data["amount"])
        category = data["category"]
        description = data["description"]

        # Add expense to the list
        expenses.append({
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        })

        # Calculate remaining budget
        total_spent = sum(expense["amount"] for expense in expenses)
        remaining_budget = budget - total_spent

        # Provide savings advice
        if remaining_budget <= 0:
            advice = "You've exceeded your budget. Try to save more next month."
        elif remaining_budget <= 0.2 * budget:
            advice = "Caution: You're close to exceeding your budget!"
        elif remaining_budget >= 0.5 * budget:
            advice = "Good job! You’re on track to save well this month."
        else:
            advice = "You're doing fine. Keep an eye on your spending!"

        return jsonify({
            "message": "Expense added successfully!",
            "remaining_budget": remaining_budget,
            "advice": advice,
            "expenses": expenses
        })
    except (KeyError, ValueError):
        return jsonify({"message": "Invalid expense data provided."}), 400

@app.route("/get_expenses", methods=["GET"])
def get_expenses():
    """Retrieve all expenses."""
    return jsonify(expenses)

if __name__ == "__main__":
    app.run(debug=True)