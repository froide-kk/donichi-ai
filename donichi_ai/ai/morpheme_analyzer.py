import MeCab

class MorphemeAnalyzer:
    # 形態素解析
    def analyze(self, text):
        mt = MeCab.Tagger("-Owakati %¥pC").parse(text)
        print(mt)
        return MeCab.Tagger("-Owakati").parse(text).rstrip(" \n").split(" ")
