from flask import Flask, render_template, request, redirect, url_for
import requests
app = Flask(__name__)

# Mock user data for demonstration purposes
users = {
    "ayush": "12345678",
    "user2": "password2"
}

# Mock questionnaire questions
questions = [
    "user_age",
    "user_Gender",
    "user_stream",
    "user_internships",
    "user_CGPA",
    "user_hostel",
    "user_backlogs",
    "user_projects",
]

@app.route('/')
def login():
    return render_template('index.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    username = request.form['username']
    password = request.form['password']

    if username in users and users[username] == password:
        return redirect(url_for('questionnaire'))
    else:
        return "Invalid credentials. Please try again."

@app.route('/questionnaire')
def questionnaire():
    return render_template('questionnaire.html')

@app.route('/submit_questionnaire', methods=['POST'])
def submit_questionnaire():
    answers = {
        "Age" : 0,               
        "Gender"  : 0,              
        "Stream" : 0,              
        "Internships" : 0,          
        "CGPA" : 0,                
        "Hostel"  : 0,              
        "HistoryOfBacklogs" : 0,    
        "projectsCount"  : 0,
    }
    ans = ["Age",                
        "Gender",                
        "Stream",               
        "Internships",           
        "CGPA",                 
        "Hostel",               
        "HistoryOfBacklogs",     
        "projectsCount" ]
    j=0
    for question in questions:
        if(question=="user_CGPA"):
            x = ((request.form[question]))
            z=float(x)
            answers[ans[j]] = round(z)
            j+=1
      
        else:
            answers[ans[j]] = int(request.form[question])
            j+=1
    
    print(answers)

    url = 'http://127.0.0.1:8000/predict'

    response = (requests.post(url, json=answers))
    print(response)
    # value = response['prediction_of_placement']

    # print(value)
    if response.status_code == 200:
        # Extract the JSON data from the response
        data = response.json()
        value = data['prediction_of_placement']
        print(value)
        if(data['no_of_true']>=3):
            return render_template('placed.html', suggestions=value)
        else:
            return render_template("suggestion.html")
    else:
        # Handle the error response
        return f"Error: {response.status_code}"



@app.route('/suggestions')
def suggestions():
    # Here you can generate and display suggestions based on the answers submitted
    return render_template('suggestions.html')

if __name__ == '__main__':
    app.run(debug=True)
