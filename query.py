import know
import jieba_system
import math


def question(user_input):
    user_seg_list = list(jieba_system.start(user_input))

    print("使用者斷詞結果:", user_seg_list)

    file = open('知識庫詞庫.txt', 'r', encoding='utf8')
    words = file.read().splitlines()
    # print(words)

    file = open('question_set.txt', 'r', encoding='utf8')
    content = file.read().splitlines()
    matrix = [[0 for x in range(len(words))] for y in range(len(content))]
    for i in range(len(content)):
        seg_list = jieba_system.start(content[i])
        for keyword in seg_list:
            if keyword in words:
                matrix[i][words.index(keyword)] += 1

    # print("系統詞頻計算:", matrix)

    user_vector = [0 for x in range(len(words))]
    for seg in user_seg_list:
        if seg in words:
            user_vector[words.index(seg)] += 1

    # print("使用者詞頻計算:", user_vector)

    maximum_cosine = 0
    most_similar_index = 0
    for i in range(len(content)):
        numerator = 0
        user_length = 0
        sample_length = 0
        for n in range(len(user_vector)):
            numerator += user_vector[n] * matrix[i][n]
            user_length += user_vector[n]**2
            sample_length += matrix[i][n]**2
        denominator = math.sqrt(user_length) * math.sqrt(sample_length)
        if denominator != 0:
            cosine = numerator / denominator
        else:
            cosine = 0
        if cosine > maximum_cosine:
            maximum_cosine = cosine
            most_similar_index = i

    if maximum_cosine == 0:
        return "沒有答案"

    print("最相近句型:", content[most_similar_index])

    file = open('corresponding_query_set.txt', 'r', encoding='utf8')

    queries = file.read().splitlines()

    data = queries[most_similar_index].split()

    file_name = data[0] + ".txt"
    file = open(file_name, 'r', encoding='utf8')
    entity_list = file.read().splitlines()
    # print(entity_list)
    arg = ""
    for word in user_seg_list:
        if word in entity_list:
            arg = word

    if data[0] == "物" or data[0] == "人" or data[0] == "事":
        for i in range(2, len(data)):
            if data[i] == "arg1":
                data[i] = "rdf:" + arg

    print("query:", data)

    if len(data) <= 5:
        command, *args = data[1:]
        ans = know.query(int(command), *args)
    else:
        ans = "還沒有這個功能，顆顆"

    return ans
