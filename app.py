from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
from datetime import datetime

app = Flask(__name__)

# Secret key for session
app.secret_key = "mysecuresecretkey12345"

# Database connection function
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # Update with your DB username
            password='root',  # Update with your DB password
            database='past_cases_db'  # Update with your DB name
        )
        return connection
    except Error as e:
        print(f"Database connection failed: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/addcase')
def add_case():
    return render_template('addcase.html')
    # Example logic for adding a case
    case_details = request.form.get('case_details')
    # Add case to the database here
    if case_details:
        # Simulate successful case addition
        flash("Case successfully added!")
        return redirect('/')
    else:
        flash("Failed to add the case. Please try again.", "error")
        return redirect('/')

@app.route('/processaddcase', methods=['POST'])
def processaddcase():
    try:
        # Debugging: Log received form data
        print("Form data received:", request.form)

        # Retrieve form data
        case_id = request.form.get('case_id')  # Matches the 'name' attribute in the form
        case_description = request.form.get('case_description')
        matched_keyword = request.form.get('matched_keyword')
        case_date = request.form.get('case_date')
        status = request.form.get('status')
        criminal_name = request.form.get('criminal_name')
        officer_name = request.form.get('officer_name')
        created_at = request.form.get('created_at')

        # Debugging: Log each variable
        print(f"case_id={case_id}, case_description={case_description}, matched_keyword={matched_keyword}, "
              f"case_date={case_date}, status={status}, criminal_name={criminal_name}, "
              f"officer_name={officer_name}, created_at={created_at}")

        # Validate form inputs
        if not all([case_id, case_description, matched_keyword, case_date, status, criminal_name, officer_name, created_at]):
            flash("All fields are required. Please fill out the form completely.", "error")
            return redirect('/addcase')

         # Connect to MySQL Database
        conn = get_db_connection()
        cursor = conn.cursor()

        insert_query = """
            INSERT INTO past_cases (case_id, case_description, matched_keyword, case_date, status, criminal_name, officer_name, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (case_id, case_description, matched_keyword, case_date, status, criminal_name, officer_name, created_at))
        
        # Commit the transaction
        conn.commit()
        
        # Close the database connection
        cursor.close()
        conn.close()

        # Flash success message and redirect
        flash("Case added successfully!", "success")
        return redirect('/')

    except Error as e:
        print(f"Error while adding case: {e}")
        flash("An error occurred while adding the case. Please try again.", "error")
        return redirect('/addcase')

@app.route('/search', methods=['POST'])
def search_cases():
    case_description = request.form['case_description'].strip().lower()
    matched_cases = []

    valid_keywords = [
        'criminal law', 'family law', 'civil rights', 'property law',
        'corporate fraud', 'labour and employment law', 'taxation law',
        'environmental law', 'consumer protection law',
        'arbitration and dispute resolution', 'immigration law',
        'banking and finance law'
    ]

    if case_description == "all cases":
        query = "SELECT * FROM past_cases"
        params = ()
    elif case_description in valid_keywords:
        query = "SELECT * FROM past_cases WHERE LOWER(matched_keyword) = %s"
        params = (case_description,)
    else:
        flash('Invalid keyword or no matching cases found.')
        return render_template('results.html', matched_cases=[], case_description=case_description, message="No results found.")

    try:
        connection = get_db_connection()
        if not connection:
            flash('Database connection failed.')
            return redirect('/')

        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params)
        matched_cases = cursor.fetchall()
        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Error while searching cases: {e}")
        flash('An error occurred while searching cases. Please try again.')

    message = "No matching cases found." if not matched_cases else None
    return render_template('results.html', matched_cases=matched_cases, case_description=case_description, message=message)

if __name__ == '__main__':
    app.debug = True
    app.run()
