import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from BYtDl.MainApp import MainApp

if __name__ == "__main__":
    app = MainApp.MainApp()
    app.run()
