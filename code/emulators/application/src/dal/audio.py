from common.structs import AudioRecord
import sqlite3
import os

DB_FILE_PATH = os.path.join(os.path.dirname(__file__), "audio_records.db")


class AudioRecordRepository:
    def __init__(self):
        self.conn = sqlite3.connect(DB_FILE_PATH)
        self.c = self.conn.cursor()
        self.c.execute(
            """CREATE TABLE IF NOT EXISTS audio_records
             (id INTEGER PRIMARY KEY AUTOINCREMENT, name text, timestamp integer, audio_data blob)"""
        )
        self.conn.commit()

    def store_record(self, record: AudioRecord) -> None:
        self.c.execute(
            "INSERT INTO audio_records (name, timestamp, audio_data) VALUES (?, ?, ?)",
            (record.name, record.timestamp, record.audio_data),
        )
        self.conn.commit()

    def get_records(self) -> list[AudioRecord]:
        self.c.execute("SELECT id, name, timestamp, audio_data FROM audio_records")
        return [
            AudioRecord(id=row[0], name=row[1], timestamp=row[2], audio_data=row[3])
            for row in self.c.fetchall()
        ]

    def get_record(self, record_id: int) -> AudioRecord:
        self.c.execute(
            "SELECT id, name, timestamp, audio_data FROM audio_records WHERE id=?",
            (record_id,),
        )
        audio_record = self.c.fetchone()
        return AudioRecord(
            id=audio_record[0],
            name=audio_record[1],
            timestamp=audio_record[2],
            audio_data=audio_record[3],
        )

    def update_record_name(self, record: AudioRecord) -> None:
        self.c.execute(
            "UPDATE audio_records SET name=? WHERE id=?",
            (
                record.name,
                record.id,
            ),
        )
        self.conn.commit()

    def delete_record(self, record: AudioRecord) -> None:
        self.c.execute("DELETE FROM audio_records WHERE id=?", (record.id,))
        self.conn.commit()
