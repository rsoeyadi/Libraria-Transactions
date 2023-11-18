from flask import Flask, jsonify, request, redirect
import pymysql
import uuid
from flask_cors import CORS
from datetime import datetime

# Set the database credentials
host = 'database-1.cwruyiuygx34.us-east-2.rds.amazonaws.com'
port = 3306
user = 'admin'
password = 'password'
database = 'library_system'

# Connect to the database
connection = pymysql.connect(
    host=host,
    port=port,
    user=user,
    password=password,
    database=database
)
app = Flask(__name__)
CORS(app)

# get all transactions with page number + limits. If page == 0, return all
@app.route("/transactions")
def get_transactions():
    page_num_str = request.args.get("page")
    limit_str = request.args.get("limit")
    cur = connection.cursor()

    if not page_num_str: 
        cur.execute("SELECT * FROM transactions")
        result = cur.fetchall()
        cur.close()
        return jsonify(result)

    page_num = int(page_num_str)
    limit = int(limit_str)
    
    # if not specify page, or set it to 0
    # we return all books
    if page_num == 0:
        cur.execute("SELECT * FROM transactions")
    else:
        offset = (page_num - 1) * limit
        cur.execute(f"SELECT * FROM transactions LIMIT {limit} OFFSET {offset}")
    result = cur.fetchall()
    cur.close()
    return jsonify(result)

# get transactions with same user
@app.route("/transactions/users")
def get_transactions_from_user():
    username = request.args.get("username")
    cur = connection.cursor()

    cur.execute(f"SELECT * FROM transactions WHERE Username = '{username}'")
    result = cur.fetchall()
    cur.close()
    return jsonify(result)

# add a transaction
@app.route('/transactions', methods=['POST'])
def add_transactions():
    username = request.form['Username']
    isbn = request.form['ISBN']

    unique_id = str(uuid.uuid4())
    current_time = datetime.now()
    formatted_time = current_time.strftime('%Y-%m-%d')

    cur = connection.cursor()
    transaction_id = "Transaction ID"
    cur.execute(f"INSERT INTO transactions(`{transaction_id}`, Reserve_Date, Return_Date, Username, ISBN) VALUES('{unique_id}', '{formatted_time}', 'NULL', '{username}', '{isbn}')")
    cur.close()

    return redirect('/transactions')

# update a transaction status
@app.route('/transactions', methods=['PUT'])
def update_transctions():
    transaction_id = request.form['transaction_id']

    current_time = datetime.now()
    formatted_time = current_time.strftime('%Y-%m-%d')

    cur = connection.cursor()
    transaction_id_name = "Transaction ID"
    cur.execute(f"UPDATE transactions SET Return_Date = '{formatted_time}' WHERE `{transaction_id_name}` = '{transaction_id}'")
    cur.close()

    return redirect('/transactions')

# remove a transaction
@app.route('/transactions', methods=['DELETE'])
def delete_transaction():
    transaction_id = request.form['transaction_id']

    cur = connection.cursor()
    transaction_id_name = "Transaction ID"
    cur.execute(f"DELETE FROM transactions WHERE `{transaction_id_name}` = '{transaction_id}'")
    cur.close()

    return redirect('/transactions')

# remove all transactions for a book
@app.route('/transactions_books', methods=['DELETE'])
def delete_transaction_book():
    isbn = request.form['isbn']

    cur = connection.cursor()
    cur.execute(f"DELETE FROM transactions WHERE ISBN = '{isbn}'")
    cur.close()

    return redirect('/transactions')

@app.get("/")
def root():
    # cur = connection.cursor()
    # cur.execute("ROLLBACK")
    # result = cur.fetchall()
    # cur.close()
    # return jsonify(result)
    return {"message": "This microservice is for our library catalog."}

if __name__ == "__main__":
    app.run(debug=True)
    #app.run(app, host="0.0.0.0", port=8000)
