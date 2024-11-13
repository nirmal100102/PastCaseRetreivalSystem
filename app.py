from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Database connection
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',  # Update with your database username
        password='root',  # Update with your database password
        database='past_cases_db'  # Update with your database name
    )
    return connection

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search_cases():
    case_description = request.form['case_description'].strip().lower()
    matched_cases = []

    # Define available keywords
    keywords = ['criminal law', 'family law', 'civil rights', 'property law', 'corporate fraud', 'Labour and Employment Law', 'Taxation Law', 'Environmental Law', 'Consumer Protection Law', 'Arbitration and Dispute Resolution', 'Immigration Law', 'Banking and Finance Law']

    # Check if the user input is "all cases"
    if case_description == "all cases":
        query = """
            SELECT case_id, case_description, matched_keyword, case_date, status, 
                   created_at, criminal_name, officer_name 
            FROM past_cases
        """
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query)
        matched_cases = cursor.fetchall()
        cursor.close()
        connection.close()
    else:
        # Check if the input matches one of the defined keywords
        if case_description in keywords:
            query = """
                SELECT case_id, case_description, matched_keyword, case_date, status, 
                       created_at, criminal_name, officer_name 
                FROM past_cases 
                WHERE matched_keyword = %s
            """
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, (case_description,))
            matched_cases = cursor.fetchall()
            cursor.close()
            connection.close()

    # If no cases match, add a message
    message = "No cases matched the given description or keyword." if not matched_cases else None

    return render_template('results.html', matched_cases=matched_cases, case_description=case_description, message=message)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')

