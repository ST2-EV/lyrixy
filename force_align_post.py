import requests

def align_process(path_to_audio, lyrics_file):
    params = (
        ('async', 'false'),
    )
    files = {
        'audio': ('audio.mp3', open(path_to_audio, 'rb')),
        'transcript': ('words.txt', open(lyrics_file, 'rb')),
    }
    response = requests.post(
        'http://35.193.155.100:32769/transcriptions', params=params, files=files)
    
    return response

if __name__ == "__main__":
    # sample test
    result = align_process("audio.mp3", "lyrics.txt")
    print(result)