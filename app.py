from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///notes.db"
db = SQLAlchemy(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)

class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    done = db.Column(db.Boolean, default=False)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(10), nullable=False)
    time = db.Column(db.String(10), nullable=False)
    content = db.Column(db.String(500), nullable=False)

with app.app_context():
    db.create_all()    

@app.route("/")
def home():
    notes = Note.query.all()
    return render_template("index.html", notes=notes)

@app.route("/add", methods=["POST"])
def add_note():
    content = request.form.get("content")
    if content:
        new_note = Note(content=content)
        db.session.add(new_note)
        db.session.commit()
    return redirect(url_for("home"))

@app.route("/delete/<int:note_id>", methods=["POST"])
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/reminders")
def reminders_page():
    reminders = Reminder.query.all()
    return render_template("reminders.html", reminders=reminders)

@app.route("/reminders/add", methods=["POST"])
def add_reminder():
    content = request.form.get("content")
    if content:
        new_reminder = Reminder(content=content)
        db.session.add(new_reminder)
        db.session.commit()
    return redirect(url_for("reminders_page"))

@app.route("/reminders/toggle/<int:reminder_id>", methods=["POST"]) 
def toggle_reminder(reminder_id):
    reminder = Reminder.query.get_or_404(reminder_id)
    reminder.done = not reminder.done
    db.session.commit()
    return redirect(url_for("reminders_page"))

@app.route("/reminders/delete/<int:reminder_id>", methods=["POST"])
def delete_reminder(reminder_id):
    reminder = Reminder.query.get_or_404(reminder_id)
    db.session.delete(reminder)
    db.session.commit()
    return redirect(url_for("reminders_page"))

@app.route("/schedule")
def schedule_page():
    events = Event.query.all()
    return render_template("schedule.html", events=events)

@app.route("/schedule/add", methods=["POST"])
def add_event():
    day = request.form.get("day")
    time = request.form.get("time")
    content = request.form.get("content")
    if day and time and content:
        new_event = Event(day=day, time=time, content=content)
        db.session.add(new_event)
        db.session.commit()
    return redirect(url_for("schedule_page"))

@app.route("/schedule/delete/<int:event_id>", methods=["POST"])
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    return redirect(url_for("schedule_page"))


if __name__ == "__main__":
    app.run(debug=True)