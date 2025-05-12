import random
import numpy as np
import os
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
matplotlib.use('Agg') 
import traceback
from collections import defaultdict, deque
import logging
import io
import base64


class make_a_schedule: 
    def __init__(self, major1, language, major2 = None, minor = None, study_abroad = False, credits = 0):
        major_filepath = os.path.join("data", "majors.npy")
        minor_filepath = os.path.join("data", "minors.npy")
        catalog_filepath = os.path.join("data", "course_catalog.npy")
        self.majors = np.load(major_filepath, allow_pickle=True).item()
        self.all_courses = np.load(catalog_filepath, allow_pickle= True)
        self.minors = np.load(minor_filepath, allow_pickle=True).item()
        self.major1 = major1
        self.major2 = major2
        self.minor = minor
        self.language = language
        self.study_abroad = study_abroad
        self.credits = credits
        self.incoming_creds = credits
        self.added_courses = set() #course codes of all courses in schedule 
        self.schedule = [] #list of each course dict
        if self.study_abroad == "I am planning on doing a semester abroad": 
            self.study_abroad = True
        elif self.study_abroad == "I am not planning on doing a semester abroad, but I might still study abroad" or self.study_abroad == "I am not planning on studying abroad": 
            self.study_abroad = False
        self.attempts = 0 

    def clean_course_data (self):
        for i in self.all_courses:
            i["tag"] = "unassigned"
            if i["credits"] is None: 
                i["credits"] = 3
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
            if i['course_code'] == "HISP 206" or i['course_code'] == "HISP 207":
                i["prereqs"] = ["HISP 202"]
            if i['course_code'] == "CHIN 301":
                i["prereqs"] = ["CHIN 202"]
            if i['course_code'] == "CHIN 302": 
                i["prereqs"] = ["CHIN 301"]
            if i['course_code'] == 'ITAL 206' or i['course_code'] == 'ITAL 208':
                i["prereqs"] = ["ITAL 202"]
            if i['course_code'] == 'JAPN 303':
                 i["prereqs"] = ["JAPN 302"]
        return self.all_courses

    def get_unmet_prereqs(self, course):
        """
        Checks which prerequisites for a given course are not met by the current schedule.

        Args:
            course (dict): The course to check prerequisites for.
            schedule (list): The current list of scheduled course dictionaries.

        Returns:
            list: A list of course codes representing unmet prerequisites.
        """

        scheduled_codes = {c["course_code"] for c in self.schedule}
        prereqs = course.get("prereqs", [])
        unmet = [code for code in prereqs if code not in scheduled_codes]
        return unmet

    def add_course(self, course_list):
        """
        Adds a valid course to the schedule, checking for duplicates and unmet prerequisites.

        Args:
            course_list (list): List of course dictionaries to consider.
            schedule (list): Current course schedule.

        Returns:
            dict or None: The course added, or None if no valid course was found.
        """
        if not any(course_list):
            return None

        attempted = 0
        max_attempts = len(course_list)

        while attempted < max_attempts:
            my_course = random.choice(course_list)
            attempted += 1
            
            if my_course.get("course_code") in self.added_courses:
                continue

            unmet_prereqs = self.get_unmet_prereqs(my_course)

            if not unmet_prereqs:
                self.schedule.append(my_course)
                self.added_courses.add(my_course["course_code"])
                self.credits += my_course.get("credits", 0)
                return my_course
        print("couldnt add course")
        logging.warning(traceback.format_exc())  # Log the traceback
        return None

    def get_minor_courses(self, seed = None): 
        if seed is not None:
            random.seed(seed)
        
        minor_info = self.minors.get(self.minor)
        selected_classes = set()
        for requirement in minor_info["requirements"]:
            if requirement["type"] == "all_of":
                for course_code in requirement["courses"]:
                    course = next((c for c in self.all_courses if c["course_code"] == course_code), None)
                    if course:
                        course['tag'] = 'minor'
                        selected_classes.add(course["course_code"])
                        self.schedule.append(course)
                        self.added_courses.add(course["course_code"])
                        self.credits += course.get("credits", 0)

            elif requirement["type"] == "choose_n":
                n = requirement["n"]
                for group in requirement["groups"]:
                    if group["type"] == "any_of":
                        available_courses = [
                            course for course in self.all_courses
                            if course["course_code"] in group["courses"]
                        ]

                        filtered_courses = [
                            course for course in available_courses
                            if not self.get_unmet_prereqs(course)
                        ]

                        if len(filtered_courses) < n:
                            filtered_courses = available_courses

                        group_selects = random.sample(filtered_courses, min(n, len(filtered_courses)))
                        
                        for course in group_selects:
                            unmet = self.get_unmet_prereqs(course)
                            unmet_dicts = [
                                c for c in self.all_courses if c["course_code"] in unmet
                            ]
                            selected_classes.update(c["course_code"] for c in unmet_dicts)
                            self.added_courses.update(c["course_code"] for c in unmet_dicts)
                            for prereq in unmet_dicts: 
                                self.credits += prereq.get("credits", 0)
                                selected_classes.add(prereq["course_code"])
                                self.schedule.append(prereq)
                                self.added_courses.add(prereq["course_code"])
                            selected_classes.add(course["course_code"])
                            self.schedule.append(course)
                            self.added_courses.add(course["course_code"])
                            self.credits += course.get("credits", 0)
        for i in self.schedule: 
            if i["course_code"] in selected_classes and i["tag"] == "unassigned": 
                    i["tag"] = "minor"
    

    def get_major_classes(self, primary=True, seed=None):
        if seed is not None:
            random.seed(seed)
        
        major_info = self.majors.get(self.major1 if primary else self.major2)
        if primary:
            major_num = 1
        else: 
            major_num = 2
        selected_classes = set()

        for requirement in major_info["requirements"]:
            if requirement["type"] == "all_of":
                for course_code in requirement["courses"]:
                    course = next((c for c in self.all_courses if c["course_code"] == course_code), None)
                    if course:
                        course["tag"] = f"major {major_num}"
                        selected_classes.add(course["course_code"])
                        self.schedule.append(course)
                        self.added_courses.add(course["course_code"])
                        self.credits += course.get("credits", 0)


            elif requirement["type"] == "choose_n":
                n = requirement["n"]
                for group in requirement["groups"]:
                    if group["type"] == "any_of":
                        available_courses = [
                            course for course in self.all_courses
                            if course["course_code"] in group["courses"]
                        ]

                        filtered_courses = [
                            course for course in available_courses
                            if not self.get_unmet_prereqs(course)
                        ]

                        if len(filtered_courses) < n:
                            filtered_courses = available_courses

                        group_selects = random.sample(filtered_courses, min(n, len(filtered_courses)))
                        
                        for course in group_selects:
                            unmet = self.get_unmet_prereqs(course)
                            unmet_dicts = [
                                c for c in self.all_courses if c["course_code"] in unmet
                            ]
                            selected_classes.update(c["course_code"] for c in unmet_dicts)
                            self.added_courses.update(c["course_code"] for c in unmet_dicts)
                            for prereq in unmet_dicts: 
                                self.credits += prereq.get("credits", 0)
                                selected_classes.add(prereq["course_code"])
                                self.schedule.append(prereq)
                                self.added_courses.add(prereq["course_code"])
                            selected_classes.add(course["course_code"])
                            self.schedule.append(course)
                            self.added_courses.add(course["course_code"])
                            self.credits += course.get("credits", 0)

        for i in self.schedule: 
            if i["course_code"] in selected_classes and i["tag"] == "unassigned": 
                i["tag"] = f"major {major_num}"
               

           

    def add_coll_classes(self, seed = None): 
        if seed:
            random.seed(seed) 
        
        #Additional Knowledge Courses 
        if not any("ALV" in course["domain"] for course in self.schedule):
            self.add_course([d for d in self.all_courses if "ALV" in d["domain"]])
        if not any("CSI" in course["domain"] for course in self.schedule):    
            self.add_course([d for d in self.all_courses if "CSI" in d["domain"]])
        if not any("NQR" in course["domain"] for course in self.schedule):
            self.add_course([d for d in self.all_courses if "NQR" in d["domain"]])


        #Math & Arts proficiency
        if not any("MATH" in course["coll"] for course in self.schedule):
            self.add_course([d for d in self.all_courses if "MATH" in d["coll"]])
        if not any("ARTS" in course["coll"] for course in self.schedule):
            self.add_course([d for d in self.all_courses if "ARTS" in d["coll"]])
        
        
        
        if self.major1 == "kinesiology" or self.major2 == "kinesiology":
            self.add_course([d for d in self.all_courses if "NQR" in d["domain"]])
            self.add_course([d for d in self.all_courses if "NQR" in d["domain"]])
            self.add_course([d for d in self.all_courses if "NQR" in d["domain"]])
        
        for i in self.schedule: 
            if i["tag"] == "unassigned": 
                i["tag"] = "proficiency"

        #COLL Classes (400 is in major)        
        self.add_course([d for d in self.all_courses if "COLL 100" in d["coll"]])
        self.add_course([d for d in self.all_courses if "COLL 150" in d["coll"]])
        self.add_course([d for d in self.all_courses if "COLL 200" in d["coll"] and "ALV" in d["domain"]])
        self.add_course([d for d in self.all_courses if "COLL 200" in d["coll"] and "CSI" in d["domain"]])
        self.add_course([d for d in self.all_courses if "COLL 200" in d["coll"] and "NQR" in d["domain"]])
        if not self.study_abroad:
            self.add_course([d for d in self.all_courses if "COLL 300" in d["coll"]])
        self.add_course([d for d in self.all_courses if "COLL 350" in d["coll"]])

        for i in self.schedule: 
             if i["tag"] == "unassigned": 
                    i["tag"] = "coll"

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
                if lang_course and lang_course["course_code"] not in self.added_courses:
                    self.schedule.append(lang_course)
                    self.added_courses.add(lang_course["course_code"])
            
        if self.major1 == "international relations" or self.major2 == "international relations":
            language_sup = {
                'spanish': ["HISP 206", "HISP 207", "HISP 208", "HISP 209", "HISP 240"],
                'french': ["FREN 206", "FREN 210", "FREN 212", "FREN 303", "FREN 303A", "FREN 304"],
                'arabic': ["ARAB 290", "ARAB 301", "ARAB 302", "ARAB 303", "ARAB 304"],
                'chinese': ["CHIN 301", "CHIN 302", "CHIN 308", "CHIN 386"],
                'italian': ["ITAL 206", "ITAL 208", "ITAL 303", "ITAL 317"],
                'german': ["GRMN 203", "GRMN 205", "GRMN 206", "GRMN 212", "GRMN 290", "GRMN 306", "GRMN 310"],
                'japanese': ["JAPN 300", "JAPN 301", "JAPN 302", "JAPN 303", "JAPN 305", "JAPN 307"],
                'russian': ["RUSN 303", "RUSN 304", "RUSN 310", "RUSN 320","RUSN 330", "RUSN 340",  "RUSN 306"],
            } 

            # self.add_course(language_sup[self.language])
            # self.add_course(language_sup[self.language])
            sup_courses = [] 
            for lang_code in language_sup.get(self.language):
                sup_course = next((c for c in self.all_courses if c.get("course_code") == lang_code), None)
                # print(sup_course)
                sup_courses.append(sup_course)
            self.add_course(sup_courses)
            self.add_course(sup_courses)


            
        for i in self.schedule: 
            if i["tag"] == "unassigned": 
                i["tag"] = "lang"

        return self.schedule
    
    def add_abroad(self): 
        if self.study_abroad: 
            sem_abroad = [{"course_code": "ABROAD", 'credits': 15, 'prereqs': [], 'coreqs': [] , 'coll': ['COLL 300'], 'domain': [], 'tag': 'abroad'}]
            self.add_course(sem_abroad)
        return
    
    def add_any_electives(self):
        credits_needed = 120 - self.credits
        while not credits_needed <= 0: 
            self.add_course(self.all_courses)
            if self.schedule[-1].get("credits") > 4: 
                self.schedule.pop()
            credits_needed = 120 - self.credits
        for i in self.schedule: 

            if i["tag"] == "unassigned": 
                i["tag"] = "elective"
        return
            
    def get_credits(self):
        return (self.credits - self.incoming_creds)
            
    def compile(self): 
        self.clean_course_data()
        self.get_major_classes()
        if self.major2: 
            self.get_major_classes(primary = False)
        elif self.minor:
           self.get_minor_courses()
        self.add_coll_classes()
        self.add_abroad()
        self.add_any_electives()
        for k in self.schedule: 
            k["status"] = False
            if k["course_code"] == 'DATA 201':
                k["logic"] = 'or'
               
            elif k["course_code"] == 'MATH 112' or k["course_code"] == 'MATH 132' or k["course_code"] == 'MATH 211' or k["course_code"] == 'MATH 212' or k["course_code"] == 'MATH 213' or k["course_code"] == 'MATH 214' or k["course_code"] == 'MATH 351' or k["course_code"] == 'MATH 352':
                k["logic"] = 'or'
                        
            elif k["course_code"] == 'CHEM 205' or k["course_code"] == 'CHEM 206' or k["course_code"] == 'CHEM 208' or k["course_code"] == 'CHEM 207'or k["course_code"] == 'CHEM 415':
                if k["course_code"] == 'CHEM 207':
                    k["prereqs"] = ['CHEM 206']
                if k["course_code"] == 'CHEM 415':
                    k["prereqs"] = ['CHEM 314', "BIOL 314"]
                k["logic"] = 'or'
            
            elif k["course_code"] == 'CHEM 209':
                k["prereqs"] = ['CHEM 206']
            
            elif k["course_code"] == 'CHEM 314':
                k["prereqs"] = ['CHEM 207', 'CHEM 205', 'CHEM 209', 'CHEM 208']
           
            elif k["course_code"] == 'FREN 212' or k["course_code"] == 'FREN 303' or k["course_code"] == 'FREN 304':
                k["logic"] = 'or'
            
            elif k["course_code"] == 'KINE 303' or k["course_code"] == 'KINE 304':
                k["logic"] = 'or'
            elif k['course_code'] == 'CSCI 243':
                k["logic"] = 'or'
            elif k["credits"] > 4:
                if not k['course_code'] == "ABROAD":
                    self.schedule.remove(k)
                    credits_needed = 120 - self.credits
                    while not credits_needed <= 0: 
                        self.add_course(self.all_courses)
                        credits_needed = 120 - self.credits
                    for i in self.schedule: 
                        if i["tag"] == "unassigned": 
                            i["tag"] = "elective"

            #elif k['course_code'] == 'BUAD 350':

        
        
        return self.schedule
    

    def sort_schedule(self):
        self.compile()

        prereq_map = defaultdict(set)  # Tracks prerequisite relationships
        in_degree = defaultdict(int)     # Tracks the number of prerequisites for each course
        course_map = {course["course_code"]: course for course in self.schedule}

        # Step 1: Build dependency mappings and in-degrees
        for course in self.schedule:
            code = course["course_code"]
            for prereq in course.get("prereqs", []):
                prereq_map[prereq].add(code)
                in_degree[code] += 1

        # Step 2: Topological Sort
        sorted_courses_topological = []
        queue = deque([code for code in course_map if in_degree[code] == 0])  # Start with courses with no prerequisites

        while queue:
            code = queue.popleft()
            sorted_courses_topological.append(course_map[code])

            for dependent in prereq_map.get(code, []):
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)

        # Check for cycles (if the length doesn't match, there's a dependency cycle)
        if len(sorted_courses_topological) != len(self.schedule):
            self.schedule = [] 
            self.attempts += 1
            if self.attempts > 4: 
                raise ValueError("Circular dependency detected in the schedule.")
            self.sort_schedule()

        # Step 3: Assign hierarchical tiers
        is_prereq = set()
        has_prereqs = set()
        for course in self.schedule:
            code = course["course_code"]
            if code in prereq_map:
                is_prereq.add(code)
            for prereq in course.get("prereqs", []):
                has_prereqs.add(code)
                break # Optimization: once a prereq is found, it has prereqs

        def get_tier(code):
            if code in is_prereq and code in has_prereqs:
                return 1  # Both are prerequisites & have prerequisites
            elif code in is_prereq:
                return 0  # Only a prerequisite
            elif code in has_prereqs:
                return 2  # Only has prerequisites
            else:
                return 3  # Elective (neither)

        # Step 4: Sort the topologically sorted courses by tier
        sorted_schedule = sorted(sorted_courses_topological, key=lambda course: get_tier(course["course_code"]))

        self.schedule = list(sorted_schedule) # Ensure self.schedule is updated
        return self.schedule

    def make_schedule(self):
        self.product = {    
            'Year 1 Fall Semester': [],
            'Year 1 Spring Semester': [],
            'Year 2 Fall Semester': [],
            'Year 2 Spring Semester': [],
            'Year 3 Fall Semester': [], 
            'Year 3 Spring Semester': [],
            'Year 4 Fall Semester': [],
            'Year 4 Spring Semester': []
        }
        self.times = 0 
        if self.times < 1:
            self.sort_schedule()
        # if (self.credits - self.incoming_creds) <= 110: 
        #     del self.product['Year 4 Spring Semester'] #graduate a semester early 

        # if (self.credits - self.incoming_creds) <= 100: 
        #     del self.product['Year 4 Fall Semester']
        
        self.semester_keys = list(self.product.keys())
        coll_100 = next((c for c in self.schedule if 'COLL 100' in c.get("coll")), None)
        coll_150 = next((c for c in self.schedule if 'COLL 150' in c.get("coll")), None)
        self.schedule = [ {**d, "status": True} if d["course_code"] == coll_100["course_code"] else d for d in self.schedule]
        self.product["Year 1 Fall Semester"].append(coll_100)
        self.schedule = [ {**d, "status": True} if d["course_code"] == coll_150["course_code"] else d for d in self.schedule]
        self.product["Year 1 Spring Semester"].append(coll_150)
        if self.language != "N/A":
            semester_idx = 0
            for d in self.schedule: 
                if d.get('tag') == 'lang': 
                    if (self.major1 == "international relations" or self.major2 == "international relations") and self.study_abroad and semester_idx == 6:
                        semester_idx += 1
                    if semester_idx > 7:
                        break
                        #print(semester_idx)
                    d['status'] = True
                    self.product[self.semester_keys[semester_idx]].append(d)
                    semester_idx += 1 
        if self.study_abroad: 
                abroad_class = next((c for c in self.schedule if c.get("tag") == 'abroad'), None)
                self.schedule = [ {**d, "status": True} if d["course_code"] == abroad_class["course_code"] else d for d in self.schedule]
                self.product["Year 3 Spring Semester"].append(abroad_class)
        
        semester_idx = 0
        semester = self.semester_keys[semester_idx]
        max_loops = 10000
        loops = 0 
        while not all(d["status"] for d in self.schedule) and loops < max_loops:
            loops += 1
            try:  
                for course in self.schedule: 
                    if course.get("status"):
                        continue  # already scheduled
                    
                    placed = False

                    # Try two passes: first for ≤15 credits, then for ≤18
                    for credit_limit in [15, 18]:
                        for semester_idx, semester in enumerate(self.semester_keys):
                            if self.study_abroad:
                                if semester_idx == 5: 
                                    continue
                            # Check prereqs are met in earlier semesters
                            prereqs = course.get("prereqs", [])
                            logic = course.get("logic", "and")
                            if logic is None:
                                logic = "and" 
                            satisfied = []

                            for prereq in prereqs:
                                prereq_satisfied = False
                                prereq_semester_idx = -1

                                for prev_idx in range(semester_idx):
                                    for prev_course in self.product[self.semester_keys[prev_idx]]:
                                        if prev_course.get("course_code") == prereq and prev_course.get("status"):
                                            prereq_satisfied = True
                                            prereq_semester_idx = prev_idx
                                            break
                                    if prereq_satisfied:
                                        break
                                
                                # Ensure prerequisites are at least one semester before
                                if prereq_satisfied and prereq_semester_idx >= semester_idx:
                                    prereq_satisfied = False
                                
                                satisfied.append(prereq_satisfied)


                            if prereqs:
                                if (logic == "and" and not all(satisfied)) or (logic == "or" and not any(satisfied)):
                                    continue  # prereqs not met, skip to next semester

                            # Check current semester credits
                            total_credits = sum(d.get("credits", 0) for d in self.product[semester])
                            if total_credits + course.get("credits", 0) > credit_limit:
                                continue  # semester is full under this limit

                            # Place the course
                            course["status"] = True
                            self.product[semester].append(course)
                            placed = True
                            break  # break out of semester loop

                        if placed:
                            break  # break out of credit limit loop if placed

            except Exception as e:
                print(f"Error during scheduling: {e}")
                traceback.print_exc()
                break
        # if not all(c for c in self.schedule if c.get('status')):
        #     self.times += 1 
        #     if self.times > 5:
        #            return
        #     for i in self.schedule: 
        #         if not i.get("status"):
        #             print(i.get("course_code"), i.get('prereqs'))
        #         #make it do the function again! (but not compile?)
        #         if i.get('status'):
        #             i['status'] = False
        #     self.make_schedule()
                
        return self.product
    
    def make_chart(self, output=None): 
        self.make_schedule()
        used_tags = set(course["tag"] for semester in self.product.values() for course in semester)

        tag_colors = {
                    'minor': '#90EE90',       # lightgreen
                    'major 1': '#87CEEB',      # skyblue
                    'major 2': '#D8BFD8',      # thistle (better than lavender)
                    'coll': '#F0E68C',        # khaki
                    'lang': '#F08080',        # lightcoral
                    'elective': '#FFDAB9',    # peachpuff
                    'abroad': '#D3D3D3',      # lightgray
                    'proficiency': '#FFB6C1'  # lightpink
                }
        legend_elements = [
                            mpatches.Patch(color=tag_colors[tag], label=tag.capitalize())
                            for tag in used_tags
                        ]
        fig, ax = plt.subplots(figsize=(12, 6))
        semesters = list(self.product.keys())
        row_gap = 2

        for row, semester in enumerate(semesters):
            y = -(row * row_gap)
            courses = self.product[semester]
            for col, course in enumerate(courses):
                tag = course["tag"]
                color = tag_colors.get(tag, "lightgray")
                # Draw rectangle with border
                rect = plt.Rectangle((col, y - 1), 1, 1, facecolor=color, edgecolor="black", linewidth=1.5)
                ax.add_patch(rect)
                # Add course code label inside block
                ax.text(col + 0.5, y - 0.5, course["course_code"], ha='center', va='center', fontsize=10)
            
            # Add semester label above the row
            # mid_col = (len(courses) - 1) / 2
            ax.text(-0.4, y + 0.2, semester, ha='left', va='bottom', fontsize=12, fontweight='bold')

        max_cols = max(len(courses) for courses in self.product.values())
        ax.set_xlim(0, max_cols)
        ax.set_ylim(-len(semesters) * row_gap, 1)
        ax.axis("off")
        ax.set_title("Customized Course Schedule by Semester", fontsize=14)
        ax.legend(handles=legend_elements, title="Course Categories", loc="upper right", bbox_to_anchor=(1.15, 1))
        plt.tight_layout()
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_dir = os.path.join(base_dir, "assets")
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, "schedule.png")
        if output:
            fig.savefig(output, format='png')  # or plt.savefig(output)
        else:
            fig.savefig(filepath)
            plt.close(fig)
            return 



# def fig_to_base64(fig):
#     buf = io.BytesIO()
#     fig.savefig(buf, format='png')
#     buf.seek(0)
#     encoded = base64.b64encode(buf.read()).decode('utf-8')
#     buf.close()
#     plt.close(fig)
#     return f"data:image/png;base64,{encoded}"




# omg = make_a_schedule('economics', 'N/A', credits= 12)
# trying = omg.make_chart()
# # for i in trying: 
#     print(i.get('course_code'))