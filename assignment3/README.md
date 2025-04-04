### File structure:
- notebook (directory)
  - __init__.py: Initializes Flask app and creates database tables.
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

### To run:

Building the Docker container:
`docker build -t my-flask-app .`

Running the Docker container:
`docker run -p 5000:5000 -v $(pwd)/instance:/app/instance my-flask-app`

If the following error arises on Mac:

`Address already in use`
`Port 5000 is in use by another program. Either identify and stop that program, or start the server with a different port.`
`On macOS, try disabling the 'AirPlay Receiver' service from System Preferences -> General -> AirDrop & Handoff.`

Follow the exact directions listed, and the error should go away. That is to say:
- Disable Airplay Receiver by going to System Preferences -> General -> AirDrop & Handoff.
