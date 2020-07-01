import numpy as np
from moviepy.editor import concatenate_videoclips, TextClip

def  create_video(lyric_duration_data, path_to_audio="placeholder", dest_path="placeholder"):
    screensize = (1920,1080)
    frames=[]
    for frame in lyric_duration_data:
        frames.append(TextClip(frame["line"],color='white', font="Amiri-Bold",
                    kerning = 5, fontsize=50, size=screensize).set_pos('center').set_duration(frame["duration"]))
    combined_frames = concatenate_videoclips(frames, method="compose")
    combined_frames.write_videofile('lyric-video.mp4',fps=25,codec='mpeg4', audio=path_to_audio)

if __name__ == "__main__":                                
    sample_data = [{"line":"I'm checking it twice and I'm getting 'em hit \n The real ones been dying The fake ones is lit", "duration": 5},
            {"line":"The game is off balance I'm back on my shit", "duration": 2}]                                 
    create_video(sample_data)