from pathlib import Path

import numpy as np
import openvino as ov
import whisper

from util import patch_whisper_for_ov_inference, OpenVINOAudioEncoder, OpenVINOTextDecoder

class WhisperOpenVINO:
    def __init__(self,model_name="small.en"):
        """whisper OpenVINOモデル読み込み
        Params:
            model_name(str):作成したOpenVINOのwhisperモデル名

        """
        WHISPER_ENCODER_OV = Path(f"models/whisper-{model_name}/whisper_{model_name}_encoder_int8.xml")
        WHISPER_DECODER_OV = Path(f"models/whisper-{model_name}/whisper_{model_name}_decoder_int8.xml")

        model = whisper.load_model(model_name, "cpu")

        patch_whisper_for_ov_inference(model)
        core = ov.Core()
        device = "GPU"
        model.encoder = OpenVINOAudioEncoder(core, WHISPER_ENCODER_OV, device=device)
        model.decoder = OpenVINOTextDecoder(core, WHISPER_DECODER_OV, device=device)
        
        self.model = model
        # 初回に無音で推論させてモデルロードを完了させる
        self.__call__(np.zeros(3200,dtype=np.float32),language="en")

    def __call__(self,audio,language="en"):
        """書き起こし実行
        Returns
            str: 書き起こした英文文字列
        """
        return self.model.transcribe(audio,verbose=None,
                                     language=language,
                                     without_timestamps=True)["text"]
