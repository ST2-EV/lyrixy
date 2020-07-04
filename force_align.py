# need to have this  in the compiled gentle folder
import logging
import multiprocessing
import os
import sys
import gentle

def align_process(path_to_audio, lyrics_file):
    disfluencies = set(['uh', 'um'])
    
    def on_progress(p):
        for k,v in p.items():
            logging.debug("%s: %s" % (k, v))

    with open(lyrics_file, encoding="utf-8") as fh:
        transcript = fh.read()

    resources = gentle.Resources()
    
    with gentle.resampled(path_to_audio) as wavfile:
        aligner = gentle.ForcedAligner(resources, transcript, nthreads=multiprocessing.cpu_count(), disfluency=False, conservative=False, disfluencies=disfluencies)
        result = aligner.transcribe(wavfile, progress_cb=on_progress, logging=logging)

    return result.to_json(indent=2)

#Testing...
if __name__ == "__main__":
    # sample test
    result = align_process("audio.mp3", "words.txt")
    print(result)