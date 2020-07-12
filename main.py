from app import *

if __name__ == '__main__':
    app = App()
    app.run_app()
    while True:
        if app.restart:
            app = App()
            app.run_app()
        else:
            break


