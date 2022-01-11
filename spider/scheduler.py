import os

def scheduler():
    for i in range(0, 10):
        start_page = 1 if i * 10 == 0 else i * 10
        end_page = (i + 1) * 10
        filename = "data/世纪佳缘-{}.csv".format(i)
        os.system("start python ./main.py {} {} {}".format(start_page, end_page, filename))

if __name__ == '__main__':
    scheduler()