# Standard Imports
import subprocess

# Third Party Imports
import platform

# Local Imports


def clear_screen():
    osName = platform.system()
    if osName is "Linux" or osName is "Darwin":
        command = "clear"
    elif osName is "Windows":
        command = "cls"
    else:
        for _ in range(0, 60):
            print("\n")
        return

    subprocess.call([command], shell=True)
