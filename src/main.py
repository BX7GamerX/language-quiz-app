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
lib_built = True if line1 == '0' else False
print(lib_built)

# # Ensure consistent library status across all tracking methods
# if lib_built:
#     try:
#         import sys
#         sys.path.append('src')
#         from functions import game_properties, write_to_csv
#         from app_variables import CSVPaths
        
#         # Update game_properties if it's out of sync
#         if not game_properties.is_library_built:
#             print("Synchronizing library status...")
#             game_properties.is_library_built = True
#             # Update the appproperties file to persist this change
#             write_to_csv(CSVPaths.APP_PROPERTIES.value, game_properties.data)
#     except Exception as e:
#         print(f"Warning: Could not synchronize library status: {e}")

if __name__ == "__main__":
    app = MainApp(lib_built)
    #app.iconbitmap(resource_path(r'logo.ico'))

    app.update()
    app.mainloop()
