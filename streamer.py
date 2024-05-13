from threading import Thread
from queue import Queue

import numpy as np
import soundcard as sc

from whisper_openvino import WhisperOpenVINO
from translator import EnJaTranslator

class AudioStreamTranslator:
    def __init__(self,samplerate=16000,interval=3,buffer_size=4096):
        """
        Params:
            samplerate(int):音声サンプリングレート 16000Hz固定
            interval(int): Whisperに音声を渡すインターバル時間(秒)
            buffer_size(int): 音声キャプチャのバッファサイズ
        """

        # 音声キュー
        self.audio_q = Queue()
        # 書き起こし文字列キュー
        self.transcribed_q = Queue()

        # whisperモデル
        print("Loading models...",end="")
        self.model_whisper = WhisperOpenVINO()
        print("...",end="")
        # 翻訳スレッド
        self.process_trans = Thread(target=self.run_translator,daemon=True)
        print("done")
        # 音声キャプチャスレッド
        self.thread_cap = Thread(target=self.run_audio_capture,
                                 args=(samplerate,interval,buffer_size),daemon=True)

        # 開始
        self.process_trans.start()
        self.thread_cap.start()
        print("Start translating")
        self.transcribe()

    def run_translator(self):
        """文単位にまとめて翻訳モデルを実行
        """
        min_length = 3 # 文としてみなす最小単語数
        # 翻訳モデルロード
        translator = EnJaTranslator()
        sentence = ""
        while True:
            # 書き起こし文字列取得
            line = self.transcribed_q.get()
            line = line.replace("...","")

            # 単語に分解
            words = line.strip().split()

            # 1語ずつ増やして文末か判断
            for word in words:
                if not sentence.endswith(" "):
                    sentence += " "    
                sentence += word

                # 区切り文字を検出
                if sentence.strip()[-1] in ",.!?":

                    # 指定単語数以上なら翻訳、それ以下なら次の処理に回す
                    if len(sentence.split()) > min_length:
                        print("")
                        print(sentence.strip())
                        print(translator(sentence.strip()))
                        sentence = ""

    def run_audio_capture(self,samplerate,interval,buffer_size):
        """音声キャプチャ実行
        Params:
            samplerate(int):音声サンプリングレート 16000Hz固定
            interval(int): Whisperに音声を渡すインターバル時間(秒)
            buffer_size(int): 音声キャプチャのバッファサイズ
        """
        # 移動平均点数
        n_conv = 200
        b = np.ones(n_conv) / n_conv
        with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=samplerate, channels=1) as mic:
            # 音声データ初期化
            audio = np.empty(samplerate * interval + buffer_size, dtype=np.float32)
            n = 0
            while True:
                while n < samplerate * interval:
                    data = mic.record(buffer_size)
                    audio[n:n+len(data)] = data.reshape(-1)
                    n += len(data)

                # 無音部でクロップしてキューに入れる
                m = n * 7 // 10
                vol = np.convolve(audio[m:n] ** 2, b, 'same')
                m += vol.argmin()
                self.audio_q.put(audio[:m])

                # 次の音声データ
                audio_prev = audio
                audio = np.empty(samplerate * interval + buffer_size, dtype=np.float32)
                audio[:n-m] = audio_prev[m:n]
                n = n-m

    def transcribe(self):
        """書き起こし実行"""
        while True:
            # 音声キューから音声取得
            audio = self.audio_q.get()
            if (audio ** 2).max() > 0.001:
                transcribed_text = self.model_whisper(audio)
                # 書き起こし文字列キューに入れる
                self.transcribed_q.put(transcribed_text.lstrip())

if __name__=="__main__":
    try:
        translator = AudioStreamTranslator()
    except KeyboardInterrupt:
        print("\nFinished")
        
