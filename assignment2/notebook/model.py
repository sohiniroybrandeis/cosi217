import json
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class Note(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)  # unique ID
    title: Mapped[str] = mapped_column(unique=True, nullable=False)  # note title
    content: Mapped[str] = mapped_column(nullable=False)  # note content
    comments: Mapped[str] = mapped_column(default="[]")  # comments stored as JSON string
    timestamp: Mapped[str] = mapped_column(nullable=False)  # note timestamp
    comment_timestamps: Mapped[str] = mapped_column(default="[]")  # comment timestamps stored as JSON string

    def add_comment(self, comment):
        """Adds a comment along with its timestamp."""
        if not self.timestamp:
            self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # check timestamp exists

        # load existing comments and timestamps
        comments_list = json.loads(self.comments or "[]")
        timestamps_list = json.loads(self.comment_timestamps or "[]")

        comments_list.append(comment)
        timestamps_list.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        self.comments = json.dumps(comments_list)
        self.comment_timestamps = json.dumps(timestamps_list)
