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

  og_status_of_fal = status_of_fal
  og_fal_bank = fal_bank

  if (False, False) in status_of_fal:
    status_of_fal, fal_bank = false_false(status_of_fal, fal_bank)
  if (True, False) in status_of_fal:
    status_of_fal, fal_bank = true_false(status_of_fal, fal_bank)
  if (False, True) in status_of_fal:
    status_of_fal, fal_bank = false_true(status_of_fal, fal_bank)
  
  # Validation , no purpose for actual tech
  print("Sanity Check!")
  print("\n")
  print("OG stats:")
  print("status of fal: ",len(og_status_of_fal))
  print("fal bank: ",len(og_fal_bank))
  print("\n")
  print("Fixed Stats:")
  print("Does False False exist: ", (False, False) in status_of_fal)
  print("Does True False exist: ",(True, False) in status_of_fal)
  print("Does False True exist: ",(False, True) in status_of_fal)
  print("\n")
  print("status of fal: ", len(status_of_fal))
  print("fal bank: ", len(fal_bank))
  # print("\n")
  # print("aligned_words: ", len(aligned_words))
  # print("\n")
  # print("fal_bank: ", fal_bank)
  # print("\n")
  # print("og_fal_bank: ",og_fal_bank)
  # print("\n")
  # print("status_of_fal: ", status_of_fal)
  # print("\n")
  # print("og_status_of_fal: ", og_status_of_fal)

  dur_bank = calc_duration(fal_bank, aligned_words)
  start_sec = aligned_words[0]["start"]
  
  video_data = [{"line": " ", "duration": start_sec}]
  for fal, dur in zip(fal_bank, dur_bank):
    ln = create_line(fal, aligned_words)
    video_data.append({
      "line": ln,
      "duration": dur
      })

  # print(video_data)
  return video_data
  print("Processing....")
  

def create_line(fal, aligned_words):
  f, l = fal
  line = []
  while f <= l:
    line.append(aligned_words[f]["word"])
    f = f+1
  return ' '.join(line)

def calc_duration(fal_bank, aligned_words):
  dur_bank = []
  for fal in fal_bank:
    first, last = fal
    if last != len(aligned_words)-1:
      dur_bank.append(aligned_words[last+1]["start"] - aligned_words[first]["start"]) 
    else:
      dur_bank.append(aligned_words[last]["end"] - aligned_words[first]["start"]) 
  return dur_bank

def false_false(status_of_fal, fal_bank):
  while (False, False) in status_of_fal:
    current_error = status_of_fal.index((False, False))
    status_of_fal, fal_bank, fn_stat, new_error = shift_left(current_error, status_of_fal, fal_bank)
    if fn_stat == False:
      print("Something went wrong with the shifting left phase!")
    status_of_fal, fal_bank, fn_stat, new_error = shift_right(new_error, status_of_fal, fal_bank)
    if fn_stat == False:
      print("Something went wrong with the shifting right phase!")
  return status_of_fal, fal_bank

def false_true(status_of_fal, fal_bank):
  while (False, True) in status_of_fal:
    current_error = status_of_fal.index((False, True))
    status_of_fal, fal_bank, fn_stat, new_error = shift_left(current_error, status_of_fal, fal_bank)
    if fn_stat == False:
      print("Something went wrong with the shifting left phase!")
  return status_of_fal, fal_bank

def true_false(status_of_fal, fal_bank):
  while (True, False) in status_of_fal:
    current_error = status_of_fal.index((True, False))
    status_of_fal, fal_bank, fn_stat, new_error = shift_right(current_error, status_of_fal, fal_bank)
    if fn_stat == False:
      print("Something went wrong with the shifting right phase!")
  return status_of_fal, fal_bank

          
def shift_left(current_string_number, status_of_fal, fal_bank):
  counter = current_string_number
  while counter != -1:
    counter = counter -1
    if status_of_fal[counter] == (True, False) or status_of_fal[counter] == (True, True):
      # print("shift_left: ", status_of_fal[counter])
      # print(current_string_number)
      fixed_status = merge(status_of_fal[counter], status_of_fal[current_string_number])
      status_of_fal = status_of_fal[0:counter] + [fixed_status] + status_of_fal[(current_string_number + 1):]

      fixed_fal = merge(fal_bank[counter], fal_bank[current_string_number])
      fal_bank = fal_bank[0:counter] + [fixed_fal] + fal_bank[(current_string_number + 1):]
      fn_res = True
      # print(fal_bank)
      return status_of_fal, fal_bank, fn_res, counter
  fn_res = False
  return status_of_fal, fal_bank, fn_res, -1

def shift_right(current_string_number, status_of_fal, fal_bank):
  counter = current_string_number
  while counter != len(status_of_fal) + 1:
      counter = counter + 1
      if status_of_fal[counter] == (False, True) or status_of_fal[counter] == (True, True):
        # print("shift_right: ", status_of_fal[counter])
        # print(current_string_number)
        fixed_status = merge(status_of_fal[current_string_number], status_of_fal[counter])
        status_of_fal = status_of_fal[0:current_string_number] + [fixed_status] + status_of_fal[(counter + 1):]

        fixed_fal = merge(fal_bank[current_string_number], fal_bank[counter])
        fal_bank = fal_bank[0:current_string_number] + [fixed_fal] + fal_bank[(counter + 1):]
        fn_res = True
        # print(fal_bank)
        return status_of_fal, fal_bank, fn_res, current_string_number
  fn_res = False
  return status_of_fal, fal_bank, fn_res, -1

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
