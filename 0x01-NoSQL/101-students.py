#!/usr/bin/env python3
""" model for top_students function """


def top_students(mongo_collection):
    """ returns all students sorted by average score """
    student = mongo_collection.find()
    students = []
    for i in student:
        sum = 0
        for x in i["topics"]:
            sum += x["score"]
        i["averageScore"] = sum / len(i["topics"])
        students.append(i)

    students.sort(key=lambda x: x["averageScore"], reverse=True)
    return students
