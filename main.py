# Run manually: python main.py

# This is giving the error `pyinstaller: error: argument --add-binary: invalid add_data_or_binary value: 'Lib/stylua/Linux/stylua:Lib/stylua/Linux'`
# Build EXE: pyinstaller --noconsole --onefile --icon="Media/legacy-mod-converter.ico" --add-data="Media/github-icon.png;Media" --add-data="Media/discord-icon.png;Media" --add-data="Media/finish.wav;Media" --add-binary="Lib/stylua/Linux/stylua:Lib/stylua/Linux" --add-data="Lib/stylua/Windows/stylua.exe;Lib/stylua/Windows" --name="Legacy Mod Converter" main.py

# Build EXE: pyinstaller --noconsole --onefile --icon="Media/legacy-mod-converter.ico" --add-data="Media/github-icon.png;Media" --add-data="Media/discord-icon.png;Media" --add-data="Media/finish.wav;Media" --add-binary="Lib/stylua/Windows/stylua.exe;Lib/stylua/Windows" --name="Legacy Mod Converter" main.py

import traceback
import PySimpleGUI as sg
from pathlib import Path
import unittest

# from Python import convert
from Python.gui import gui
from Python import shared_globals as cfg


if __name__ == "__main__":
    try:  # TODO: The VS Code Python debugger isn't able to catch exceptions due to this.
        # convert.convert(
        # 	input_mod_path=Path("I:/Programming/Cortex-Command-Community-Project-Data/LegacyModConverter-v1.2-pre4.0/Input/SRM.rte"),
        # 	input_folder_path="I:/Programming/Cortex-Command-Community-Project-Data/LegacyModConverter-v1.2-pre4.0/Input",
        # 	output_folder_path="I:/Programming/Cortex-Command-Community-Project-Data",
        # 	beautify_lua=True,
        # 	output_zip=True,
        # 	skip_conversion=False,
        # )

        gui.init_window_theme()
        if cfg.RUN_TESTS:
            unittest.TextTestRunner().run(
                unittest.defaultTestLoader.discover("Python/tests")
            )
        gui.init_settings()
        gui.run_window()
    except Exception as e:
        sg.popup_error(
            "AN EXCEPTION OCCURRED!\n\nYou should make a screenshot of this and either make a GitHub issue for this by clicking the GitHub icon in this program, or you can send it to MyNameIsTrez#1585 on Discord.\n"
            + "_" * 60,
            traceback.format_exc(),
            title="AN EXCEPTION OCCURRED!",
        )
