import random
import numpy as np
import os

class make_a_schedule: 
    def __init__(self, major1, language, major2 = None, minor = None, study_abroad = False, credits = 0):
        major_filepath = os.path.join("data", "majors.npy")
        catalog_filepath = os.path.join("data", "course_catalog.npy")
        self.majors = np.load(major_filepath, allow_pickle=True).item()
        self.all_courses = np.load(catalog_filepath, allow_pickle= True)
        self.minors = { }
        self.major1 = major1
        self.major2 = major2
        self.minor = minor
        self.language = language
        self.study_abroad = study_abroad
        self.credits = credits


    def clean_course_data (self):
        for i in self.all_courses:
            real_prereqs = []
            coreqs = []
            if isinstance(i["prereqs"], list):
                for j in i["prereqs"]:
                    if j != '' and j != 'Modern Campus Catalog™' and j != 'Print (opens a new window)' and j != 'catalogs' and j != 'T' and j != 'Help (opens a new window)' and j != 'Modern Languages and Literatures': 
                        course = next((c for c in self.all_courses if c.get("course_code") == j), None)
                        if course and i["course_code"] in course["prereqs"]:
                            coreqs.append(j)
                        else: 
                            real_prereqs.append(j)
            
                i["prereqs"] = real_prereqs
                i["coreqs"] = coreqs
            if i['coll'] is not None:
                if ', ' in i["coll"]:
                    i['coll'] = i['coll'].split(', ')
                else:
                    i['coll'] = [i["coll"]]
            elif i['coll'] is None: 
                i['coll'] = []
        return self.all_courses

    def get_minor_courses(self, seed = None): 
        if seed is not None:
            random.seed(seed)
        
        minor_info = self.minors.get(self.minor)
        selected_classes = set()
        for requirement in minor_info["requirements"]:
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
        self.minor_classes = list(selected_classes)
        return self.minor_classes

    def get_major_classes(self, primary = True, seed=None):
        if seed is not None:
            random.seed(seed)
        
        if primary == False: 
            major_info = self.majors.get(self.major2)
        else: 
            major_info = self.majors.get(self.major1)

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
        if primary == True: 
            self.major1_classes = list(selected_classes)
            return self.major1_classes
        else:
            self.major2_classes = list(selected_classes)
            return self.major2_classes

    def get_required_classes(self):
        self.get_major_classes(primary = True)
        if self.major2 is not None: 
            self.get_major_classes(primary = False)
            self.all_reqs = self.major1_classes.extend(self.major2_classes)
            return self.all_reqs
        elif minor is not None: 
            minor = self.get_minor_courses(minor)
            self.all_reqs = self.major1_classes.extend(minor)
            return self.all_reqs
        else: 
            self.all_reqs = self.major1_classes
            return self.all_reqs
        

    def get_coll_classes(self, seed = None): 
        coll_schedule = []
        coll_100s = [d for d in self.all_courses if "COLL 100" in d["coll"]]
        my_coll_100 = random.sample(coll_100s, 1)
        coll_schedule.append(my_coll_100)
        coll_150s = [d for d in self.all_courses if "COLL 150" in d["coll"] ]
        my_coll_150 = random.sample(coll_150s, 1)
        coll_schedule.append(my_coll_150)
        coll_200_alvs = [d for d in self.all_courses if "COLL 200" in d["coll"] and "ALV" in d["domain"]]
        my_coll_200alv = random.sample(coll_200_alvs, 1)
        coll_schedule.append(my_coll_200alv)
        coll_200_csis = [d for d in self.all_courses if "COLL 200" in d["coll"] and "CSI" in d["domain"]]
        my_coll_200csi = random.sample(coll_200_csis, 1)
        coll_schedule.append(my_coll_200csi)
        coll_200_nqrs = [d for d in self.all_courses if "COLL 200" in d["coll"] and "NQR" in d["domain"]]
        my_coll_200nqr = random.sample(coll_200_nqrs, 1)
        coll_schedule.append(my_coll_200nqr)
        if self.study_abroad == False: 
            coll_300s = [d for d in self.all_courses if "COLL 300" in d["coll"]]
            my_coll_300 = random.sample(coll_300s,1)
            coll_schedule.append(my_coll_300)
        coll_350s = [d for d in self.all_courses if "COLL 350" in d["coll"]]
        my_coll_350 = random.sample(coll_350s,1)
        coll_schedule.append(my_coll_350)
        if self.language is not "N/A": 
            if self.language == 'spanish': 
                lang_req = ["HISP 101", "HISP 102", "HISP 201", "HISP 202"]
                for i in lang_req: 
                    k = next((c for c in self.all_courses if c.get("course_code") == i), None)
                    coll_schedule.append(k)
            elif self.language == 'french': 
                lang_req = ["FREN 101", "FREN 102", "FREN 201", "FREN 202"]
                for i in lang_req: 
                    k = next((c for c in self.all_courses if c.get("course_code") == i), None)
                    coll_schedule.append(k)
            elif self.language == 'arabic': 
                lang_req = ["ARAB 101", "ARAB 102", "ARAB 201", "ARAB 202"]
                for i in lang_req: 
                    k = next((c for c in self.all_courses if c.get("course_code") == i), None)
                    coll_schedule.append(k)
            elif self.language == 'chinese': 
                lang_req = ["CHIN 101", "CHIN 102", "CHIN 201", "CHIN 202"]
                for i in lang_req: 
                    k = next((c for c in self.all_courses if c.get("course_code") == i), None)
                    coll_schedule.append(k)
            elif self.language == 'italian': 
                lang_req = ["ITAL 101", "ITAL 102", "ITAL 201", "ITAL 202"]
                for i in lang_req: 
                    k = next((c for c in self.all_courses if c.get("course_code") == i), None)
                    coll_schedule.append(k)
            elif self.language == 'german': 
                lang_req = ["GRMN 101", "GRMN 102", "GRMN 201", "GRMN 202"]
                for i in lang_req: 
                    k = next((c for c in self.all_courses if c.get("course_code") == i), None)
                    coll_schedule.append(k)
            elif self.language == 'japanese': 
                lang_req = ["JAPN 101", "JAPN 102", "JAPN 201", "JAPN 202"]
                for i in lang_req: 
                    k = next((c for c in self.all_courses if c.get("course_code") == i), None)
                    coll_schedule.append(k)
            elif self.language == 'russian': 
                lang_req = ["RUSN 101", "RUSN 102", "RUSN 201", "RUSN 202"]
                for i in lang_req: 
                    k = next((c for c in self.all_courses if c.get("course_code") == i), None)
                    coll_schedule.append(k)
        return coll_schedule

# subset_with_prereqs = [
#     d for d in all_courses
#     if isinstance(d.get('prereqs'), list) and len(d.get('prereqs', [])) >= 1
# ]
# print(len(subset_with_prereqs))
    

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

# clean_cc = clean_course_data()
# bio = next((c for c in all_courses if c.get("course_code") == "ECON 307"), None)
# print(bio)