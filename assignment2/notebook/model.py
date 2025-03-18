import json
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:////Users/sohiniroy/Documents/cosi217/HW1/instance/db.sqlite"
)
db.init_app(app) #configure Flask with SQLAlchemy

class Note(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True) # unique id
    title: Mapped[str] = mapped_column(unique=True, nullable=False) # note title
    content: Mapped[str] = mapped_column(nullable=False) # note content
    comments: Mapped[str] = mapped_column(default="[]")  # comment stored as JSON string
    timestamp: Mapped[str] = mapped_column(nullable=False) # note timestamp
    comment_timestamps: Mapped[str] = mapped_column(default="[]")  # comment timestamps stored as JSON string

    def add_comment(self, comment):
        if not self.timestamp:
            self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # check that timestamp exists

        # load existing comments and timestamps
        comments_list = json.loads(self.comments or "[]")
        timestamps_list = json.loads(self.comment_timestamps or "[]")

        comments_list.append(comment)
        timestamps_list.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))  

        self.comments = json.dumps(comments_list)
        self.comment_timestamps = json.dumps(timestamps_list)


with app.app_context():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def page():
    notes = Note.query.all() #get all notes
    if request.method == 'POST':
        note = request.form.get("note")  # receives input
        if note:
            db_note = Note(
                title=request.form["note"],
                content=request.form["content"],
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            db.session.add(db_note)
            db.session.commit()
        return redirect(url_for('page'))  #refresh
    
    search = request.args.get("search")  #receives input
    matched_notes = []
    if search:
        matched_notes = [
            note for note in notes
            if search.lower() in note.content.lower()
            or any(search.lower() in comment.lower() for comment in json.loads(note.comments)) #check matched notes
        ]
    return render_template('base.html', notes=notes, matched_notes=matched_notes)  #pass to template


@app.route('/note/<mn>', methods=['GET', 'POST'])
def notepage(mn):
    note = Note.query.filter(Note.title == mn).first() #get note with specified title
    if note:
        action = request.form.get("action")
        comments_list = json.loads(note.comments)
        timestamps_list = json.loads(note.comment_timestamps)
        comments_with_timestamps = list(zip(comments_list, timestamps_list))

        if action == "home":
            return redirect("/")
        
        if action == "comment":
            comment = request.form.get("comment")
            note.add_comment(comment)
            db.session.commit()

            comments_list = json.loads(note.comments)
            timestamps_list = json.loads(note.comment_timestamps)
            comments_with_timestamps = list(zip(comments_list, timestamps_list))
            return render_template('note.html', title=note.title, content=note.content, note_date=note.timestamp, comments=comments_with_timestamps)
        
        if action == "delete":
            db.session.delete(note)
            db.session.commit()
            return redirect("/")
        
        return render_template('note.html', title=note.title, content=note.content, note_date=note.timestamp, comments=comments_with_timestamps)
    return "Note not found", 404


if __name__ == "__main__":
   app.run(host='0.0.0.0', port=5000)