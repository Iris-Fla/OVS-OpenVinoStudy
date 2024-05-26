from transformers import pipeline

class EnJaTranslator:
    def __init__(self,model_name="staka/fugumt-en-ja"):
        """翻訳モデルロード
        Params:
            model_name(str): huggingfaceの翻訳モデル名
        """
        self.trans = pipeline("translation", model=model_name)
    def __call__(self,text):
        """翻訳結果の文字列を返す
        Params:
            text(str): 英語の文字列
        Returns:
            str: 翻訳後の日本語の文字列
        """
        result = self.trans(text)
        return  result[0]['translation_text']
    
class JaEnTranslator:
    def __init__(self,model_name="staka/fugumt-ja-en"):
            """翻訳モデルロード
            Params:
                model_name(str): huggingfaceの翻訳モデル名
            """
            self.trans = pipeline("translation", model=model_name)
    def __call__(self,text):
            """翻訳結果の文字列を返す
            Params:
                text(str): 日本語の文字列
            Returns:
                str: 翻訳後の英語の文字列
            """
            result = self.trans(text)
            return  result[0]['translation_text']