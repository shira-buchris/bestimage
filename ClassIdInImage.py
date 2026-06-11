# מחלקת אדם בתמונה
class ClassIdInImage: 
    def __init__(self, id ,Sharpness, eyes, smile,PriorityInImage):
        self.id = id 
        self.sharpness = Sharpness 
        self.eyes = eyes 
        self.smile = smile 
        self.PriorityInImage = PriorityInImage            
        self.ImagesThatparticipant = set() 
        self.participants = []
        
    def addto(self,participant): 
        self.participants.add(participant) 