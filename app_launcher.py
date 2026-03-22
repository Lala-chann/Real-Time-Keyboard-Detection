#TODO(1): Import OS to enable to access computer
import os


#TODO(2): Write down what apps you want to access with visual keyboard. Hints: start refers to clicking double with mouse
apps = {
    "settings": "start ms-settings:",
    "calculator": "start calc",
    "notepad": "start notepad",
    "camera": "start microsoft.windows.camera:",
    "files": "start explorer",
    "chrome" : "start chrome"
}

#TODO(3): Call launch_apps function for launching apps. Hints: os.system()
def launch_apps(typed_text):
    word = typed_text.strip().lower()

    if word in apps:
        os.system(apps[word])
        return f"{word} is successfully opening"
    else:
        return f"{word} could not found. Try again!"