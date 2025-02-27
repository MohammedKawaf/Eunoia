import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Controller.controller import Controller

def main():
    app = Controller()
    app.start()
    app.login_view.root.mainloop()

if __name__ == "__main__":
    main()