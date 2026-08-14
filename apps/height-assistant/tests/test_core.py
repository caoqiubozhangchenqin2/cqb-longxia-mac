import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from database import HeightDatabase
from standards import age_years, evaluate_height, midparental_target_height

class CoreTests(unittest.TestCase):
    def test_multiple_children_and_medications(self):
        with tempfile.TemporaryDirectory() as folder:
            db = HeightDatabase(Path(folder) / "data")
            ids = [db.save_child({"name": f"孩子{i}", "nickname": "", "gender": "男", "birth_date": "2020-01-01",
                                  "father_height": None, "mother_height": None, "focus": ""}) for i in range(4)]
            self.assertEqual(len(db.children()), 4)
            for name in ("药品A", "药品B", "药品C"):
                med_id = db.get_or_create_medication(ids[0], name)
                db.add_medication_period(med_id, "2026-01-01")
            self.assertEqual(len(db.active_medications(ids[0], "2026-02-01")), 3)

    def test_archive_and_restore_child_preserves_all_data(self):
        with tempfile.TemporaryDirectory() as folder:
            db = HeightDatabase(Path(folder) / "data")
            child_id = db.save_child({"name": "归档测试", "nickname": "", "gender": "女",
                                      "birth_date": "2020-01-01", "father_height": None,
                                      "mother_height": None, "focus": ""})
            db.add_measurement(child_id, "2026-01-01", 118.5, 42.0, notes="重要原始记录")
            med_id = db.get_or_create_medication(child_id, "测试药品")
            db.add_medication_period(med_id, "2026-01-01")
            self.assertEqual(db.child_summary(child_id), {"measurements": 1, "medications": 1, "periods": 1})

            db.archive_child(child_id)
            self.assertEqual(len(db.children()), 0)
            self.assertEqual(len(db.children(include_archived=True)), 1)
            self.assertEqual(len(db.measurements(child_id)), 1)
            self.assertEqual(len(db.medication_periods(child_id)), 1)

            db.restore_child(child_id)
            self.assertEqual(len(db.children()), 1)
            self.assertEqual(db.measurements(child_id)[0]["notes"], "重要原始记录")

    def test_reference_evaluation(self):
        self.assertAlmostEqual(age_years("2016-04-03", "2026-04-03"), 10, places=2)
        label, median = evaluate_height("男", 10, 140.76)
        self.assertEqual(label, "正常范围")
        self.assertEqual(median, 140.76)

    def test_midparental_target_height(self):
        self.assertEqual(midparental_target_height("男", 175, 160), (174.0, 163.8, 184.2))
        self.assertEqual(midparental_target_height("女", 175, 160), (161.0, 150.8, 171.2))
        self.assertIsNone(midparental_target_height("男", None, 160))
        self.assertIsNone(midparental_target_height("女", 175, 0))

    def test_user_selected_backup(self):
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder)
            db = HeightDatabase(base / "data")
            db.save_child({"name": "备份测试", "nickname": "", "gender": "女", "birth_date": "2020-01-01",
                           "father_height": None, "mother_height": None, "focus": ""})
            chosen = base / "customer-choice" / "my-backup.db"
            db.backup_to(chosen)
            self.assertTrue(chosen.exists())
            self.assertEqual(db.validate_backup(chosen), (True, "ok"))
            db.save_child({"name": "备份后新增", "nickname": "", "gender": "男", "birth_date": "2021-01-01",
                           "father_height": None, "mother_height": None, "focus": ""})
            self.assertEqual(len(db.children()), 2)
            db.restore_from(chosen)
            self.assertEqual(len(db.children()), 1)

    def test_edit_and_restore_measurement(self):
        with tempfile.TemporaryDirectory() as folder:
            db = HeightDatabase(Path(folder) / "data")
            child_id = db.save_child({"name": "编辑测试", "nickname": "", "gender": "男", "birth_date": "2016-01-01",
                                      "father_height": None, "mother_height": None, "focus": ""})
            measurement_id = db.add_measurement(child_id, "2026-01-01", 130.0, 60.0, notes="原备注")
            old = db.update_measurement(measurement_id, {"measured_at": "2026-01-01", "height_cm": 130.2,
                                                         "weight_jin": 60.0, "method": "家中测量",
                                                         "notes": "修改后的较长备注", "needs_recheck": True})
            self.assertEqual(db.measurement(measurement_id)["notes"], "修改后的较长备注")
            db.restore_measurement(old)
            self.assertEqual(db.measurement(measurement_id)["notes"], "原备注")


if __name__ == "__main__":
    unittest.main()
