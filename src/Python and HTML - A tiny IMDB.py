import os

gendata = open("u.genre", "r")
genDict = {}
for line in gendata.readlines():
    line = line.strip("\n")
    line = line.split("|")
    genDict[line[1]] = line[0]

itemdata = open("u.item", "r")
itemDict = {}
movieIds = {}
movAndGen = {}
genList = []
count = 1
films = []
for line in itemdata.readlines():
    line = line.strip("\n")
    line = line.split("|")
    if not len(line) == 23:
        continue
    count1 = 0
    for i in line[4:]:
        if i == '1':
            genList.append(genDict[str(count1)])
            line[count1 + 4] = genDict[str(count1)]
        count1 += 1
    a = line[1].split("(")
    a[0] = a[0].lower()
    films.append(a[0])
    movAndGen[a[0]] = genList[0:]
    genList.clear()
    movieIds[a[0]] = line[0]
    itemDict[a[0]] = line[2:]

ocdata = open("u.occupation", "r")
ocDict = {}
for line in ocdata.readlines():
    line = line.strip("\n")
    line = line.split("|")
    ocDict[line[0]] = line[1]
userdata = open("u.user", "r")
userDict = {}
userAndOcc = {}
for line in userdata.readlines():
    line = line.strip("\n")
    line = line.split("|")
    userDict[line[0]] = line[1:]
    userAndOcc[line[0]] = ocDict[line[3]]


dataData = open("u.data", "r")
dataDict = {}
rateAndMovIds = {}
list1 = []
for line in dataData.readlines():
    line = line.strip("\n")
    line = line.split("\t")
    dataDict[line[3]] = line[0:2]
    list1.append(line[0])
    list1.append(line[2])
    rateAndMovIds[line[1]] = list1[0:]
    list1.clear()
dataData.close()

rvs = {}
fls = []
directory = os.path.normpath("film/")
for subdir, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith(".txt"):
            filmReview = open(os.path.join(subdir, file), 'r')
            a = filmReview.read()
            rvs[str(file)] = a
            fls.append(file)
dennisFilms= []
newpath = 'filmList'
if not os.path.isdir(newpath):
    os.makedirs(newpath)
for i in fls:
    htl = i.split(".")
    name0 = rvs[i].split("\n")
    text = ''
    for i in name0[1:]:
        text = text + i
    name1 = name0[0].split("(")
    name2 = name1[0]
    name = name2.lower()
    dennisFilms.append(name)
    h = movieIds[name] + ".html"
    html = open(newpath + "\\" +h, "w")
    namet = name.title()
    gens = ''
    for i in movAndGen[name]:
        gens = gens +" " +i
    imdb = itemDict[name][1]
    movid = movieIds[name]



    html.write("<html>\n<head>\n<title> " + namet +
               "</title>\n</head>\n<body>\n</head>\n<body>\n"
               "<font face='Times New Roman' font size='6' color='red'<b>"+ namet +
                "</b></font><br>\n<b>Genre: </b>"+ gens +"</b><br>\n<b>IMDB Link:  </b><a href="+imdb+"/>"+namet+"</a><br>"
                "<font face='Times New Roman' font size='4' color='black'><b>Review: </b><br>"
                + str(text) +"</font><br><br>\n <br><b>User who rate the film:  \n</b>")
    dataData = open("u.data", "r")
    totalUser = 0
    total = 0
    for line in dataData.readlines():
        line = line.strip("\n")
        line = line.split("\t")
        mid = line[0]
        if line[1] == movid:
            totalUser += 1
            rate = line[2]
            total = total + int(rate)
            age = userDict[line[0]][0]
            gender = userDict[line[0]][1]
            o = userDict[line[0]][2]
            occ = ocDict[o]
            occ = occ.title()
            zipcode = userDict[line[0]][3]
            html.write("<br><b>User: </b>" + line[0] + " <b>Rate: </b>" + rate + " \n</b>")
            html.write("<br><b>User Detail: Age: </b>" + age + " <b>Gender: </b>" + gender + " <b>Occupation: </b>" + occ + " <b>Zip Code: </b>" + zipcode+ "\n")
    totalRate = total / totalUser
    html.write("<br><br><b>Total User: </b>" + str(totalUser) + " / <b>Total Rate: </b>" + str(totalRate))
    dataData.close()
output = open("review.txt", "w")
for i in films:
    try:
        if i in dennisFilms:
            output.write(movieIds[i] + " " + i.title() + "is found in folder\n")
        else: raise
    except:
        output.write(movieIds[i] + " " + i.title() + " is not found in folder. Look at " + itemDict[i][1] + "\n")
