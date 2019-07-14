
import os

def read():

    save=open('summary','w')
    set_title=set()

    path='./doc'
    dir = os.listdir(path)
    for file in dir:
        file_path=os.path.join(path,file)
        f=open(file)

        for line in f.readlines():
            title=line.split('^')[0]
            if title not in set_title:
                set_title.add(title)
                save.write(line)

        f.close()

    save.close()

    print "Successful!"

def main():
    read()

if __name__ == '__main__':
    main()
