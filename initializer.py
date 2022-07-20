import os
def appinitializer():
    if not os.path.exists(os.getcwd()+"\\sound\\"):
        os.makedirs(os.getcwd()+"\\sound\\")
    if not os.path.exists(os.getcwd()+"\\setting.py\\"):
        open("setting.py", "a").close()
    # try:
        # print("Yes")
    with open(os.getcwd()+"\\setting.py", "w") as f:
        f.write(f"""file_location='{direc}\\sentence.txt'""")
    # except:
    #     print("Error")
    #     pass
    return True