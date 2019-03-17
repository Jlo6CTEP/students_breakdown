from DB.db_manager import DbManager, MAX_GRADE
db = DbManager()
class Algorithm:
    # first element is mode of distribution
    # if set to true then all members must have almost same values
    # if false - values should be different

    # second parameter is set to true if needed to minimize parameter
    # third parameter is number of such priorities, max function will be applied to them

    study_group_priority = [True, False, 1, 100]
    project_priority = [True, True, 3, 90]
    language_priority = [True, False, 3, 75]
    role_priority = [False, False, 3, 70]
    experience_priority = [False, False, 1, 50]
    grades_priority = [False, False, 1, 40]
    psych_factor_priority = [False, False, 1, 10]
    
    record_list = None
    
    def __init__(self):
        pass
    
    def do_the_magic(self):
        pass
    
    def priority_vector(self):
        return self.study_group_priority + self.project_priority + \
               self.language_priority + self.role_priority + \
               self.experience_priority + self.grades_priority + \
               self.psych_factor_priority

    def normalizing_vector(self):
        return list(map(lambda x: 10/x, db.get_max_ids()))


    