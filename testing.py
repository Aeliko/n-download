import os, requests, bs4, json, configparser

config = configparser.ConfigParser()
config.read('config.ini')

# Wrap in try block in order to hide unexpected crash such as Internet error
try:
    # Target destination folder
    os.makedirs('c:/Internet Explorer', exist_ok=True)

    # For trolling unsuspecting user
    print("Processing:")

    url = config['CONFIG']['website']
    search_options = config['CONFIG']['search_options']

    i = 1
    base_search_url = f'{url}/search/?q={search_options}&page='

    res = requests.get(base_search_url + str(i))
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, features="html.parser")

    # Number of results
    result_pages = int(soup.find_all("a", class_="last")[0]["href"][205:])

    print(result_pages)

    while i != result_pages + 1:
        print(str(i) + '%')

        # Get Page i of search results
        res = requests.get(base_search_url + str(i))
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, features="html.parser")

        links = [a['href'] for a in soup.select('a[href].cover')]

        # Loop through each link in the page
        for link in links:
            res = requests.get(url + link)
            doujinshi = bs4.BeautifulSoup(res.text, features="html.parser")

            title = doujinshi("h1")[0].find_all("span")[1].string

            # print(title)

            pages = int(
                doujinshi.find_all(
                    id="info")[0].find_all("div")[7].find("a").string)

            atrs = {'title': title, 'pages': pages}

            # God number
            folder = link.split("/")[2]

            os.makedirs('c:/Internet Explorer/' + folder, exist_ok=True)

            # Create json in folder for "metadata"
            with open(
                    'c:/Internet Explorer/' + folder + '/' + folder + '.json',
                    "w") as out_file:
                json.dump(atrs, out_file)

            # Save image
            for page in range(1, pages + 1):
                res = requests.get(url + link + str(page) + '/')
                soup = bs4.BeautifulSoup(res.text, features="html.parser")
                pic = soup("img")[1]["src"]
                res = requests.get(pic)
                imageFile = open(
                    os.path.join('c:/Internet Explorer/' + folder,
                                 os.path.basename(str(page) + '.png')), 'wb')
                for chunk in res.iter_content(100000):
                    imageFile.write(chunk)
                imageFile.close()

        i += 1

except:
    # Reassure the user that nothing sus is happening
    print("Something went wrong!")

print("Program finished.")
input()
