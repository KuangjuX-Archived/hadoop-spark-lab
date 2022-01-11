import os

def scheduler():
    for i in range(0, 5):
        start_page = 1 if i * 50 == 0 else i * 50
        end_page = (i + 1) * 50
        print("[Debug] start_page: {}, end_page: {}".format(start_page, end_page))
        filename = "data/世纪佳缘-{}.csv".format(i)
        os.system("start python ./main.py {} {} {}".format(start_page, end_page, filename))

if __name__ == '__main__':
    scheduler()