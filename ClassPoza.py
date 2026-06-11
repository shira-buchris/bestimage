
# מחלקת פוזה
class Posa:
    def __init__(self, IdPoza, folder_path, imagesInPoza):
        self.IdPoza = IdPoza
        self.folder_path = folder_path
        self.selected_image = None  # התמונה הנבחרת
        self.imagesInPoza = imagesInPoza            #מה זה? 
        self.images = [] 
        
    def add_image(self, image):
        self.images.append(image)

    def set_selected_image(self, image):
        if image in self.images:
            self.selected_image = image
        else:
            raise ValueError("Image not in this posa")

    def __repr__(self):
        return (f"Posa(folder='{self.folder_path}', "
                f"num_images={len(self.images)}, "
                f"selected={self.selected_image.image_id if self.selected_image else None})")