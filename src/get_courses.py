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
        self.added_courses = set()


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

    def get_unmet_prereqs(self, course, schedule = None):
        """
        Checks which prerequisites for a given course are not met by the current schedule.

        Args:
            course (dict): The course to check prerequisites for.
            schedule (list): The current list of scheduled course dictionaries.

        Returns:
            list: A list of course codes representing unmet prerequisites.
        """
        if schedule == None: 
            schedule = self.added_courses
        scheduled_codes = {c["course_code"] for c in schedule}
        prereqs = course.get("prereqs", [])
        unmet = [code for code in prereqs if code not in scheduled_codes]
        return unmet

    def add_course(self, course_list, schedule):
        """
        Adds a valid course to the schedule, checking for duplicates and unmet prerequisites.

        Args:
            course_list (list): List of course dictionaries to consider.
            schedule (list): Current course schedule.

        Returns:
            dict or None: The course added, or None if no valid course was found.
        """
        if not course_list:
            return None

        attempted = 0
        max_attempts = len(course_list)

        while attempted < max_attempts:
            my_course = random.choice(course_list)
            attempted += 1

            if my_course["course_code"] in self.added_courses:
                continue

            unmet_prereqs = self.get_unmet_prereqs(my_course)

            if not unmet_prereqs:
                schedule.append(my_course)
                self.added_courses.add(my_course["course_code"])
                self.credits += my_course.get("credits", 0)
                return my_course

        return None

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
                for course_code in requirement["courses"]:
                    course = next((c for c in self.all_courses if c["course_code"] == course_code), None)
                    if course:
                        selected_classes.add(course)
            elif requirement["type"] == "choose_n":
                n = requirement["n"]
                for group in requirement["groups"]:
                    available_courses_codes = []
                    if group["type"] == "any_of":
                        
                        available_courses_codes.extend(group["courses"])
                
                        # Convert course codes into course dictionaries
                        available_courses = [
                            course for course in self.all_courses
                            if course["course_code"] in available_courses_codes
                        ]
                        #filter out courses with unmet prereqs 
                        filtered_courses = [
                                course for course in available_courses
                                if not self.get_unmet_prereqs(course, list(selected_classes))
                            ]
                        
                        # If no courses have met prerequisites, include courses with unmet prerequisites
                        if not filtered_courses:
                            filtered_courses = available_courses

                        group_selects = random.sample(filtered_courses, n) if filtered_courses else []
                        
                        # Add selected courses to theselected_courses set of selected classes
                        selected_classes.update(group_selects)
            
                        for course in group_selects:
                            unmet = self.get_unmet_prereqs(course, list(selected_classes))
                            
                            # Find full course dicts for unmet prereqs
                            unmet_dicts = [
                                c for c in self.all_courses if c["course_code"] in unmet
                            ]
                            
                            # Add prereqs first
                            selected_classes.update(unmet_dicts)
                            
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
        

    def add_coll_classes(self, seed = None): 
        if seed:
            random.seed(seed) 
        schedule = []
        added_courses = set(self.all_reqs) 
       
        #Additional Knowledge Courses 
        if not any("ALV" in course["domain"] for course in schedule):
            self.add_course([d for d in self.all_courses if "ALV" in d["domain"]], schedule)
        if not any("CSI" in course["domain"] for course in schedule):    
            self.add_course([d for d in self.all_courses if "CSI" in d["domain"]], schedule)
        if not any("NQR" in course["domain"] for course in schedule):
            self.add_course([d for d in self.all_courses if "NQR" in d["domain"]], schedule)

        #COLL Classes (400 is in major)        
        self.add_course([d for d in self.all_courses if "COLL 100" in d["coll"]], schedule)
        self.add_course([d for d in self.all_courses if "COLL 150" in d["coll"]], schedule)
        self.add_course([d for d in self.all_courses if "COLL 200" in d["coll"] and "ALV" in d["domain"]], schedule)
        self.add_course([d for d in self.all_courses if "COLL 200" in d["coll"] and "CSI" in d["domain"]], schedule)
        self.add_course([d for d in self.all_courses if "COLL 200" in d["coll"] and "NQR" in d["domain"]], schedule)
        if not self.study_abroad:
            self.add_course([d for d in self.all_courses if "COLL 300" in d["coll"]], schedule)
        self.add_course([d for d in self.all_courses if "COLL 350" in d["coll"]], schedule)

        # Add language requirements
        if self.language != "N/A":
            language_codes = {
                'spanish': ["HISP 101", "HISP 102", "HISP 201", "HISP 202"],
                'french': ["FREN 101", "FREN 102", "FREN 201", "FREN 202"],
                'arabic': ["ARAB 101", "ARAB 102", "ARAB 201", "ARAB 202"],
                'chinese': ["CHIN 101", "CHIN 102", "CHIN 201", "CHIN 202"],
                'italian': ["ITAL 101", "ITAL 102", "ITAL 201", "ITAL 202"],
                'german': ["GRMN 101", "GRMN 102", "GRMN 201", "GRMN 202"],
                'japanese': ["JAPN 101", "JAPN 102", "JAPN 201", "JAPN 202"],
                'russian': ["RUSN 101", "RUSN 102", "RUSN 201", "RUSN 202"],
            }
            for lang_code in language_codes.get(self.language, []):
                lang_course = next((c for c in self.all_courses if c.get("course_code") == lang_code), None)
                if lang_course and lang_course["course_code"] not in added_courses:
                    schedule.append(lang_course)
                    added_courses.add(lang_course["course_code"])

        #Math & Arts Proficency
        if not any("MATH" in course["coll"] for course in schedule):
            self.add_course([d for d in self.all_courses if "MATH" in d["COLL"]], schedule)
        if not any("ARTS" in course["coll"] for course in schedule):
            self.add_course([d for d in self.all_courses if "ARTS" in d["COLL"]], schedule)

        self.coll_schedule = schedule
        return 
    
    def add_any_electives(self):
        self.get_required_classes()
        self.add_coll_classes
        credits_in_schedule = self.credits
        for course in self.schedule:
            credits_in_schedule += course["credits"]
        


one = make_a_schedule("economics", "N/A")
clean = one.clean_course_data()
more = [c for c in clean if len(c["prereqs"]) > 1]
for i in more: 
    print(i["course_code"], i["prereqs"])


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