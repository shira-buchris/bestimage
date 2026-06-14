# class ID:
#     ID
#     רשימת תמונות בהם משתתף
#     עדיפות כללית
#     גיל

class ClassId:
    def __init__(self, person_id, embedding=None, count= 0, priority=0, age=None):
        self.person_id = person_id  # מזהה אחיד בין תמונות 
        self.embedding = embedding        ## לשאול את שושי בשביל מה אני צריכה בעצם לשמור את זה הרי זה כבר שמור בנתינת הID הייחודי.
        self.count = count              #כמות פעמים שהופיע. 
        self.priority = priority   # כמה הוא חשוב באירוע
        self.images = []         # סט של אובייקטי ImageData 
        #
        # ? self.age = age 

    def add_count(self):
        self.count = self.count+1 

    def add_priority(self,priNow):
        self.priority = self.priority + priNow

    def add_image(self, image):
        self.images.append(image)

    # def remove_image(self, image):
    #     self.images.discard(image)                  ?למה שאצטרך למחוק תמונה 

    def __repr__(self):
        return (f"Id(id={self.person_id}, "
                f"priority={self.priority}"#, age={self.age}, "
                f"num_images={len(self.images)})")
