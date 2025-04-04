from flask import render_template, request, redirect, url_for
from datetime import datetime
import json
from notebook import app, db
from notebook import model

@app.route("/", methods=["GET", "POST"])
def page():
    """Main page that displays notes and handles new note creation."""
    notes = model.Note.query.all()  # Get all notes
    if request.method == "POST":
        note_title = request.form.get("note")  # Receives input
        note_content = request.form.get("content")

        if note_title and note_content:
            db_note = model.Note(
                title=note_title,
                content=note_content,
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )
            db.session.add(db_note)
            db.session.commit()

        return redirect(url_for("page"))  # Refresh page

    # Handle search functionality
    search = request.args.get("search")  # Receives input
    matched_notes = []
    if search:
        matched_notes = [
            note
            for note in notes
            if search.lower() in note.content.lower()
            or any(search.lower() in comment.lower() for comment in json.loads(note.comments))
            or search.lower() in note.title.lower()    # Check matched notes
        ]
    return render_template("base.html", notes=notes, matched_notes=matched_notes)  # Pass to template


@app.route("/note/<mn>", methods=["GET", "POST"])
def notepage(mn):
    """Displays a single note and handles commenting and deletion."""
    note = model.Note.query.filter(model.Note.title == mn).first()  # Get note with specified title

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