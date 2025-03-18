from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import json

from model import db, Note

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:////Users/sohiniroy/Documents/cosi217/HW1/instance/db.sqlite"
)
db.init_app(app)  # configure Flask with SQLAlchemy

with app.app_context():
    db.create_all()  # create tables


@app.route("/", methods=["GET", "POST"])
def page():
    """Main page that displays notes and handles new note creation."""
    notes = Note.query.all()  # get all notes
    if request.method == "POST":
        note_title = request.form.get("note")  # receives input
        note_content = request.form.get("content")

        if note_title and note_content:
            db_note = Note(
                title=note_title,
                content=note_content,
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )
            db.session.add(db_note)
            db.session.commit()

        return redirect(url_for("page"))  # refresh page

    search = request.args.get("search")  # receives input
    matched_notes = []
    if search:
        matched_notes = [
            note
            for note in notes
            if search.lower() in note.content.lower()
            or any(search.lower() in comment.lower() for comment in json.loads(note.comments))  # check matched notes
        ]
    return render_template("base.html", notes=notes, matched_notes=matched_notes)  # pass to template


@app.route("/note/<mn>", methods=["GET", "POST"])
def notepage(mn):
    """Displays a single note and handles commenting and deletion."""
    note = Note.query.filter(Note.title == mn).first()  # get note with specified title

    if note:
        action = request.form.get("action")
        comments_list = json.loads(note.comments)
        timestamps_list = json.loads(note.comment_timestamps)
        comments_with_timestamps = list(zip(comments_list, timestamps_list))

        if action == "home":
            return redirect("/")

        if action == "comment":
            comment = request.form.get("comment")
            if comment:
                note.add_comment(comment)
                db.session.commit()

            comments_list = json.loads(note.comments)
            timestamps_list = json.loads(note.comment_timestamps)
            comments_with_timestamps = list(zip(comments_list, timestamps_list))

            return render_template(
                "note.html",
                title=note.title,
                content=note.content,
                note_date=note.timestamp,
                comments=comments_with_timestamps,
            )

        if action == "delete":
            db.session.delete(note)
            db.session.commit()
            return redirect("/")

        return render_template(
            "note.html",
            title=note.title,
            content=note.content,
            note_date=note.timestamp,
            comments=comments_with_timestamps,
        )

    return "Note not found", 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
