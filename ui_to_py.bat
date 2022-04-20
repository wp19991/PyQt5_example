call C:\DevelopmentTools\Miniconda3\miniconda3\Scripts\activate.bat C:\DevelopmentTools\Miniconda3\miniconda3\envs\learn_pyqt5
pyrcc5 res/app.qrc -o res/app_rc.py
python -m PyQt5.uic.pyuic ui/main_window.ui -o ui/main_window.py --import-from=res
python -m PyQt5.uic.pyuic ui/login_form.ui -o ui/login_form.py --import-from=res
python -m PyQt5.uic.pyuic ui/close_dialog.ui -o ui/close_dialog.py --import-from=res