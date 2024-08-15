import threading
import time
import pyaudio
import wave
from mode import Mode


class Player(threading.Thread):
    CHUNK = 1024  # 定义数据流块

    class AbRepeatStateMachine:
        def __init__(self):
            super().__init__()
            self.last_mode = None
            self.has_set_a = False
            self.has_set_b = False

        def init(self):
            self.last_mode = None
            self.has_set_a = False
            self.has_set_b = False

    def __init__(self, filename, mode=Mode.SINGLE):
        super().__init__()
        self.__mode = mode
        self.__wave_read = wave.open(filename, 'rb')
        self.__pyAudio = pyaudio.PyAudio()  # 创建一个播放器
        # 打开数据流
        self.__stream = self.__pyAudio.open(
            format=self.__pyAudio.get_format_from_width(self.__wave_read.getsampwidth()),
            channels=self.__wave_read.getnchannels(),
            rate=self.__wave_read.getframerate(),
            output=True)

        self.__start_frame_pos = 0  # 设置起始 frame position
        self.__end_frame_pos = self.__wave_read.getnframes()
        self.__is_pause = threading.Event()  # 用于暂停线程的标识
        self.__is_pause.set()  # 设置为True
        self.__is_running = threading.Event()  # 用于停止线程的标识
        self.__is_running.set()  # 设置为True
        self.__abr_state_machine = Player.AbRepeatStateMachine()

    def set_mode(self, mode: Mode):
        if self.__mode != Mode.AB_REPEAT:  # 需要先退出 ab_repeat 状态
            self.__mode = mode

    def get_pos(self):
        return self.__wave_read.tell()

    def set_pos(self, pos):
        self.__wave_read.setpos(pos)

    def is_run(self):
        return self.__is_running.isSet()

    def run(self):
        data = self.__wave_read.readframes(Player.CHUNK)  # 读取数据
        while self.is_run() \
                and len(data) > 5 \
                and self.__wave_read.tell() <= self.__end_frame_pos:
            self.__is_pause.wait()  # 为True时立即返回, 为False时阻塞直到内部的标识位为True后返回
            self.__stream.write(data)  # 播放
            data = self.__wave_read.readframes(Player.CHUNK)

        if self.__abr_state_machine.has_set_a:
            self.__abr_state_machine.has_set_b = True

        if self.__mode == Mode.REPEAT or self.__mode == Mode.AB_REPEAT:
            self.__wave_read.setpos(self.__start_frame_pos)  # 重置偏移量循环播放
            self.run()

    def pause(self):
        self.__is_pause.clear()  # 设置为False, 让线程阻塞
        print("pause")

    def resume(self):
        self.__is_pause.set()  # 设置为True, 让线程停止阻塞
        print("resume")

    def stop(self):
        print('stop')
        self.__is_running.clear()  # 将running设置为 False

    def set_a(self):
        # set ab-repeat start position 'a'
        if self.__abr_state_machine.has_set_a is False \
                and self.__abr_state_machine.has_set_b is False:
            self.__start_frame_pos = self.__wave_read.tell()
            self.__abr_state_machine.last_mode = self.__mode
            self.__abr_state_machine.has_set_a = True
            self.__mode = Mode.AB_REPEAT

    def set_b(self):
        # set ab-repeat end position 'b'
        pos = self.__wave_read.tell()
        if self.__abr_state_machine.has_set_a \
            and self.__abr_state_machine.has_set_b is False \
                and pos > self.__start_frame_pos:
            self.__end_frame_pos = self.__wave_read.tell()
            self.__abr_state_machine.has_set_b = True
        self.__mode = Mode.AB_REPEAT

    def quit_ab(self):
        self.__start_frame_pos = 0
        self.__end_frame_pos = self.__wave_read.getnframes()
        self.__mode = self.__abr_state_machine.last_mode
        self.__abr_state_machine.init()


def demo():
    player = Player("resources/01－A Puma at Large.wav")
    player.start()
    time.sleep(2)
    player.pause()
    time.sleep(2)
    player.resume()
    time.sleep(2)

    print('set a')
    player.set_a()
    time.sleep(5)
    print('set b')
    player.set_b()


if __name__ == "__main__":
    demo()
    pass
