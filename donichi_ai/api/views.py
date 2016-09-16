import json
import re
from collections import OrderedDict
from datetime import datetime
from django.http import HttpResponse
#from ai import ai
from ai import markov
from ai import morpheme_analyzer
from ai import fixed_phrase
from ai import import_text

# Create your views here.
def talk(request):
    #print(request.body)
    request_str = request.body.decode('utf-8')
    print(request_str)
    request_obj = json.loads(request_str)

    user_input = request_obj['question']

    import_text_obj = import_text.ImportText()
    morpheme_analyzer_obj = morpheme_analyzer.MorphemeAnalyzer()
    fixed_phrase_obj = fixed_phrase.FixedPhrase()
    markov_obj = markov.Markov(morpheme_analyzer_obj.analyze(import_text_obj.read()))

    answer_text = ""
    # ユーザー入力をインポートテキストに追記する
    if (re.match("覚えて: ", user_input)):
        text = user_input.replace("覚えて: ", "")
        import_text_obj.add(text)
        markov_obj.add(morpheme_analyzer.analyze(text))
        answer_text = "覚えたよ！"
    else:

        # ユーザー入力を形態素解析
        user_morphemes = morpheme_analyzer_obj.analyze(user_input)

        # 定型文から回答を取得
        answer_text = fixed_phrase_obj.answer(user_input)

        for um in user_morphemes:
            print("user_morphemes : " + um)

        # 定型文の回答がなければマルコフ連鎖で回答
        if answer_text == "":answer_text = markov_obj.answer(user_morphemes)


    answer = {
        "answer" : answer_text,
        "timestamp" : datetime.now().strftime('%Y.%m.%d %H:%M:%S')
    }
    return HttpResponse(json.dumps(answer),
     content_type='application/json; charset=UTF-8',
     status=None)
