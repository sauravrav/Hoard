def response_content():
    form = """
    <html>
        <body>
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
        </body>
    </html>
    """
    return form