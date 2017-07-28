import know
import jieba_system
import math


def question(user_input):
    user_seg_list = jieba_system.start(user_input)

    file = open('知識庫詞庫.txt', 'r', encoding='utf8')
    words = file.read().splitlines()

    file = open('question_set.txt', 'r', encoding='utf8')
    content = file.read().splitlines()
    matrix = [[0 for x in range(len(words))] for y in range(len(content))]
    for i in range(len(content)):
        seg_list = jieba_system.start(content[i])
        for keyword in seg_list:
            if keyword in words:
                matrix[i][words.index(keyword)] += 1

    user_vector = [0 for x in range(len(words))]
    for seg in user_seg_list:
        if seg in words:
            user_vector[words.index(seg)] += 1

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

    file = open('corresponding_query_set.txt', 'r', encoding='utf8')

    queries = file.read().splitlines()

    data = queries[most_similar_index].split()
    if len(data) <= 4:
        command = int(data[0])
        if command == 3 or command == 4:
            return know.query(command, data[1])
        elif command == 2:
            return know.query(command, data[1], data[2])
        elif command == 1 or command == 5:
            return know.query(command, data[1], data[2], data[3])
    else:
        return "not yet"
