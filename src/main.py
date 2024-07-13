from mainapplication import MainApp


def read_lib_status(file_path):
    try:
        with open(file_path, 'r') as file:
            line1 = file.readline().strip()
            line2 = file.readline().strip()
            return line1, line2
    except FileNotFoundError:
        return None, None


# Example usage:
file_path = r'wordlib/libstatus'
line1, line2 = read_lib_status(file_path)
lib_built = True if line1 == 0 else False
print(lib_built)
if __name__ == "__main__":
    app = MainApp(lib_built)
    #app.iconbitmap(resource_path(r'logo.ico'))

    app.update()
    app.mainloop()
