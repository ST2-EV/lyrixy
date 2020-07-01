#Pending part
import json
def decide_frames(aligned_data):
   transcript = remove_hyphens(aligned_data["transcript"].splitlines())
   aligned_words = aligned_data["words"]
   fal_bank = []
   f_pointer = 0
   l_pointer = 0
   
   for line in transcript:
       words = line.split()
       l_pointer = l_pointer + len(words)
       fal_bank.append((f_pointer, l_pointer-1))

       f_pointer = l_pointer

   print(fal_bank)
   
   status_of_fal = []
   for fal in fal_bank:
       first, last = fal
       if aligned_words[first]["case"] == "success":
           if aligned_words[last]["case"] == "success":
               status_of_fal.append((True, True))
           else:
               status_of_fal.append((True, False))
       else:
           if aligned_words[last]["case"] == "success":
               status_of_fal.append((False, True))
           else:
               print("error")
               status_of_fal.append((False, False))
   
   for i in range(len(status_of_fal)):
       if(status_of_fal[i] == (False, False)):
           aligned_corrected = merge(i, shift_left(i, status_of_fal, aligned_words), aligned_words)
           aligned_corrected = 
        

           

def shift_left(current_string_number, status_of_fal, aligned_words):
    if (current_string_number < 1):
        return current_string_number + 1
    else: 
        counter = current_string_number
        while counter != 0:
            counter = counter -1
            if status_of_fal[counter] == (True, False) or status_of_fal[counter] == (True, True):
                return counter
        return 0


def shift_right(current_string_number, status_of_fal):
    if (current_string_number ==  len(status_of_fal)-1):
        return current_string_number + 1
    else: 
        counter = current_string_number
        while counter != len(status_of_fal):
            counter = counter + 1
            if status_of_fal[counter] == (False, True) or status_of_fal[counter] == (True, True):
                return counter
        return len(status_of_fal)

def merge(first, last):
    f_first, l_first = first
    f_last, l_last = last
    return (f_first, l_last)



def remove_hyphens(list_of_strings):
    for index, st in enumerate(list_of_strings):
        if "-" in st:
            list_of_strings[index] = " ".join(st.split("-"))
    return list_of_strings    

if __name__ == "__main__":
    with open('data.json', 'r') as fp:
        data = json.load(fp)
    decide_frames(data)
    #print(remove_hyphens(data["transcript"].splitlines()))