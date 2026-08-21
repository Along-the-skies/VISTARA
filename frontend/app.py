import sys
import os
from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QObject, Slot
from PySide6.QtWebChannel import QWebChannel



BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
HTML_FILE = BASE_DIR / "index.html"


sys.path.insert(0, str(PROJECT_ROOT))


class Backend(QObject):

    @Slot(str, result=list)
    def search(self, query):
        print("SEARCH RECEIVED:", query)

        from search.results import run_search

        print("STARTING SEARCH")

        results = run_search(query)

        print("SEARCH FINISHED:", len(results))

        return results

    @Slot(str)
    def open_file(self,path):
        try:
            os.startfile(path)
        except Exception as error:
            print(f"Failed to open file : {error}")


app = QApplication(sys.argv)

window = QWebEngineView()

channel = QWebChannel()
backend = Backend()

channel.registerObject("backend", backend)
window.page().setWebChannel(channel)

window.setWindowTitle("VISTARA")
window.resize(1200, 800)

window.load(HTML_FILE.as_uri())

window.show()

sys.exit(app.exec())