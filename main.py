import time
start = time.time()
import force_align
import extract_proper_frames
import create_video

def run_algo(path_to_audio_file, path_to_lyrics, dest_path="lyrixy-out.mp4"):
	aligned_data = force_align.align_process(path_to_audio_file, path_to_lyrics)
	extract_proper_frames.decide_frames(aligned_data)
	create_video.create_video(video_data, path_to_audio_file, dest_path)
  	print('It took', time.time()-start, 'seconds.')

if __name__ == "__main__":
	run_algo()