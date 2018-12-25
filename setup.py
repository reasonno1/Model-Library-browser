from cx_Freeze import setup, Executable

includes = ["os", "sys", "PyQt5.QtWidgets", "PyQt5.QtGui", "PyQt5.QtCore", "pickle", "getpass", "time", "shutil", "PIL"]
buildOption = dict(create_shared_zip=False, append_script_to_exe=True, includes=includes)
executables = [Executable(script='main_gui.py',targetName='library_search.exe',base="Win32GUI")]
setup(name="ProjectName", version="1.0", description=" ", options=dict(build_exe=buildOption), executables=executables)

