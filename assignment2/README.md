### File structure:
- notebook (directory)
  - model.py: Database model logic.
  - routes.py: Flask application that can opens up a website to create, add, delete, or search for a note, as well as display and comment on them.
  - static (directory)
    -   styles.css: CSS styles for Flask application.
    -   toggle.js: Javascript code for toggling buttons
  - templates (directory)
    - base.html: Base HTML file for website
    - note.html: HTML file to display webpage with individual note, extends Base file.
   
- instance (directory)
  - db.sqlite: Database file for writing all notes to.
- requirements.txt
- run.py: Runs Flask app

To run:

`python run.py`
