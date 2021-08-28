import sys
from controller.Controller import Controller


if __name__ == '__main__':
    app = Controller(sys.argv)
    sys.exit(app.exec_())
