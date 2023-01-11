# import PySimpleGUI as sg
# from pathlib import Path

# from Python import utils
# from Python import shared_globals as cfg

# window = None
# app = None
# def get_settings_window_layout():
#     return [
#         [
#             [
#                 sg.Checkbox(
#                     "Skip conversion",
#                     tooltip=" For previously converted mods, does not skip case matching ",
#                     key="skip_convert",
#                     default=Settings.get("skip_convert"),
#                     enable_events=True,
#                 )
#             ],
#             [
#                 sg.Checkbox(
#                     "Output zips",
#                     tooltip=" Zipping is slow ",
#                     key="OUTPUT_ZIPS",
#                     default=Settings.get("output_zips"),
#                     enable_events=True,
#                 )
#             ],
#             [
#                 sg.Checkbox(
#                     "Play finish sound",
#                     tooltip=" Notifies you when the conversion has finished ",
#                     key="PLAY_FINISH_SOUND",
#                     default=Settings.get("play_finish_sound"),
#                     enable_events=True,
#                 )
#             ],
#             [
#                 sg.Checkbox(
#                     "Beautify Lua",
#                     tooltip=" Fixes the indentation and much more of Lua files ",
#                     key="BEAUTIFY_LUA",
#                     default=Settings.get("beautify_lua"),
#                     enable_events=True,
#                 )
#             ],
#             [
#                 sg.Checkbox(
#                     "Launch after converting",
#                     tooltip=" Launches launch_dev.bat after converting ",
#                     key="launch_on_finish",
#                     default=Settings.get("launch_on_finish"),
#                     enable_events=True,
#                 )
#             ],
#         ]
#     ]


# def get_settings_window():
#     return sg.Window(
#         title="Settings",
#         layout=get_settings_window_layout(),
#         icon=utils.path("Media/legacy-mod-converter.ico"),
#         font=("Helvetica", 25),
#         finalize=True,
#     )
