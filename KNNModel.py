import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from flask import Flask, request, render_template, redirect
from flask import Flask, send_file

app = Flask(__name__,template_folder='C:\\Users\\pavan\\Desktop\\LOAN\\templates',static_url_path='/static')
@app.route('/download_project')
def download_project():
    # Specify the path to your PDF file
    pdf_path = "C:\\Users\\pavan\\Desktop\\LOAN\\Loan-Distribution-Predictor-A-Machine-Learning-Project (1).pdf"
    
    # Specify the name you want for the downloaded file
    filename = 'Loan_Predictor_Project.pdf'

    return send_file(pdf_path, as_attachment=True, download_name=filename)

@app.route("/", methods=["GET"])
def welcome():
    return render_template("welcome.html")

@app.route("/index", methods=["GET"])
def index1():
    return render_template("index1.html")

@app.route('/login')
def login():
    return render_template('login.html')
@app.route("/ml_model", methods=["GET", "POST"])
def ml_model():
    res = None
    if request.method == "POST":
        no_loans = float(request.form.get("loansinput", 0))
        credit_score_input = float(request.form.get("creditinput", 0))

        dataset = pd.read_csv("loan.csv")
        X = dataset.iloc[:, :-1].values
        y = dataset.iloc[:, -1].values
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=21)
        sc = StandardScaler()
        X_train = sc.fit_transform(X_train)
        X_test = sc.transform(X_test)

        classifier = KNeighborsClassifier(n_neighbors=5, metric='minkowski', p=2)
        classifier.fit(X_train, y_train)
        arr=np.ones(1)
        arr = classifier.predict(sc.transform([[no_loans, credit_score_input]]))
        if no_loans>10:
            res = "sorry...you can't take a new loan since you have already taken maximum loans."
        elif credit_score_input>900:
            res="you cant have a credit score greater than 900"
        elif credit_score_input<700:
            res="you cant have a credit score less than than 900"
        elif arr[0] == 1:
            res = "Congratulations...You are eligible for a new loan"
        else:
            res = "Sorry...You are not eligible for a new loan"
    return render_template("index1.html", result=res)
if __name__ == "__main__":
    app.run(debug=True)
