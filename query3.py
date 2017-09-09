import know2
import jieba_system
import random
import string
import collections
from hanziconv import HanziConv


dir_path = "詞庫/"


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


def query_matching(user_query):
    queries = ["C", "I", "CR", "CC", "IR", "II", "IP", "CRC", "CPV", "CRI", "IRPV", "CPVRC", "CRCPV"]
    for num, query in enumerate(queries):
        if collections.Counter(user_query) == collections.Counter(query):
            return num
    return -1


def question(user_input):
    response = not_a_question(user_input)
    if response:
        return response, -2

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

    user_input = HanziConv.toSimplified(user_input)
    user_seg_list = list(jieba_system.start(user_input))
    print("使用者斷詞:", user_seg_list)

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
        elif word in simp_question_words:
            user_question_word = word

    print("user query:", pattern)
    match_number = query_matching(pattern)
    response = know2.make_query(match_number, *keywords)

    if not response and match_number == 0:
        match_number = 15
        response = know2.make_query(match_number, *keywords)
    else:
        response = ", ".join(response)

    if not response or response == "Nope":
        return "不知道耶QAQ", match_number

    return response, match_number
