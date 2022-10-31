from orgparse import load, loads, date
from orgparse.date import OrgDateClock
# import re
# import datetime
import matplotlib.pyplot as plt

root = load('/home/jack/notes/beorg/chinese.org')
my_list = []

def return_title_and_duration(heading, list_entry):
 # return title and duration
    chapter = heading.get_heading()
    characters = heading.get_property('characters')
    list_entry = [list_entry[0]]

    n = 0
    for i in heading.clock:
       n += i.duration.seconds

    if n != 0:
        list_entry.append(chapter)
        list_entry.append(int(characters))
        list_entry.append(int(n/60))
        # print(chapter)
        # print(characters + " characters")
        # print(str(int(n/60)) + " mins")
        # cpm = 60 * int(characters) / int(n)
        # print(str(int(cpm)) + " cpm\n")
        my_list.append(list_entry)

# def run_on_all_books(books):
#     for book in books:
#         for chapter in book:
#             return_title_and_duration(chapter)

# run_on_all_books(root)

for book in reversed(root.children[0:]):
    list_entry = []
    list_entry.append(book.get_heading())
    for subheading in book:
        return_title_and_duration(subheading, list_entry)

# not necessary
# print(my_list)

# character count total
n = 0
for i in my_list:
    n += i[2]
print("今年年总字数: " + str(n))

# reading time total
m = 0
for i in my_list:
    m += i[3]
h = m - (m % 60)
m = m - h
h = int(h / 60)
d = h - (h % 24)
h = h - d
d = int(d / 24)
print("阅读时间: " + str(d) + "天" + str(h) + "小时" + str(m) + "分钟")

# total average
t = (24 * 60 * d) + (60 * h) + m
print("平均阅读速度：" + str(round(n / t)) + " cpm")

# # The following is used for determining where each book begins and ends
# char_count = 0
# titles = []
# final_chapters = []
# titles.append(my_list[0][0])

# for item in my_list:
#     if item[0] in titles:
#         char_count += item[2]
#     else:
#         final_chapters.append(char_count)
#         char_count += item[2]
#         titles.append(item[0])


# # Determine the midpoint of each book
# midpoints = []
# x0 = 0
# for item in final_chapters:
#     x1 = item
#     midpoint = (x1 - x0) / 2
#     midpoint = midpoint + x0
#     midpoints.append(midpoint)
#     x0 = x1

# # combine title, final chapter and midpoint lists together
# details = list(zip(titles, final_chapters, midpoints)) 


# # graph
# x_entry = 0
# x = []
# y = []
# for entry in my_list:
#     x_entry += entry[2]
#     x.append(x_entry)
#     y.append(int(entry[2] / entry[3]))

# for entry in details:
#     plt.axvline(x=entry[1], color='red', linestyle='--')
#     # TODO change y value
#     plt.text(entry[2], 305, entry[0])

# plt.scatter(x,y)
# plt.show()
