import wave
import pyaudio
import time


# tamanho do frame
CHUNK = 1024

with wave.open("assets\\music\\wav_file_1mb.wav", "rb") as wf:
    # Instantiate PyAudio and initialize PortAudio system resources (1)
    # p = pyaudio.PyAudio()

    # # Open stream (2)
    # stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
    #                 channels=wf.getnchannels(),
    #                 rate=wf.getframerate(),
    #                 output=True)

    # print(f"quantidade de frames: {wf.getnframes()}")
    # print(f"frames por segundo: {wf.getframerate()}")
    # print(f"qnt frames para 5 segundos: {wf.getframerate() * 5}")

    # Play samples from the wave file (3)
    # while len(data := wf.readframes(CHUNK)):
    #     print(data)  # Requires Python 3.8+ for :=
        # stream.write(data)

    # Close stream (4)
    # stream.close()

    # # Release PortAudio system resources (5)
    # p.terminate()

    # d0 = wf.readframes(CHUNK)
    # d1 = wf.readframes(CHUNK)
    # d2 = wf.readframes(CHUNK)

    # d3 = d0 + d1 + d2

    # n_d1 = []
    d = b"frame1frame2frame3"
    i = 0
    c = 6

    for i in range(3):
        print(d[c*i:c*(i+1)])

