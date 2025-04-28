import random
import numpy as np
import os

major_filepath = os.path.join("data", "majors.npy")
majors = np.load(major_filepath, allow_pickle=True).item()
catalog_filepath = os.path.join("data", "course_catalog.npy")
all_courses = np.load(catalog_filepath, allow_pickle= True)

def get_required_classes(major_name, seed=None):
    if seed is not None:
        random.seed(seed)
    
    major_info = majors.get(major_name)

    selected_classes = set()
    for requirement in major_info["requirements"]:
        if requirement["type"] == "all_of":
            selected_classes.update(requirement["courses"])
        elif requirement["type"] == "choose_n":
            n = requirement["n"]
            for group in requirement["groups"]:
                available_courses = []
                if group["type"] == "any_of":
                    available_courses.extend(group["courses"])
                    available_courses = list(set(available_courses) - selected_classes)
                    selected_courses = random.sample(available_courses, n)
                    selected_classes.update(selected_courses)
    return list(selected_classes)



def get_classes(study_abroad = False, seed = None): 
    coll_schedule = []
    major_schedule = []
    coll_100s = [d for d in all_courses if d["coll"] == "COLL 100"]
    my_coll_100 = random.sample(coll_100s, 1)
    coll_schedule.append(my_coll_100)
    coll_150s = [d for d in all_courses if d["coll"] == "COLL 150"]
    my_coll_150 = random.sample(coll_150s, 1)
    coll_schedule.append(my_coll_150)
    coll_200_alvs = [d for d in all_courses if d["coll"] == "COLL 200" and d["domain"] == "ALV"]
    my_coll_200alv = random.sample(coll_200_alvs, 1)
    coll_schedule.append(my_coll_200alv)
    coll_200_csis = [d for d in all_courses if d["coll"] == "COLL 200" and d["domain"] == "CSI"]
    my_coll_200csi = random.sample(coll_200_csis, 1)
    coll_schedule.append(my_coll_200csi)
    coll_200_nqrs = [d for d in all_courses if d["coll"] == "COLL 200" and d["domain"] == "NQR"]
    my_coll_200nqr = random.sample(coll_200_nqrs, 1)
    coll_schedule.append(my_coll_200nqr)
    if study_abroad == False: 
        coll_300s = [d for d in all_courses if d["coll"] == "COLL 300"]
        my_coll_300 = random.sample(coll_300s,1)
        coll_schedule.append(my_coll_300)
    coll_350s = [d for d in all_courses if d["coll"] == "COLL 350"]
    my_coll_350 = random.sample(coll_350s,1)
    coll_schedule.append(my_coll_350)
    return coll_schedule


#   for i in major1: 
#         major_courses = [d for d in all_courses if d["course_code"] == i]

#     if major2 is not None: 
#         for j in major2: 
#             maj2_corses = [d for d in all_courses if d["course_code"] == j]
#             major_courses.extend(maj2_corses)
#     elif minor is not None: 
#         for k in minor:
#             minor_courses = [d for d in all_courses if d["course_code"] == k]
#             coll_schedule.extend(minor_courses)


# my_list = get_required_classes("computer science")
# for i in my_list:
#    eek = [d for d in all_courses if d["course_code"] == i]
#    if len(eek) == 0:
#        print(f"course: {i} not found")
#    else:
#        print(eek)

# here = get_classes(major1=my_list)
# for item in here:
#     if isinstance(item, list):
#         print(item[0]['course_code'])


