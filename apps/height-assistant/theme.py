APP_STYLE = r"""
* { font-family: "Microsoft YaHei UI", "Microsoft YaHei"; font-size: 14px; color: #20313A; }
QMainWindow { background: #F4F8FA; }
QWidget#AppRoot { background: transparent; }
QFrame#Sidebar { background: #123C4A; border: none; }
QLabel#Brand { color: white; font-size: 20px; font-weight: 700; padding: 0; }
QLabel#BrandSub { color: #B9D8DD; font-size: 12px; }
QPushButton#NavButton { color: #D7E9EC; background: transparent; border: none; border-radius: 10px; padding: 12px 16px; text-align: left; font-size: 15px; }
QPushButton#NavButton:hover { background: #1B5361; color: white; }
QPushButton#NavButton:checked { background: #E7F7F4; color: #126A68; font-weight: 700; }
QFrame#TopBar { background: rgba(255,255,255,245); border-bottom: 1px solid #E3ECEF; }
QLabel#PageTitle { font-size: 23px; font-weight: 700; color: #163C48; }
QLabel#PageHint { color: #71838B; }
QFrame#Card, QGroupBox { background: rgba(255,255,255,246); border: 1px solid #DCE9EC; border-radius: 14px; }
QFrame#InfoPanel { background: rgba(232,247,243,235); border: 1px solid #C8E6E1; border-radius: 12px; }
QGroupBox { margin-top: 14px; padding: 18px 12px 12px 12px; font-weight: 700; color: #244A55; }
QGroupBox::title { subcontrol-origin: margin; left: 14px; padding: 0 6px; }
QLabel#CardTitle { color: #72858C; font-size: 13px; }
QLabel#CardValue { color: #123C4A; font-size: 25px; font-weight: 700; }
QLabel#AccentValue { color: #16877F; font-size: 25px; font-weight: 700; }
QLabel#Muted { color: #7B8D94; }
QLabel#Badge { background: #E8F7F3; color: #13776F; border-radius: 10px; padding: 4px 9px; font-weight: 700; }
QLabel#ArchiveBadge { background: #FFF2E2; color: #A55A12; border: 1px solid #F0D2A8; border-radius: 10px; padding: 4px 9px; font-weight: 700; }
QLabel#QrPanel { background: white; border: 1px solid #D8E7E9; border-radius: 16px; padding: 14px; }
QLabel#ChartHelp { background: rgba(232,247,243,235); color: #35626A; border: 1px solid #C7E3DF; border-radius: 8px; padding: 7px 12px; }
QLabel#TargetHelp { background: rgba(245,240,252,238); color: #63458D; border: 1px solid #DDD0EE; border-radius: 8px; padding: 7px 12px; }
QPushButton { background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #F4F9FA,stop:1 #E2EEF0); border: 1px solid #D2E1E4; border-radius: 9px; padding: 9px 16px; color: #28505B; min-height: 18px; }
QPushButton:hover { background: #DDF0EE; border-color: #8CCDC6; color: #126A68; }
QPushButton:pressed { background: #CBE5E1; padding-top: 10px; padding-bottom: 8px; }
QPushButton#Primary { background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #16877F,stop:1 #35A99E); border: 1px solid #16877F; color: white; font-weight: 700; }
QPushButton#Primary:hover { background: #11756F; }
QPushButton#Compact { padding: 7px 11px; min-width: 38px; }
QPushButton#Danger { background: #FFF0EF; color: #B54038; }
QPushButton#Undo { background: #FFF7E8; border: 1px solid #E8C98B; color: #8A5A13; }
QPushButton#Undo:hover { background: #FCEBC9; border-color: #D6AB58; }
QLineEdit, QDateEdit, QDoubleSpinBox, QComboBox, QTextEdit { background: white; border: 1px solid #CBDCDF; border-radius: 8px; padding: 8px; selection-background-color: #72C9C0; }
QComboBox { padding-right: 38px; }
QComboBox::drop-down { subcontrol-origin: padding; subcontrol-position: top right; width: 32px; background: #E1F2F0; border-left: 1px solid #B8D8D7; border-top-right-radius: 7px; border-bottom-right-radius: 7px; }
QComboBox::drop-down:hover { background: #CDE9E5; }
QComboBox::down-arrow { image: url(__COMBO_ARROW__); width: 16px; height: 10px; }
QDateEdit { padding-right: 40px; }
QDateEdit::drop-down { subcontrol-origin: padding; subcontrol-position: top right; width: 34px; background: #E1F2F0; border-left: 1px solid #B8D8D7; border-top-right-radius: 7px; border-bottom-right-radius: 7px; }
QDateEdit::drop-down:hover { background: #CDE9E5; }
QDateEdit::down-arrow { image: url(__CALENDAR_ICON__); width: 18px; height: 18px; }
QDoubleSpinBox { padding-right: 38px; }
QDoubleSpinBox::up-button { subcontrol-origin: border; subcontrol-position: top right; width: 32px; height: 19px; background: #E1F2F0; border-left: 1px solid #B8D8D7; border-bottom: 1px solid #C9E1DF; border-top-right-radius: 7px; }
QDoubleSpinBox::down-button { subcontrol-origin: border; subcontrol-position: bottom right; width: 32px; height: 19px; background: #E1F2F0; border-left: 1px solid #B8D8D7; border-bottom-right-radius: 7px; }
QDoubleSpinBox::up-button:hover, QDoubleSpinBox::down-button:hover { background: #CDE9E5; }
QDoubleSpinBox::up-arrow { image: url(__SPIN_UP__); width: 14px; height: 9px; }
QDoubleSpinBox::down-arrow { image: url(__SPIN_DOWN__); width: 14px; height: 9px; }
QLineEdit:focus, QDateEdit:focus, QDoubleSpinBox:focus, QComboBox:focus, QTextEdit:focus { border: 2px solid #46AEA4; }
QTableWidget { background: white; alternate-background-color: #F7FAFB; border: 1px solid #E0EAED; border-radius: 10px; gridline-color: #E8EFF1; }
QHeaderView::section { background: #EAF3F4; color: #31545E; border: none; border-bottom: 1px solid #D6E4E7; padding: 9px; font-weight: 700; }
QTableWidget::item { padding: 7px; }
QTabWidget::pane { border: 1px solid #DFEAED; background: white; border-radius: 10px; }
QTabBar::tab { background: #EAF2F4; padding: 10px 20px; margin-right: 3px; border-top-left-radius: 8px; border-top-right-radius: 8px; }
QTabBar::tab:selected { background: white; color: #16877F; font-weight: 700; }
QListWidget { background: white; border: 1px solid #DBE7EA; border-radius: 9px; padding: 5px; }
QListWidget::item { padding: 9px; border-radius: 7px; }
QListWidget::item:selected { background: #DFF3F0; color: #116A65; }
QScrollBar:vertical { width: 10px; background: transparent; }
QScrollBar::handle:vertical { background: #BED3D7; border-radius: 5px; min-height: 25px; }
QToolTip { background: #123C4A; color: white; border: 1px solid #4FB9AF; border-radius: 7px; padding: 8px; }
"""
