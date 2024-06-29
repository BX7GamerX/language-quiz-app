from mainapplication import MainApp
from assetlibmanager import resource_path

if __name__ == "__main__":
    app = MainApp()
    #app.iconbitmap(resource_path(r'logo.ico'))
    app.update()
    app.mainloop()