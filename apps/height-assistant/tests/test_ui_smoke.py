import os
import sys
import tempfile
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from PySide6.QtCharts import QChartView
from PySide6.QtWidgets import QApplication
from database import HeightDatabase
from main import EditMeasurementDialog, MainWindow


class UiSmokeTest(unittest.TestCase):
    def test_window_and_six_pages(self):
        app = QApplication.instance() or QApplication([])
        with tempfile.TemporaryDirectory() as folder:
            db = HeightDatabase(Path(folder) / "data")
            db.save_child({"name": "测试孩子", "nickname": "", "gender": "男", "birth_date": "2016-01-01",
                           "father_height": 175, "mother_height": 160, "focus": ""})
            child = db.find_child("测试孩子")
            db.add_measurement(child["id"], "2025-01-01", 120.0, 45.0)
            last_id = db.add_measurement(child["id"], "2026-01-01", 126.0, 50.0, notes="复查后记录")
            window = MainWindow(db)
            self.assertEqual(window.stack.count(), 6)
            self.assertEqual(window.child_combo.count(), 1)
            home = window.pages[0]
            self.assertGreater(home.layout().indexOf(home.chart_help), home.layout().indexOf(home.chart))
            settings = window.pages[5]
            self.assertEqual(settings.child_filter.count(), 3)
            self.assertEqual(settings.tabs.tabText(settings.tabs.count() - 1), "支持作者")
            self.assertEqual(settings.profile_status.text(), "正在使用")
            db.archive_child(child["id"])
            settings.child_filter.setCurrentIndex(1)
            settings.refresh(child["id"])
            self.assertEqual(settings.profile_status.text(), "已归档")
            self.assertFalse(settings.restore_button.isHidden())
            self.assertTrue(settings.save_button.isHidden())
            db.restore_child(child["id"])
            settings.child_filter.setCurrentIndex(0)
            settings.refresh(child["id"])
            history = window.pages[2]
            history.sort_order.setCurrentIndex(0)
            self.assertEqual(history.table.item(0, 0).text(), "2026-01-01")
            history.sort_order.setCurrentIndex(1)
            self.assertEqual(history.table.item(0, 0).text(), "2025-01-01")
            charts = window.pages[3]
            self.assertGreater(charts.layout().indexOf(charts.chart_help), charts.layout().indexOf(charts.chart))
            charts.mode.setCurrentIndex(0)
            charts.refresh_current()
            self.assertEqual(len(charts.chart.last_point_details), 2)
            self.assertFalse(any("遗传" in series.name() for series in charts.chart.chart().series()))
            self.assertEqual(charts.target_height_card.value.text(), "174.0 cm")
            self.assertIn("163.8–184.2 cm", charts.target_height_info.text())
            self.assertIn("备注：复查后记录", charts.chart.last_point_details[-1][2])
            self.assertTrue(charts.chart.last_point_details[-1][3])
            for mode_index in range(charts.mode.count()):
                charts.mode.setCurrentIndex(mode_index)
                charts.refresh_current()
                self.assertGreaterEqual(len(charts.chart.last_point_details), 1)
            charts.chart.zoom_in()
            charts.chart.zoom_out()
            charts.chart.reset_zoom()
            self.assertEqual(charts.chart.rubberBand(), QChartView.NoRubberBand)
            edit_dialog = EditMeasurementDialog(db.measurement(last_id), window)
            self.assertGreaterEqual(edit_dialog.notes.minimumHeight(), 190)
            self.assertEqual(edit_dialog.values()["notes"], "复查后记录")
            edit_dialog.close()
            window.close()
        app.processEvents()


if __name__ == "__main__":
    unittest.main()
