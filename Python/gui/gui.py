import os, webbrowser, sys
import PySimpleGUI as sg

from pathlib import Path
from threading import Thread

import Python.convert as convert
from Python import shared_globals as cfg
from Python import warnings

from PySide6.QtCore import (
    QCoreApplication,
    QMetaObject,
    QObject,
    QSize,
    Qt,
    QThread,
    QThreadPool,
    Signal,
    Slot,
)
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QErrorMessage,
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from Python.settings import Settings

SETTINGS = {}
APP = None
WINDOW = None


class ManuallyCreatedInstance(Exception):
    def __init__(self):
        super("Get the window using Window.get_instance!")

class ConverterConnection(QObject):
    set_progress = Signal(int)
    set_progress_max = Signal(int)
    update_text = Signal(str)
    error_msg = Signal(str)

class ConvertWorker(QObject):
    started = Signal()
    finished = Signal()
    
    @Slot()
    def run(self):
        t = Thread(target=convert.convert_all)
        t.start()
        # convert.convert_all()
        

class ConverterWindow(QMainWindow):
    
    SINGLETON = None
    connection = ConverterConnection()

    def __init__(self, parent=None):
        super().__init__(parent)
        if ConverterWindow.SINGLETON:
            raise ManuallyCreatedInstance()
        ConverterWindow.SINGLETON = self
        self.connection = ConverterConnection()
        self.init_ui()
        if (sys.platform == "win32"):
            self.activateWindow()
        else:
            self.raise_()
        self.thread_manager = QThreadPool()

    @classmethod
    def get_instance(cls, parent=None):
        if not ConverterWindow.SINGLETON:
            return ConverterWindow(parent)
        else:
            return ConverterWindow.SINGLETON

    def convert_button_click(self):
        self.run_convert()

    def run_convert(self):
        self.lock_convert_button()
        self.worker = ConvertWorker()
        self.worker.finished.connect(self.convert_finished)

        self.worker.run()
        
        # self.worker.moveToThread(self.workerThread)
        # self.workerThread.started.connect(self.worker.run)
        # self.worker.started.connect(self.worker.started)
        # self.worker.finished.connect(self.workerThread.quit)
        # self.workerThread.finished.connect(self.workerThread.deleteLater)
        # self.workerThread.start()

    def convert_finished(self):
        self.unlock_convert_button()
        self.set_status_message("Done!")
        pass

    # def run_safely(self, func):
    #     self.thread_manager.start(func)

    def disable_progress_bar(self):
        self.window.progress_bar.setEnabled(False)

    def enable_progress_bar(self):
        self.window.progress_bar.setEnabled(True)

    def unlock_convert_button(self):
        # gui_windows.get_main_window()["CONVERT"].update(disabled=False)
        self.convert_button.setEnabled(True)

    def lock_convert_button(self):
        # gui_windows.get_main_window()["CONVERT"].update(disabled=True)
        self.convert_button.setEnabled(False)
    
    def show_error_message(self, msg: str):
        e = QErrorMessage(self)
        e.setFixedSize(QSize(380, 260))
        e.showMessage(msg.replace('\n', '<br>'))

    def init_ui(self):
        self.setupUi()
        # window icon
        p = Path("Media/legacy-mod-converter.ico").resolve()
        icon = QIcon(str(p))
        self.setWindowIcon(icon)

        # init convert button
        button = self.convert_button
        button.clicked.connect(self.convert_button_click)

        # init progress bar

        # init checkboxes
        self.init_checkboxes()
        # init file pickers
        self.init_file_buttons()

        self.try_enable_convert()

        self.connection.set_progress.connect(self.convert_progress_bar.setValue)
        self.connection.set_progress_max.connect(
            self.convert_progress_bar.setMaximum
        )
        self.connection.update_text.connect(self.set_status_message)
        self.connection.error_msg.connect(self.show_error_message)

    def init_checkboxes(self):
        s = Settings.get()
        for key, val in s.items():
            if not hasattr(self, key):
                continue
            cbox = getattr(self, key)

            if type(cbox) == QCheckBox:
                if val:
                    cbox.setCheckState(Qt.CheckState.Checked)
                cbox.stateChanged.connect(lambda x, b=cbox: checkbox_handler(b, x))

    def init_file_buttons(self):
        buttons = [self.input_folder_picker, self.output_folder_picker]

        # setup file button handlers
        for button in buttons:
            button.clicked.connect(
                # For some reason, this lambda only works if there are two variables,
                # and both are assigned "button"
                lambda x=button, b=button: file_button_handler(x)
                )

        # fix labels
        in_loc, out_loc = Settings.get(["input_folder", "output_folder"])

        self.input_folder_label.setText(in_loc if in_loc else "No folder specified.")
        self.output_folder_label.setText(out_loc if out_loc else "No folder specified.")

    def set_status_message(self, msg: str):
        self.statusLabel.setText(msg)

    def try_enable_convert(self):
        if should_enable_convert():
            self.unlock_convert_button()

    def setupUi(self):
        if not self.objectName():
            self.setObjectName(u"MainWindow")
        self.resize(563, 213)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setAcceptDrops(True)
        icon = QIcon()
        icon.addFile(u":/icon/legacy-mod-converter.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        self.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.setAnimated(False)
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy1)
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(18, 9, 18, 9)
        self.options_layout = QHBoxLayout()
        self.options_layout.setObjectName(u"options_layout")
        self.folders_box = QGroupBox(self.centralwidget)
        self.folders_box.setObjectName(u"folders_box")
        self.verticalLayout_3 = QVBoxLayout(self.folders_box)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.input_layout = QHBoxLayout()
        self.input_layout.setObjectName(u"input_layout")
        self.input_folder_picker = QPushButton(self.folders_box)
        self.input_folder_picker.setObjectName(u"input_folder_picker")
        sizePolicy2 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.input_folder_picker.sizePolicy().hasHeightForWidth())
        self.input_folder_picker.setSizePolicy(sizePolicy2)
        self.input_folder_picker.setMinimumSize(QSize(120, 0))

        self.input_layout.addWidget(self.input_folder_picker)

        self.input_folder_label = QLineEdit(self.folders_box)
        self.input_folder_label.setObjectName(u"input_folder_label")
        self.input_folder_label.setEnabled(False)
        self.input_folder_label.setDragEnabled(True)

        self.input_layout.addWidget(self.input_folder_label)


        self.verticalLayout_3.addLayout(self.input_layout)

        self.output_layout = QHBoxLayout()
        self.output_layout.setObjectName(u"output_layout")
        self.output_folder_picker = QPushButton(self.folders_box)
        self.output_folder_picker.setObjectName(u"output_folder_picker")
        sizePolicy2.setHeightForWidth(self.output_folder_picker.sizePolicy().hasHeightForWidth())
        self.output_folder_picker.setSizePolicy(sizePolicy2)
        self.output_folder_picker.setMinimumSize(QSize(120, 0))

        self.output_layout.addWidget(self.output_folder_picker)

        self.output_folder_label = QLineEdit(self.folders_box)
        self.output_folder_label.setObjectName(u"output_folder_label")
        self.output_folder_label.setEnabled(False)
        self.output_folder_label.setDragEnabled(True)

        self.output_layout.addWidget(self.output_folder_label)


        self.verticalLayout_3.addLayout(self.output_layout)


        self.options_layout.addWidget(self.folders_box)

        self.settings_box = QGroupBox(self.centralwidget)
        self.settings_box.setObjectName(u"settings_box")
        self.settings_box.setMaximumSize(QSize(200, 16777215))
        self.verticalLayout_4 = QVBoxLayout(self.settings_box)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.output_zips = QCheckBox(self.settings_box)
        self.output_zips.setObjectName(u"output_zips")

        self.verticalLayout_4.addWidget(self.output_zips)

        self.play_finish_sound = QCheckBox(self.settings_box)
        self.play_finish_sound.setObjectName(u"play_finish_sound")

        self.verticalLayout_4.addWidget(self.play_finish_sound)

        self.skip_convert = QCheckBox(self.settings_box)
        self.skip_convert.setObjectName(u"skip_convert")
        self.skip_convert.setEnabled(True)

        self.verticalLayout_4.addWidget(self.skip_convert)

        self.beautify_lua = QCheckBox(self.settings_box)
        self.beautify_lua.setObjectName(u"beautify_lua")

        self.verticalLayout_4.addWidget(self.beautify_lua)

        self.launch_on_finish = QCheckBox(self.settings_box)
        self.launch_on_finish.setObjectName(u"launch_on_finish")
        self.launch_on_finish.setMouseTracking(False)
        self.launch_on_finish.setFocusPolicy(Qt.NoFocus)

        self.verticalLayout_4.addWidget(self.launch_on_finish)


        self.options_layout.addWidget(self.settings_box)


        self.verticalLayout_2.addLayout(self.options_layout)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.convert_button = QPushButton(self.centralwidget)
        self.convert_button.setObjectName(u"convert_button")
        self.convert_button.setEnabled(False)

        self.horizontalLayout_17.addWidget(self.convert_button)

        self.convert_progress_bar = QProgressBar(self.centralwidget)
        self.convert_progress_bar.setObjectName(u"convert_progress_bar")
        self.convert_progress_bar.setEnabled(True)
        self.convert_progress_bar.setValue(0)
        self.convert_progress_bar.setInvertedAppearance(False)
        self.convert_progress_bar.setTextDirection(QProgressBar.TopToBottom)

        self.horizontalLayout_17.addWidget(self.convert_progress_bar)


        self.verticalLayout_2.addLayout(self.horizontalLayout_17)

        self.statusLabel = QLabel(self.centralwidget)
        self.statusLabel.setMaximumWidth(540)
        self.statusLabel.setMinimumWidth(540)
        self.statusLabel.setObjectName(u"statusLabel")
        
        self.statusLabel.setSizePolicy(sizePolicy)
        self.setSizePolicy(sizePolicy)
        

        self.verticalLayout_2.addWidget(self.statusLabel)

        self.setCentralWidget(self.centralwidget)

        self.retranslateUi(self)

        MAX_SIZE = QSize(560, 220)
        self.setMaximumSize(MAX_SIZE)
        self.setMinimumSize(MAX_SIZE)

        QMetaObject.connectSlotsByName(self)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"CCCP Mod Conversion Tool", None))
#if QT_CONFIG(statustip)
        MainWindow.setStatusTip(QCoreApplication.translate("MainWindow", u"Waiting...", None))
#endif // QT_CONFIG(statustip)
        self.folders_box.setTitle(QCoreApplication.translate("MainWindow", u"Folders", None))
#if QT_CONFIG(tooltip)
        self.input_folder_picker.setToolTip(QCoreApplication.translate("MainWindow", u"Where the mods to convert are located.", None))
#endif // QT_CONFIG(tooltip)
        self.input_folder_picker.setText(QCoreApplication.translate("MainWindow", u"Input Mod Folder", None))
        self.input_folder_label.setText(QCoreApplication.translate("MainWindow", u"No folder specified.", None))
#if QT_CONFIG(tooltip)
        self.output_folder_picker.setToolTip(QCoreApplication.translate("MainWindow", u"Where the mods will be onced converted.", None))
#endif // QT_CONFIG(tooltip)
        self.output_folder_picker.setText(QCoreApplication.translate("MainWindow", u"Output Mod Folder", None))
        self.output_folder_label.setText(QCoreApplication.translate("MainWindow", u"No folder specified.", None))
        self.settings_box.setTitle(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.output_zips.setText(QCoreApplication.translate("MainWindow", u"Output mods as zip files", None))
        self.play_finish_sound.setText(QCoreApplication.translate("MainWindow", u"Play sound when finished", None))
        self.skip_convert.setText(QCoreApplication.translate("MainWindow", u"Skip Conversion", None))
        self.beautify_lua.setText(QCoreApplication.translate("MainWindow", u"Beautify Lua", None))
#if QT_CONFIG(tooltip)
        self.launch_on_finish.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.launch_on_finish.setStatusTip(QCoreApplication.translate("MainWindow", u"Launch Cortex Command.exe if it exists in the output folder.", None))
#endif // QT_CONFIG(statustip)
        self.launch_on_finish.setText(QCoreApplication.translate("MainWindow", u"Launch after converting", None))
        self.convert_button.setText(QCoreApplication.translate("MainWindow", u"Convert", None))
        self.statusLabel.setText(QCoreApplication.translate("MainWindow", u"Waiting...", None))
    # retranslateUi
    # retranslateUi


class ConverterApplication(QApplication):
    def __init__(self, args) -> None:
        super().__init__(args)
        self.window = ConverterWindow.get_instance()
        self.window.show()

    def create_error_message(msg):
        pass


def run_window():
    app = ConverterApplication(sys.argv)
    app.exec()


def should_enable_convert():
    s = Settings.get(["input_folder", "output_folder"])
    b = bool(s[0] != s[1] and s[0] and s[1])
    return b


def file_button_handler(element):
    data = {
        "input_folder_picker": {
            "caption": "Select input mod folder",
            "label": ConverterWindow.get_instance().input_folder_label,
            "execute": lambda x: Settings.set("input_folder", x),
        },
        "output_folder_picker": {
            "caption": "Select output mod folder",
            "label": ConverterWindow.get_instance().output_folder_label,
            "execute": lambda x: Settings.set("output_folder", x),
        },
    }

    n = element.objectName()
    if n not in data:
        return
    # get the folder picked.
    folder_path = QFileDialog.getExistingDirectory(
        element, data[n]["caption"], os.getcwd()
    )
    if folder_path == "":
        return

    other = "output_folder" if n == "input_folder_picker" else "input_folder"
    if folder_path == Settings.get(other):
        data[n]["label"].setText("Input cannot be same as output!")
        data[n]["label"].setToolTip("Input cannot be same as output!")
        # err.setTex
        createErrorMessageBox("Input folder can't be the same as an output folder!")
        return

    data[n]["label"].setText(folder_path or "No folder specified.")
    data[n]["label"].setToolTip(folder_path or "No folder specified.")
    Settings.set(n.replace("_picker", ""), folder_path)
    should_enable_convert()


def createErrorMessageBox(error_msg: str):
    QErrorMessage().showMessage(error_msg)


def init_checkbox_handler(checkbox: QCheckBox):
    # checkbox.event = checkbox_handler
    checkbox.stateChanged.connect(lambda x: checkbox_handler(checkbox, x))


def checkbox_handler(checkbox: QCheckBox, arg: int):
    bool = [False, True, True]
    name = checkbox.objectName()
    Settings.set(name, bool[arg])


# def unlock_convert_button():
#     gui_windows.get_main_window()["CONVERT"].update(disabled=False)


# def lock_convert_button():
#     gui_windows.get_main_window()["CONVERT"].update(disabled=True)


# def init_window_theme():
#     path_set_color = "#528b30"
#     progress_bar_color = "#17569c"

#     sg.theme("DarkGrey14")
#     sg.theme_input_background_color(path_set_color)
#     sg.theme_progress_bar_color((progress_bar_color, sg.theme_progress_bar_color()[1]))
#     sg.theme_button_color((sg.theme_text_color(), "#2a3948"))


# def init_settings():
#     sg.user_settings_filename(filename="settings.json", path=".")

#     if not os.path.isfile(sg.user_settings_filename()):
#         sg.Popup(
#             "This is a tool that allows you to convert legacy (old) mods to the latest version of CCCP.\n\nYou can get more information from the GitHub repository and the Discord server by clicking their corresponding icons in the bottom-right corner after pressing OK.",
#             title="Welcome",
#             custom_text=" OK ",
#         )

#     cfg.sg = sg

#     warnings.load_conversion_and_warning_rules()  # TODO: Why is this called in this GUI function?

#     default_settings_to_true(["play_finish_sound", "beautify_lua"])


# def default_settings_to_true(settings_to_default_to_true):
#     for setting_to_default_to_true in settings_to_default_to_true:
#         play_finish_sound_setting = Settings.get(
#             setting_to_default_to_true
#         )
#         sg.user_settings_set_entry(
#             setting_to_default_to_true,
#             True if play_finish_sound_setting == None else play_finish_sound_setting,
#         )


# def is_part_of_cccp_folder(cccp_folder):
#     if not cccp_folder.exists():
#         return False

#     while cccp_folder and cccp_folder.name != "":
#         for entry in cccp_folder.iterdir():
#             if entry.is_file() and "Cortex Command" in entry.name:
#                 sg.user_settings_set_entry("cccp_folder", str(cccp_folder))
#                 return True

#         cccp_folder = cccp_folder.parent

#     return False


# def run_window():
# main_window = gui_windows.get_main_window()
# settings_window = None

# cfg.progress_bar = ProgressBar(
#     main_window["PROGRESS_BAR"], main_window["PROGRESS_BAR_TEXT"]
# )

# valid_cccp_path = True if Settings.get("cccp_folder") else False

# while True:
#     window, event, values = sg.read_all_windows()

#     if event == "Exit" or event == sg.WIN_CLOSED:
#         window.close()
#         if window == main_window:
#             break
#         if window == settings_window:
#             settings_window = None
#             main_window.Enable()
#             main_window.BringToFront()

#     elif event == "CCCP_FOLDER":
#         cccp_folder = Path(values[event])

#         if is_part_of_cccp_folder(cccp_folder):
#             valid_cccp_path = True
#             window[event](background_color=sg.theme_input_background_color())
#             window[event](value=Settings.get("cccp_folder"))
#         else:
#             valid_cccp_path = False
#             window[event](background_color=cfg.NO_PATH_SET_COLOR)

#     elif event == "LAUNCH_SETTINGS_WINDOW" and settings_window == None:
#         settings_window = gui_windows.get_settings_window()
#         main_window.Disable()

#     elif event in (
#         "skip_convert",
#         "OUTPUT_ZIPS",
#         "PLAY_FINISH_SOUND",
#         "BEAUTIFY_LUA",
#         "launch_on_finish",
#         "OUTPUT_MOD_FOLDER",
#         "INPUT_MOD_FOLDER"
#     ):
#         value = values[event]
#         sg.user_settings_set_entry(event.lower(), value)

#     elif event == "CONVERT":
#         if valid_cccp_path:
#             cfg.progress_bar.setTitle("Starting...")
#             cfg.progress_bar.reset()
#             lock_convert_button()
#             # Run on a separate thread, don't lock up the UI.
#             t = Thread(target=convert.converwt_all)
#             t.start()

#     elif event == "GITHUB":
#         webbrowser.open(
#             "https://github.com/cortex-command-community/Cortex-Command-Legacy-Mod-Converter"
#         )
#     elif event == "DISCORD":
#         webbrowser.open("https://discord.gg/TSU6StNQUG")
# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'qtcVolYH.ui'
##
## Created by: Qt User Interface Compiler version 6.4.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
