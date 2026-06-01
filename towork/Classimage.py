# class Image:
class ImageData:
    def __init__(self, image_id, path,  score=0.0,participants = None):
        self.image_id = image_id
        self.path = path
        # self.sharpness = sharpness
        # self.brightness = brightness
        self.score = score  # "מוצלחות"
        self.participants = participants if participants is not None else []  # מערך של Participant
        

    def add_participant(self, participant):
        self.participants.add(participant)
        participant.add_image(self)  # קשר דו-כיווני

    def remove_participant(self, participant):
        self.participants.discard(participant)
        participant.remove_image(self)

    @property
    def num_participants(self):
        return len(self.participants)

    def __repr__(self):
        return (f"ImageData(id={self.image_id}, "
                f"path='{self.path}', "
                f"participants={len(self.participants)}, "
                # f"sharpness={self.sharpness}, "
                # f"brightness={self.brightness}, "
                f"score={self.score})")