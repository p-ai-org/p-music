import os

cwd = os.getcwd()

#now let's make a file
#(this line doesn't compile)! os.mkdir("/Whut? Thee Album")
#os.mkdir(r"Whut?_Thee_Album")

#see if getting rid of special characters makes it work
#path = os.path.join(cwd, "Do You Want More ?!!!?!?")
#os.mkdir(path)
path = os.path.join(cwd, "Do_You_Want_More")
os.mkdir(path)

# go through each name and "clean them?"