import os
import know2
import jieba_system
import random
import string
import collections
from hanziconv import HanziConv


dir_path = "詞庫/"
record_path = "record/"
quantity_question_words = ["多少", "几", "几个", "几堂", "几位"]
personal_pronoun = ["你", "您", "我", "他", "我们", "你们", "他们", "咱", "咱们", "大家", "大伙儿", "人家", "别人", "旁人", "自", "自个儿"]
demonstrative_pronoun = ["这", "那", "这里", "那里", "这儿", "那儿", "这会儿", "那会儿", "这么", "那么", "这样", "那样", "这么样", "那么样"]
pronoun = personal_pronoun + demonstrative_pronoun

classes = open(dir_path + "類別.txt", encoding='utf8').read().splitlines()
instances = open(dir_path + "實體.txt", encoding='utf8').read().splitlines()
relations = open(dir_path + "關係.txt", encoding='utf8').read().splitlines()
properties = open(dir_path + "特質.txt", encoding='utf8').read().splitlines()
property_values = open(dir_path + "特質內容.txt", encoding='utf8').read().splitlines()
question_words = open(dir_path + "疑問詞.txt", encoding='utf8').read().splitlines()

simp_classes = [HanziConv.toSimplified(c) for c in classes]
simp_instances = [HanziConv.toSimplified(i) for i in instances]
simp_relations = [HanziConv.toSimplified(r) for r in relations]
simp_properties = [HanziConv.toSimplified(p) for p in properties]
simp_property_values = [HanziConv.toSimplified(p) for p in property_values]
simp_question_words = [HanziConv.toSimplified(q) for q in question_words]


def not_a_question(user_input):
    user_input = "".join(char for char in user_input if char not in string.punctuation)
    with open(dir_path + "Greeting.txt", encoding='utf8') as f:
        greeting_list = f.read().splitlines()
        user_greeting_list = [item[:-1].lower() for item in greeting_list]
        if user_input.lower() in user_greeting_list:
            return random.choice(greeting_list)

    with open(dir_path + "bye.txt", encoding='utf8') as f:
        bye_list = f.read().splitlines()
        user_bye_list = [item[:-1].lower() for item in bye_list]
        if user_input.lower() in user_bye_list:
            return random.choice(bye_list)

    with open(dir_path + "彩蛋問句.txt", encoding='utf8') as f1:
        easter_egg_list = f1.read().splitlines()
        user_egg_list = [item[:-1].lower() for item in easter_egg_list]
        if user_input.lower() in user_egg_list:
            index = user_egg_list.index(user_input.lower())
            with open(dir_path + "彩蛋回應.txt", encoding='utf8') as f2:
                egg_response = f2.read().splitlines()
                return egg_response[index]
    return False


def query_matching(user_query, keywords):
    queries = ["C", "I", "CR", "CC", "IR", "II", "IP", "CRC", "CPV", "CRI", "IRPV", "CPVRC", "CRCPV"]
    for num, query in enumerate(queries):
        if collections.Counter(user_query) == collections.Counter(query):
            new_keywords = [None] * len(keywords)
            for i, q1 in enumerate(query):
                for j, q2 in enumerate(user_query):
                    if q1 == q2 and keywords[j]:
                        new_keywords[i] = keywords[j]
                        keywords[j] = None
            return num, new_keywords
    return -1, []


def find_class(word):
    if word in classes:
        return "C", "rdf:" + word
    elif word in instances:
        return "I", "rdf:" + word
    elif word in relations:
        return "R", "rdf:" + word
    elif word in properties:
        return "P", "rdf:" + word
    else:
        return None, None


def question(user_input):
    response = not_a_question(user_input)
    if response:
        return response, -2

    user_input = HanziConv.toSimplified(user_input)
    user_seg_list = list(jieba_system.start(user_input))
    print("使用者斷詞:", user_seg_list)

    is_followup = False
    keywords = []
    pattern = []
    user_question_word = ""
    for word in user_seg_list:
        if word in simp_classes:
            pattern.append("C")
            keywords.append("rdf:" + classes[simp_classes.index(word)])
        elif word in simp_instances:
            pattern.append("I")
            keywords.append("rdf:" + instances[simp_instances.index(word)])
        elif word in simp_relations:
            pattern.append("R")
            keywords.append("rdf:" + relations[simp_relations.index(word)])
        elif word in simp_properties:
            pattern.append("P")
            keywords.append("rdf:" + properties[simp_properties.index(word)])
        elif word in simp_property_values:
            pattern.append("V")
            keywords.append(property_values[simp_property_values.index(word)])
        elif word in pronoun:
            is_followup = True
            pattern.append("N")
            keywords.append("pronoun")
        elif word in simp_question_words:
            user_question_word = word

    if is_followup or (not keywords and user_question_word):
        if not os.path.exists(record_path + 'test_pattern.txt') or not os.path.exists(record_path + 'test_record.txt'):
            return None, 87
        with open(record_path + 'test_pattern.txt', 'w', encoding='utf8') as pf:
            pf.write(" ".join(pattern) + '\n')
            pf.write(" ".join(keywords) + '\n')
        with open(record_path + 'test_record.txt', 'r', encoding='utf8') as rf:
            records = rf.read().splitlines()
        return records, 87

    if os.path.exists(record_path + 'test_record.txt'):
        with open(record_path + 'test_record.txt', 'w', encoding='utf8') as f:
            for keyword in keywords:
                c, _ = find_class(keyword[4:])
                if c:
                    f.write(keyword[4:] + '\n')

    print("user query:", pattern)
    match_number, keywords = query_matching(pattern, keywords)
    response = know2.make_query(match_number, *keywords)

    if not response and match_number == 0:
        match_number = 52
        response = know2.make_query(match_number, *keywords)

    if match_number == 1:
        response.append("".join(keywords))
    elif user_question_word in quantity_question_words and match_number in [0, 4, 7, 8, 9, 10, 11, 12]:
        response = str(len(response))

    if not response:
        unknown_responses = ["不知道耶QAQ", "在下實在是不明白您的意思。", "可以請您更簡單的描述您的問題嗎?", "抱歉我理解力不夠, 可以講清楚一點?"]
        match_number = -1
        return random.choice(unknown_responses), match_number

    return response, match_number
