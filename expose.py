import getpass, os, random, ctypes, time, json
user = getpass.getuser()
pages = folders = i = 0
flag = False

for _, dirnames, filenames in os.walk(os.path.join("c:/", "Internet Explorer")):
  if i == 0:
      folders = dirnames
  pages += len([file for file in filenames if file.endswith(".png")])
  i += 1
# random_folder = os.path.normcase("c:/Internet Explorer/"+folders[random.randint(0, len(folders)-1)])
# print(folders)
for _ in range(len(folders)):
    # print(os.path.join("c:", "Internet Explorer",folders[_], "1.png"))

    if os.path.isfile(os.path.join("c:/", "Internet Explorer",folders[_], "1.png")):
        flag = True
        break
if flag:
    print("{} has downloaded {} doujinshi, and a total of {} pages".format(user, len(folders),pages))
    for _ in range(len(folders)):

        with open(os.path.join("c:/", "Internet Explorer",folders[_], folders[_]+".json")) as json_file:
            data = json.load(json_file)
            print("Setting", data['title'], "as desktop background...")
        # print(os.path.join("c:", "Internet Explorer",folders[_], "1.png"), os.path.isfile(os.path.join("c:/", "Internet Explorer",folders[_], "1.png")))
        ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.join("c:/", "Internet Explorer",folders[_], "1.png") , 0)
        time.sleep(5)
    input()
