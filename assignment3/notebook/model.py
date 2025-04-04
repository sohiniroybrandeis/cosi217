import json
from datetime import datetime
from notebook import db
from sqlalchemy.orm import Mapped, mapped_column


class Note(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)  # Unique ID
    title: Mapped[str] = mapped_column(unique=True, nullable=False)  # Note title
    content: Mapped[str] = mapped_column(nullable=False)  # Note content
    comments: Mapped[str] = mapped_column(default="[]")  # Comments stored as JSON string
    timestamp: Mapped[str] = mapped_column(nullable=False)  # Note timestamp
    comment_timestamps: Mapped[str] = mapped_column(default="[]")  # Comment timestamps stored as JSON string

    def add_comment(self, comment):
        """Adds a comment along with its timestamp."""
        if not self.timestamp:
            self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Ensure timestamp exists

        # Load existing comments and timestamps
        comments_list = json.loads(self.comments or "[]")
        timestamps_list = json.loads(self.comment_timestamps or "[]")

        comments_list.append(comment)
        timestamps_list.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        self.comments = json.dumps(comments_list)
        self.comment_timestamps = json.dumps(timestamps_list)