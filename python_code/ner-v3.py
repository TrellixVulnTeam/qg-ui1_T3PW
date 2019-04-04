from pycorenlp import StanfordCoreNLP
import sys
import json
nlp = StanfordCoreNLP('http://localhost:9000')
#file_name = 'test1.txt'
file_name = sys.argv[1]
input = file_name.splitlines()
# input = open(file_name).read().splitlines()
i = 0
ans_index=1
res_sentence_arr = []
while (i<len(input)):
    input[i] = input[i].lower()
    res = nlp.annotate(input[i],
                   properties={
                       'annotators': 'ner',
                       'outputFormat': 'json',
                       'timeout': 1000000,
                   })
    flag = 0
    t_flag = 0
    words_ner = []
    index_arr = []
    count  = 0
    for k in range(0,len(res["sentences"])):
        tokens = res["sentences"][k]['tokens']
        for token in tokens:
            w = str(token['word'])
            w_ner = str(token['ner'])
            if w_ner != 'O':
                count = count+1
            words_ner.append((w,w_ner))

    if(count == 0):
        i=i+1
        continue
    else:
        while(len(index_arr) < count ):
            t_flag = 0
            res_sentence = ''
            res_ans=''
            original_sentence = ''
            for j in range(0,len(words_ner)):
                w = words_ner[j][0]
                original_sentence += w + ' '
                ner = words_ner[j][1]
                if t_flag == 1:
                    res_sentence += w + u"\uffe8O_ANS "
                else:
                    if ner == 'O':
                        res_sentence += w + u"\uffe8O_ANS "
                        flag = 0
                    else:
                        if flag == 0 and (j not in index_arr):
                            index_arr.append(j)
                            res_sentence += w + u"\uffe8B_ANS "
                            res_ans += w
                            flag = 1
                            if(j!=(len(words_ner)-1)):
                                if (words_ner[j+1][1] == 'O'):
                                    t_flag = 1
                            else:
                                t_flag = 1
                        elif flag == 1 and (j not in index_arr) :
                            index_arr.append(j)
                            res_sentence += w + u"\uffe8I_ANS "

                            if(j!=(len(words_ner)-1)):
                                if (words_ner[j+1][1] == 'O'):
                                    t_flag = 1
                            else:
                                t_flag = 1
                            res_ans += ' ' + w
                        else:
                            res_sentence += w + u"\uffe8O_ANS "
            res_sentence_arr.append({'index':ans_index,'original_sentence':original_sentence,'tagged_sentence':res_sentence,'answer':res_ans})
            ans_index=ans_index+1

    i = i+1

data = json.dumps(res_sentence_arr,ensure_ascii=False)
print(data)
