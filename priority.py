import PeopleInThePicture 
# import main 
import shutil
import os 

# חילוק למיון
def split(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left_arr = split(arr[:mid])
    right_arr = split(arr[mid:])

    return merge(left_arr, right_arr)

# מיון מיזוג
def merge(left_arr, right_arr, milonAtmunotArashi):
    merged = []

    left_len = len(left_arr)
    right_len = len(right_arr)
    left_idx = right_idx = 0

    while left_idx < left_len and right_idx < right_len:
        if milonAtmunotArashi[left_arr[left_idx]].score < milonAtmunotArashi[right_arr[right_idx]].score:
            merged.append(left_arr[left_idx])
            left_idx += 1
        else:
            merged.append(right_arr[right_idx])
            right_idx += 1

    merged.extend(left_arr[left_idx:])
    merged.extend(right_arr[right_idx:])

    return merged



# עדיפות מעודכנת לאדם בתמונה
def priorityAfter(arrpozot,path_folder, milonAtmunotArashi): 
    #תעבור על כל המערך שקיבלת-arrpozot
    #בכל פעם שאתה עומד על פוזה מסוימת
    for poza in arrpozot:
        for image_id  in poza.imagesInPoza:
            sum=0
            image = milonAtmunotArashi[image_id]
            for particpant in image.participants:
                particpant.PriorityInImage =particpant.PriorityInImage* PeopleInThePicture.person[particpant.id].priority
                sum+=particpant.PriorityInImage
                #לכל תמונה בתוך הפוזה צריך לקבוע עדיפות שתהיה עכשיו אמיתית בהתאם לעדיפות הנכונה של כל האנשים שבתוכה 
            image.score=sum
        
        split(poza.imagesInPoza)
        sorted_images = split(poza.imagesInPoza)
        poza.selected_image = sorted_images[0]
        #poza.selected_image=poza.images[0].image_id 
        new_folder = os.path.join(path_folder,"Selected_Image") 
        os.makedirs(new_folder,exist_ok=True)
        # new_folder=path_folder/"Selected_Image" 
        # new_folder.mkdir(exist_ok=True)
        shutil.copy(milonAtmunotArashi[poza.selected_image].path, new_folder)

    return new_folder 

    


        #לפני שיוצאים מהפוזה אחרי שגומרים לקבוע את העדיפות המעודכנת של כל התמונות בפוזה
        #ממינים את המערך של הפוזות במיון מיזוג 
        #ואז שמים בתוך התכונה של POZA.selected_image את הנתיב לתמונה מהמערך הממוין במקום 0
        #ומעבירים את התמונה לתיקיה של התמונות הנבחרות

    #לשמור את כל הנתונים של הלקוח בתוך המסד נתונים עם הקישור לתיקיה שבה התמונות הנבחרות

    # סדר המבני נתונים הוא כך:
    #  יש את מילון בנ"א הראשי שמכיל לכל איי די- מפתח, אובייקט מסוג קלאס איי די. 
    # חוץ ממנו יש את מילון התמונות הראשי שבו לכל מפתח-מונה, יש אובייקט של קלאס אימג' (אימג' דאטה) 
    # יש את מערך הפוזות בו האינדקסים הרי מתחילים מ-0 ובכל אינדקס יש מערך(תמונות בפוזה) שכל איבר זה אוביייקט של פוזה 


    # בעצם, העדיפות של האדם היא כל פעם 1 חלקי מספר האנשים. 
    # צריך לשים לב שללא נרמול התוצאות יהיו לא שיוויוניות. 
    # ? אז איך מנרמלים 
    # המוצלחות של אדם בתמונה היא העדיפות המנורמלת!! כפול המוצלחות, חלקי מספר האנשים
    


def priorityToImage(participants, Image):
    # :כדי לחשב את העדיפות של התמונה אצטרך להתחשב ב
    # חדות, בהירות-מה קורה עם זה? צריך? , סכימת ערכי הוצלחים וסכימת ערכי הלא מוצלחים
    # הנוסחה!!!! פשוטה מאד- 0.6 משקל לחדות ו-0.4 משקל למוצלחות ז"א סכימת המוצלחות של כל האנשים- מוצלחים ולא, כפול 0.4!!!
    Successful = 0
    for participant in participants: 
       Successful+= participant.priority  
    
    
    return participants