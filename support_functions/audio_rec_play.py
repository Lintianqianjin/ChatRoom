# pyrec.py 文件内容
import pyaudio
import wave

class Lin_Audio_Process:
    def __init__(self):
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 2
        self.RATE = 16000
        self.RECORD_SECONDS = 5

    def record_audio(self, file_name):
        p = pyaudio.PyAudio()

        stream = p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)

        # print("开始录音,请说话......")

        frames = []

        for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
            data = stream.read(self.CHUNK)
            frames.append(data)

        print("录音结束,请闭嘴!")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(file_name, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

    def play_audio(self, filename):

        # 引入库
        import wave
        import pyaudio

        # 只读方式打开wav文件
        f = wave.open(filename, "rb")

        p = pyaudio.PyAudio()

        # 打开数据流
        stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                        channels=f.getnchannels(),
                        rate=f.getframerate(),
                        output=True)

        # 读取数据
        data = f.readframes(self.CHUNK)

        # 播放
        while data != b"":
            stream.write(data)
            data = f.readframes(self.CHUNK)
            print('循环中')
            print(data)

        # 停止数据流
        stream.stop_stream()
        stream.close()
        f.close()

        # 关闭 PyAudio
        p.terminate()
        print('结束')


if __name__ == '__main__':
    test = Lin_Audio_Process()
    test.play_audio('test_wav.wav')