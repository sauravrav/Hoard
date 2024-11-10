def response_content(transaction_data=None, bank_user_data=None, error_message=None):
    error_banner = ""
    if error_message:
        error_banner = f"""
        <div style="background-color: red; color: white; padding: 10px; margin-bottom: 10px;">
            <span>{error_message}</span>
            <button onclick="this.parentElement.style.display='none'">Close</button>
        </div>
        """

    form = """
    <div id="form-section" style="display:{form_display}">
        <h1>Transfer Funds</h1>
        <form method="post" action="/">
            <label for="source_account_id">Source Account ID:</label>
            <input type="number" id="source_account_id" name="source_account_id" required><br><br>

            <label for="target_account_id">Target Account ID:</label>
            <input type="number" id="target_account_id" name="target_account_id" required><br><br>

            <label for="amount">Amount:</label>
            <input type="number" id="amount" name="amount" required><br><br>

            <button type="submit">Send</button>
        </form>
    </div>
    """
    # .format(form_display="none" if error_message else "block")

    transaction_table = "<h2>Transaction History</h2><table border='1'><tr><th>ID</th><th>Amount</th><th>Date</th><th>Details</th></tr>"
    for transaction in transaction_data:
        transaction_table += f"<tr><td>{transaction.id}</td><td>{transaction.amount}</td><td>{transaction.timestamp}</td><td>{transaction.description}</td></tr>"
    transaction_table += "</table>"

    bank_user_table = """
    <h2>Bank and Account Details</h2>
    <table border="1">
        <tr><th>Account Id</th><th>Bank Name</th><th>User First Name</th><th>User Last Name</th><th>Account Type</th><th>Balance</th></tr>
    """
    for row in bank_user_data:
        bank_user_table += f"""
        <tr>
            <td>{row.account_id}</td>
            <td>{row.bank_name}</td>
            <td>{row.user_first_name}</td>
            <td>{row.user_last_name}</td>
            <td>{row.account_type}</td>
            <td>{row.balance}</td>
        </tr>
        """
    bank_user_table += "</table>"

    return f"""
    <html>
        <body>
            {error_banner}
            {form}
            {transaction_table}
            {bank_user_table}
        </body>
    </html>
    """