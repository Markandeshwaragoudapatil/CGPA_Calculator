from flask import Flask,render_template,request,session,redirect,url_for
from flask_session import Session

app=Flask(__name__)

app.config["SESSION_PERMANENT"]=False
app.config["SESSION_TYPE"]="filesystem"

Session(app)

@app.route("/")
def index():
    length=len(session['credits']) if 'credits' in session else 0
    return render_template("index.html",length=length,session=session)

@app.route("/calculate",methods=['GET','POST'])
def calculate():
    if request.method=='POST':
        decide=request.form.get("decide")
        sgpa=request.form.get('sgpa')
        credit=request.form.get('credit')
        
        # when user want to calculate total even after adding added button
        if (not sgpa or not credit) and (decide=='calculate' and 'credits' in session):
            return calculate_cgpa(session['credits'],session['sgpas'])
        

        if not sgpa or not credit or not decide:
            return redirect("/")
        
        try:
            sgpa=float(sgpa)
            credit=float(credit)
        except ValueError:
            return redirect('/')
        
        if "credits" not in session:
            session["credits"]=[]
        session["credits"].append(float(credit))

        if "sgpas" not in session:
            session["sgpas"]=[]
        session["sgpas"].append(float(sgpa))

        if decide=="add":
            return redirect(url_for('index'))
        elif decide=="calculate":
            return calculate_cgpa(session['credits'],session['sgpas'])
        

def calculate_cgpa(credits,sgpas):
    weighted_sum = sum(credit*sgpa for credit,sgpa in zip(credits,sgpas))
    total = weighted_sum / sum(credits)
    return render_template("result.html",session=session,total=total,length=len(session['credits']))
    # return f"Total : {total:.2f}"

@app.route("/newCalculation")
def newCalculation():
    session.clear()
    return redirect("/")

if __name__=="__main__":
    app.run(debug=True)