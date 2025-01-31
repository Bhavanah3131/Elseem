import os
def open_folder(folder_path, file_name):
    file_path =os.path.join(folder_path, file_name)
    try:
        os.startfile(file_path)
    except AttributeError:
        print("os.startfile is not available on this operating system")
    except Exception as e:
        print("An error occured:{e}")


if __name__ == "__main__":
        folder_path = "C:\\Users\\Toshiba\\OneDrive\\Desktop\\companies\\oak"
        file_name = "oakGroveCapitalAnalysis_11.xlsx"
        open_folder(folder_path, file_name)