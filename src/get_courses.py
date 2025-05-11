import random
import numpy as np
import os
import matplotlib.pyplot as plt
import traceback

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
                            selected_classes.update(unmet_dicts)
                            self.added_courses.update(unmet_dicts)
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
                            selected_classes.update(unmet_dicts)
                            self.added_courses.update(unmet_dicts)
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
                'german': ["GRMN 205", "GRMN 206", "GRMN 212", "GRMN 290", "GRMN 306", "GRMN 310"],
                'japanese': ["JAPN 300", "JAPN 301", "JAPN 302", "JAPN 303", "JAPN 305", "JAPN 307"],
                'russian': ["RUSN 303", "RUSN 304", "RUSN 310", "RUSN 320","RUSN 330", "RUSN 340",  "RUSN 306"],
            } 
            self.add_course(language_sup[self.language])
            self.add_course(language_sup[self.language])

            # for lang_code in language_sup.get(self.language, []):
            #     lang_course = next((c for c in self.all_courses if c.get("course_code") == lang_code), None)
            #     if lang_course and lang_course["course_code"] not in self.added_courses:
            #         self.schedule.append(lang_course)
            #         self.added_courses.add(lang_course["course_code"])


            
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
        return self.schedule
    

    # def add_course_to_product(self, course, semester_idx):
    #     semester = self.semester_keys[semester_idx]
    #     if course["prereqs"]: 
    #         for prereq in course["prereqs"]:
    #             if prereq["status"] == False: 
    #                 self.add_course_to_product(prereq, semester_idx) #AHHHHHH RECURSION
    #     else:  
    #         course["status"] = True
    #         self.schedule.remove(course)
    #         self.product[semester].append(course) 
    #         return 


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
        self.compile()
        if (self.credits - self.incoming_creds) <= 105: 
            del self.product['Year 4 Spring Semester'] #graduate a semester early 

        if (self.credits - self.incoming_creds) <= 90: 
            del self.product['Year 4 Fall Semester']
        
        self.semester_keys = list(self.product.keys())
        coll_100 = next((c for c in self.schedule if 'COLL 100' in c.get("coll")), None)
        coll_150 = next((c for c in self.schedule if 'COLL 150' in c.get("coll")), None)
        self.schedule = [ {**d, "status": True} if d["course_code"] == coll_100["course_code"] else d for d in self.schedule]
        self.product["Year 1 Fall Semester"].append(coll_100)
        self.schedule = [ {**d, "status": True} if d["course_code"] == coll_150["course_code"] else d for d in self.schedule]
        self.product["Year 1 Spring Semester"].append(coll_150)
        if self.language != "N/A":
            lang1 = next((c for c in self.schedule if c.get("tag") == 'lang' and c.get("status") == False), None)
            self.product["Year 1 Fall Semester"].append(lang1)
            self.schedule = [ {**d, "status": True} if d["course_code"] == lang1["course_code"] else d for d in self.schedule]
            lang2 = next((c for c in self.schedule if c.get("tag") == 'lang' and c.get("status") == False), None)
            self.product["Year 1 Spring Semester"].append(lang2)
            self.schedule = [ {**d, "status": True} if d["course_code"] == lang2["course_code"] else d for d in self.schedule]
            lang3 = next((c for c in self.schedule if c.get("tag") == 'lang'and c.get("status") == False), None)
            self.product["Year 2 Fall Semester"].append(lang3)
            self.schedule = [ {**d, "status": True} if d["course_code"] == lang3["course_code"] else d for d in self.schedule]
            lang4 = next((c for c in self.schedule if c.get("tag") == 'lang' and c.get("status") == False), None)
            self.product["Year 2 Spring Semester"].append(lang4)
            self.schedule = [ {**d, "status": True} if d["course_code"] == lang4["course_code"] else d for d in self.schedule]
            if self.major1 == "international relations" or self.major2 == "international relations":
                lang5 = next((c for c in self.schedule if c.get("tag") == 'lang'and c.get("status") == False), None)
                self.product["Year 3 Fall Semester"].append(lang5)
                self.schedule = [ {**d, "status": True} if d["course_code"] == lang5["course_code"] else d for d in self.schedule]
                if not self.study_abroad:
                    lang6 = next((c for c in self.schedule if c.get("tag") == 'lang'and c.get("status") == False), None)
                    self.product["Year 3 Spring Semester"].append(lang6)
                    self.schedule = [ {**d, "status": True} if d["course_code"] == lang6["course_code"] else d for d in self.schedule]
                else: 
                    lang6 = next((c for c in self.schedule if c.get("tag") == 'lang'and c.get("status") == False), None)
                    self.product["Year 4 Fall Semester"].append(lang6)
                    self.schedule = [ {**d, "status": True} if d["course_code"] == lang6["course_code"] else d for d in self.schedule]
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
                for i in self.schedule: 
                    if i.get("status"):
                        continue  # already scheduled
                    
                    found_place = False
                    end = 0 
                    while not found_place and end < 32:
                        end += 1
                        credits_in_semester = sum(d.get("credits", 0) for d in self.product.get(semester))
                        if (credits_in_semester + i.get("credits")) > 15:
                            semester_idx = (semester_idx + 1) % len(self.semester_keys)
                            semester = self.semester_keys[semester_idx]
                        elif (credits_in_semester + i.get("credits")) <= 18 and end > 8: 
                            found_place = True
                        else: 
                            found_place = True
                    # if end == 32: 
                        # raise ValueError(f"Course: {i.get('course_code')} could not be placed")
                    
                    if i.get("prereqs"): 
                        placed = 0 
                        for prereq in i.get("prereqs"): 
                            done = 0  
                            pre_in_schedule = next((c for c in self.schedule if prereq in c.get("course_code")), None)
                            
                            # print(pre_in_schedule.get("course_code"))
                            if i.get("logic") == 'or' and placed > 0:
                                done += 1
                                break
                            elif not pre_in_schedule: 
                                print(i)
                                raise TypeError(f"Error with course {prereq} as a prereq for {i.get('course_code')}")
                            if pre_in_schedule.get("status") == False:
                                if i.get("logic") == 'or' and placed > 0:
                                    done += 1
                                    break
                                else: 
                                    break
                            
                            for sem in range(0,semester_idx+1):
                                if pre_in_schedule in self.product[self.semester_keys[sem]]:
                                    if pre_in_schedule in self.product[self.semester_keys[semester_idx]]:
                                        semester_idx = (semester_idx + 1) % len(self.semester_keys)
                                        semester = self.semester_keys[semester_idx]
                                        credits_in_semester = sum(d.get("credits", 0) for d in self.product.get(semester))
                                        if (credits_in_semester + pre_in_schedule.get("credits")) <= 18:
                                            done += 1
                                            placed += 1
                                        else:
                                            break
                                    else:     
                                        done += 1
                                        placed += 1
                        if done != 1: 
                            continue

                    i["status"] = True
                    self.product[semester].append(i)
                    # print(f"Course: {i.get('course_code')} scheduled!")
            except Exception as e:
                print(f"Error during scheduling: {e}")
                traceback.print_exc()
                break
        print("unplaced courses: ")
        for i in self.schedule: 
            if not i.get("status"):
                print(i.get('course_code'), i.get("credits"))
                
        return self.product
    
    def make_chart(self): 
        self.make_schedule()
        tag_colors = {
                'minor': 'lightgreen',
                'major1': 'skyblue',
                'major2': 'lavender',
                'coll': 'khaki',
                'lang': 'lightcoral',
                'elective': 'goldenrod',
                'abroad': 'lightgray',
                'proficiency': 'softpink'

            }
        fig, ax = plt.subplots(figsize=(12, 6))
        semesters = list(self.product.keys())
        row_gap = 1.5

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
            mid_col = (len(courses) - 1) / 2
            ax.text(mid_col + 0.5, y + 0.1, semester, ha='center', va='bottom', fontsize=12, fontweight='bold')

        max_cols = max(len(courses) for courses in self.product.values())
        ax.set_xlim(0, max_cols)
        ax.set_ylim(-len(semesters), 1)
        ax.axis("off")
        ax.set_title("Customized Course Schedule by Semester", fontsize=14)
        plt.tight_layout()
        plt.show()


hola = make_a_schedule('economics', 'french', minor = 'psychology', study_abroad= True, credits = 15)
trying = hola.make_schedule() 

print("1 Fall: ") 
for i in trying['Year 1 Fall Semester']: 
    print(i.get("course_code"), i.get("credits"))
print("1 spring: ") 
for i in trying['Year 1 Spring Semester']: 
   print(i.get("course_code"), i.get("credits"))
print("2 Fall: ") 
for i in trying['Year 2 Fall Semester']: 
   print(i.get("course_code"), i.get("credits"))
print("2 spring: ") 
for i in trying['Year 2 Spring Semester']: 
    print(i.get("course_code"), i.get("credits"))
print("3 Fall: ") 
for i in trying['Year 3 Fall Semester']: 
   print(i.get("course_code"), i.get("credits"))
print("3 spring: ") 
for i in trying['Year 3 Spring Semester']: 
   print(i.get("course_code"), i.get("credits"))
print("4 Fall: ") 
for i in trying['Year 4 Fall Semester']: 
    print(i.get("course_code"), i.get("credits"))
if 'Year 4 Spring Semester' in trying:
    print("4 Spring: ") 
    for i in trying['Year 4 Spring Semester']: 
       print(i.get("course_code"), i.get("credits"))


