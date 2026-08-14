from __future__ import annotations

import json
import shutil
import sqlite3
from contextlib import contextmanager
from datetime import date, datetime
from pathlib import Path


SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS children (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    nickname TEXT DEFAULT '',
    gender TEXT NOT NULL DEFAULT '男',
    birth_date TEXT NOT NULL,
    father_height REAL,
    mother_height REAL,
    focus TEXT DEFAULT '',
    archived INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS measurements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    child_id INTEGER NOT NULL REFERENCES children(id) ON DELETE RESTRICT,
    measured_at TEXT NOT NULL,
    height_cm REAL NOT NULL,
    weight_jin REAL,
    method TEXT DEFAULT '',
    notes TEXT DEFAULT '',
    needs_recheck INTEGER NOT NULL DEFAULT 0,
    archived INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(child_id, measured_at, height_cm)
);

CREATE TABLE IF NOT EXISTS medications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    child_id INTEGER NOT NULL REFERENCES children(id) ON DELETE RESTRICT,
    name TEXT NOT NULL,
    default_unit TEXT DEFAULT '',
    route TEXT DEFAULT '',
    prescriber TEXT DEFAULT '',
    notes TEXT DEFAULT '',
    archived INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(child_id, name)
);

CREATE TABLE IF NOT EXISTS medication_periods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    medication_id INTEGER NOT NULL REFERENCES medications(id) ON DELETE RESTRICT,
    start_date TEXT NOT NULL,
    end_date TEXT,
    status TEXT NOT NULL DEFAULT '使用中',
    dose REAL,
    unit TEXT DEFAULT '',
    frequency TEXT DEFAULT '',
    route TEXT DEFAULT '',
    prescriber TEXT DEFAULT '',
    notes TEXT DEFAULT '',
    needs_confirmation INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS measurement_medications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    measurement_id INTEGER NOT NULL REFERENCES measurements(id) ON DELETE CASCADE,
    medication_id INTEGER REFERENCES medications(id) ON DELETE SET NULL,
    snapshot_name TEXT NOT NULL,
    dose REAL,
    unit TEXT DEFAULT '',
    frequency TEXT DEFAULT '',
    status TEXT DEFAULT '',
    UNIQUE(measurement_id, snapshot_name)
);

CREATE TABLE IF NOT EXISTS app_settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
"""


class HeightDatabase:
    def __init__(self, data_dir: str | Path):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.data_dir / "height_assistant.db"
        self.backup_dir = self.data_dir.parent / "backup"
        self.export_dir = self.data_dir.parent / "exports"
        self.export_dir.mkdir(parents=True, exist_ok=True)
        self.initialize()

    @contextmanager
    def connect(self):
        con = sqlite3.connect(self.db_path)
        con.row_factory = sqlite3.Row
        con.execute("PRAGMA foreign_keys = ON")
        try:
            yield con
            con.commit()
        except Exception:
            con.rollback()
            raise
        finally:
            con.close()

    def initialize(self):
        with self.connect() as con:
            con.executescript(SCHEMA)
            columns = {row["name"] for row in con.execute("PRAGMA table_info(measurements)")}
            if "archived" not in columns:
                con.execute("ALTER TABLE measurements ADD COLUMN archived INTEGER NOT NULL DEFAULT 0")

    def children(self, include_archived=False):
        query = "SELECT * FROM children"
        if not include_archived:
            query += " WHERE archived=0"
        query += " ORDER BY id"
        with self.connect() as con:
            return [dict(row) for row in con.execute(query)]

    def child(self, child_id: int):
        with self.connect() as con:
            row = con.execute("SELECT * FROM children WHERE id=?", (child_id,)).fetchone()
            return dict(row) if row else None

    def find_child(self, name: str):
        with self.connect() as con:
            row = con.execute("SELECT * FROM children WHERE name=?", (name,)).fetchone()
            return dict(row) if row else None

    def save_child(self, values: dict, child_id: int | None = None):
        fields = ("name", "nickname", "gender", "birth_date", "father_height", "mother_height", "focus")
        data = [values.get(field) for field in fields]
        with self.connect() as con:
            if child_id:
                assignments = ",".join(f"{field}=?" for field in fields)
                con.execute(
                    f"UPDATE children SET {assignments}, updated_at=CURRENT_TIMESTAMP WHERE id=?",
                    (*data, child_id),
                )
                return child_id
            cur = con.execute(
                f"INSERT INTO children ({','.join(fields)}) VALUES ({','.join('?' for _ in fields)})",
                data,
            )
            return cur.lastrowid

    def archive_child(self, child_id: int):
        with self.connect() as con:
            con.execute("UPDATE children SET archived=1, updated_at=CURRENT_TIMESTAMP WHERE id=?", (child_id,))

    def restore_child(self, child_id: int):
        with self.connect() as con:
            con.execute("UPDATE children SET archived=0, updated_at=CURRENT_TIMESTAMP WHERE id=?", (child_id,))

    def child_summary(self, child_id: int):
        """Return counts used by the archive confirmation and archived-child view."""
        with self.connect() as con:
            measurements = con.execute(
                "SELECT COUNT(*) FROM measurements WHERE child_id=?",
                (child_id,),
            ).fetchone()[0]
            medications = con.execute(
                "SELECT COUNT(*) FROM medications WHERE child_id=?",
                (child_id,),
            ).fetchone()[0]
            periods = con.execute(
                """SELECT COUNT(*) FROM medication_periods p
                   JOIN medications m ON m.id=p.medication_id
                   WHERE m.child_id=?""",
                (child_id,),
            ).fetchone()[0]
        return {"measurements": measurements, "medications": medications, "periods": periods}

    def measurements(self, child_id: int, descending=False):
        order = "DESC" if descending else "ASC"
        with self.connect() as con:
            rows = con.execute(
                f"SELECT * FROM measurements WHERE child_id=? AND archived=0 ORDER BY measured_at {order}, id {order}",
                (child_id,),
            )
            return [dict(row) for row in rows]

    def measurement(self, measurement_id: int):
        with self.connect() as con:
            row = con.execute("SELECT * FROM measurements WHERE id=?", (measurement_id,)).fetchone()
            return dict(row) if row else None

    def update_measurement(self, measurement_id: int, values: dict):
        old = self.measurement(measurement_id)
        if not old:
            raise ValueError("找不到要修改的记录。")
        try:
            with self.connect() as con:
                con.execute(
                    """UPDATE measurements SET measured_at=?, height_cm=?, weight_jin=?, method=?,
                       notes=?, needs_recheck=?, updated_at=CURRENT_TIMESTAMP WHERE id=?""",
                    (values["measured_at"], values["height_cm"], values.get("weight_jin"),
                     values.get("method", ""), values.get("notes", ""),
                     int(values.get("needs_recheck", False)), measurement_id),
                )
        except sqlite3.IntegrityError as exc:
            raise ValueError("同一孩子在该日期已经存在相同身高的记录，请检查后再保存。") from exc
        return old

    def restore_measurement(self, snapshot: dict):
        return self.update_measurement(snapshot["id"], snapshot)

    def add_measurement(self, child_id: int, measured_at: str, height_cm: float,
                        weight_jin: float | None = None, method: str = "",
                        notes: str = "", needs_recheck: bool = False,
                        medication_snapshots: list[dict] | None = None):
        with self.connect() as con:
            cur = con.execute(
                """INSERT OR IGNORE INTO measurements
                   (child_id, measured_at, height_cm, weight_jin, method, notes, needs_recheck)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (child_id, measured_at, height_cm, weight_jin, method, notes, int(needs_recheck)),
            )
            if cur.lastrowid:
                measurement_id = cur.lastrowid
            else:
                row = con.execute(
                    "SELECT id FROM measurements WHERE child_id=? AND measured_at=? AND height_cm=?",
                    (child_id, measured_at, height_cm),
                ).fetchone()
                measurement_id = row["id"]
            for snapshot in medication_snapshots or []:
                con.execute(
                    """INSERT OR REPLACE INTO measurement_medications
                       (measurement_id, medication_id, snapshot_name, dose, unit, frequency, status)
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (measurement_id, snapshot.get("medication_id"), snapshot["name"], snapshot.get("dose"),
                     snapshot.get("unit", ""), snapshot.get("frequency", ""), snapshot.get("status", "")),
                )
            return measurement_id

    def delete_measurement(self, measurement_id: int):
        with self.connect() as con:
            con.execute("UPDATE measurements SET archived=1, updated_at=CURRENT_TIMESTAMP WHERE id=?", (measurement_id,))

    def medications(self, child_id: int, include_archived=False):
        query = "SELECT * FROM medications WHERE child_id=?"
        args = [child_id]
        if not include_archived:
            query += " AND archived=0"
        query += " ORDER BY archived, name"
        with self.connect() as con:
            return [dict(row) for row in con.execute(query, args)]

    def get_or_create_medication(self, child_id: int, name: str, **defaults):
        name = name.strip()
        with self.connect() as con:
            row = con.execute("SELECT id FROM medications WHERE child_id=? AND name=?", (child_id, name)).fetchone()
            if row:
                return row["id"]
            cur = con.execute(
                """INSERT INTO medications (child_id, name, default_unit, route, prescriber, notes)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (child_id, name, defaults.get("default_unit", ""), defaults.get("route", ""),
                 defaults.get("prescriber", ""), defaults.get("notes", "")),
            )
            return cur.lastrowid

    def add_medication_period(self, medication_id: int, start_date: str, end_date: str | None = None,
                              status: str = "使用中", dose: float | None = None, unit: str = "",
                              frequency: str = "", route: str = "", prescriber: str = "",
                              notes: str = "", needs_confirmation: bool = False):
        with self.connect() as con:
            existing = con.execute(
                "SELECT id FROM medication_periods WHERE medication_id=? AND start_date=? AND COALESCE(end_date,'')=COALESCE(?,'')",
                (medication_id, start_date, end_date),
            ).fetchone()
            if existing:
                return existing["id"]
            cur = con.execute(
                """INSERT INTO medication_periods
                   (medication_id, start_date, end_date, status, dose, unit, frequency, route,
                    prescriber, notes, needs_confirmation)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (medication_id, start_date, end_date, status, dose, unit, frequency, route,
                 prescriber, notes, int(needs_confirmation)),
            )
            return cur.lastrowid

    def medication_periods(self, child_id: int):
        with self.connect() as con:
            rows = con.execute(
                """SELECT p.*, m.name AS medication_name, m.archived
                   FROM medication_periods p JOIN medications m ON m.id=p.medication_id
                   WHERE m.child_id=? ORDER BY p.start_date, p.id""",
                (child_id,),
            )
            return [dict(row) for row in rows]

    def active_medications(self, child_id: int, on_date: str):
        with self.connect() as con:
            rows = con.execute(
                """SELECT p.*, m.name AS medication_name
                   FROM medication_periods p JOIN medications m ON m.id=p.medication_id
                   WHERE m.child_id=? AND m.archived=0 AND p.start_date<=?
                     AND (p.end_date IS NULL OR p.end_date='' OR p.end_date>=?)
                     AND p.status NOT IN ('已停用','已结束')
                   ORDER BY m.name""",
                (child_id, on_date, on_date),
            )
            return [dict(row) for row in rows]

    def measurement_medications(self, measurement_id: int):
        with self.connect() as con:
            rows = con.execute(
                "SELECT * FROM measurement_medications WHERE measurement_id=? ORDER BY snapshot_name",
                (measurement_id,),
            )
            return [dict(row) for row in rows]

    def archive_medication(self, medication_id: int):
        with self.connect() as con:
            con.execute("UPDATE medications SET archived=1 WHERE id=?", (medication_id,))

    def setting(self, key: str, default=None):
        with self.connect() as con:
            row = con.execute("SELECT value FROM app_settings WHERE key=?", (key,)).fetchone()
            if not row:
                return default
            try:
                return json.loads(row["value"])
            except json.JSONDecodeError:
                return row["value"]

    def set_setting(self, key: str, value):
        with self.connect() as con:
            con.execute(
                "INSERT INTO app_settings(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                (key, json.dumps(value, ensure_ascii=False)),
            )

    def create_backup(self, keep=30):
        if not self.db_path.exists():
            return None
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        target = self.backup_dir / f"height_assistant-{stamp}.db"
        shutil.copy2(self.db_path, target)
        backups = sorted(self.backup_dir.glob("height_assistant-*.db"), reverse=True)
        for old in backups[keep:]:
            old.unlink(missing_ok=True)
        return target

    def backup_to(self, target: str | Path):
        """Create a consistent SQLite backup at the location explicitly chosen by the user."""
        target = Path(target)
        if target.resolve() == self.db_path.resolve():
            raise ValueError("不能把备份保存为当前正在使用的数据库文件。")
        target.parent.mkdir(parents=True, exist_ok=True)
        source = sqlite3.connect(self.db_path)
        destination = sqlite3.connect(target)
        try:
            source.backup(destination)
        finally:
            destination.close()
            source.close()
        return target

    @staticmethod
    def validate_backup(path: str | Path):
        required = {"children", "measurements", "medications", "medication_periods", "app_settings"}
        path = Path(path)
        if not path.is_file():
            return False, "备份文件不存在。"
        try:
            con = sqlite3.connect(f"file:{path.as_posix()}?mode=ro", uri=True)
            integrity = con.execute("PRAGMA integrity_check").fetchone()[0]
            tables = {row[0] for row in con.execute("SELECT name FROM sqlite_master WHERE type='table'")}
            con.close()
        except sqlite3.Error as exc:
            return False, f"无法读取备份：{exc}"
        if integrity != "ok":
            return False, f"备份完整性检查失败：{integrity}"
        missing = required - tables
        if missing:
            return False, "不是有效的身高小助理备份。"
        return True, "ok"

    def restore_from(self, source: str | Path):
        valid, message = self.validate_backup(source)
        if not valid:
            raise ValueError(message)
        shutil.copy2(Path(source), self.db_path)
        self.initialize()

    def summary(self, child_id: int):
        rows = self.measurements(child_id)
        if not rows:
            return {"count": 0, "latest": None, "growth": None, "days": None}
        latest = rows[-1]
        first = rows[0]
        days = (date.fromisoformat(latest["measured_at"]) - date.fromisoformat(first["measured_at"])).days
        return {
            "count": len(rows),
            "latest": latest,
            "growth": round(latest["height_cm"] - first["height_cm"], 1),
            "days": days,
        }
