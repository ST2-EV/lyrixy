# lyrixy
[**Genenrated example from just audio file and lyrics text file**](https://drive.google.com/file/d/1IqlcGBGaHnn4n0nlCDmxP5e62uTlwc-3/view?usp=sharing)
* ```force_align.py``` runs gentle and gives a dictionary.
* ```data.json``` is a sample output from force_align.py with the song MIDDLE CHILD - J.COLE, use this to test and iterate for the file below.
* ```extract_proper_frames.py``` should create split the  lyrics into sentences that have start stop durations in a way tolerating all te words that have not been recognized.
* ```create_video.py``` this creates the video from the data the above file produces.(a dicionary of each line per frame and its respective duration).
* ```main.py``` will be the file that brings all the above files together.
