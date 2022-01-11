import os
import csv

def scheduler():
    for i in range(0, 5):
        start_page = 1 if i * 50 == 0 else i * 50
        end_page = (i + 1) * 50
        print("[Debug] start_page: {}, end_page: {}".format(start_page, end_page))
        filename = "data/世纪佳缘-{}.csv".format(i)
        os.system("start python ./main.py {} {} {}".format(start_page, end_page, filename))

def reduce():
    output_filename = "data/新世纪佳缘.csv"
    input_filenames = ["data/世纪佳缘-{}.csv".format(i) for i in range(0,5)]
    writer = open(output_filename, "a+", encoding = 'utf-8')
    csv_writer = csv.writer(writer)
    for filename in input_filenames:
        reader = open(filename, "r+", encoding = 'utf-8')
        csv_reader = csv.reader(reader)
        for line in csv_reader:
            csv_writer.writerow(line)
        reader.close()
    writer.close()

    


if __name__ == '__main__':
    scheduler()
    reduce()