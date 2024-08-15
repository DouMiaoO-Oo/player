import pyaudio
import wave


def demo_test():
    filename = "../resources/01－A Puma at Large.wav"
    wf = wave.open(filename, 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    data = wf.readframes(1024 * 1024)
    stream.write(data)
    print('next chunk')
    data = wf.readframes(1024 * 1024)
    stream.write(data)


if __name__ == '__main__':
    demo_test()
