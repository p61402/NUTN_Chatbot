import know
import jieba_system
import random
import string
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


def question(user_input):
    response = not_a_question(user_input)
    if response:
        return response

    classes = open(dir_path + "類別.txt").read().splitlines()
    instances = open(dir_path + "實體.txt").read().splitlines()
    relations = open(dir_path + "關係.txt").read().splitlines()
    properties = open(dir_path + "特質.txt").read().splitlines()
    question_words = open(dir_path + "疑問詞.txt").read().splitlines()

    simp_classes = [HanziConv.toSimplified(c) for c in classes]
    simp_instances = [HanziConv.toSimplified(i) for i in instances]
    simp_relations = [HanziConv.toSimplified(r) for r in relations]
    simp_properties = [HanziConv.toSimplified(p) for p in properties]
    simp_question_words = [HanziConv.toSimplified(q) for q in question_words]

    user_input = HanziConv.toSimplified(user_input)
    user_seg_list = list(jieba_system.start(user_input))
    print("使用者斷詞:", user_seg_list)

    pattern = ""
    for word in user_seg_list:
        if word in simp_classes:
            pattern += "C"
            class_word = "rdf:" + classes[simp_classes.index(word)]
        elif word in simp_instances:
            pattern += "I"
            instance_word = "rdf:" + instances[simp_instances.index(word)]
        elif word in simp_relations:
            pattern += "R"
            relation_word = "rdf:" + relations[simp_relations.index(word)]
        elif word in simp_properties:
            pattern += "P"
            property_word = "rdf:" + properties[simp_properties.index(word)]
        elif word in simp_question_words:
            pattern += "Q"

    print(pattern)

    if pattern == "CQ":
        print("4")
        command = 4
        arg = [class_word]
        response = know.query(command, *arg)
        if response == "沒有答案":
            command = 6
    elif pattern in ["IQR", "QRI", "RIQ", "IRQ"]:
        print("1")
        command = 1
        arg = [instance_word, relation_word]
    elif pattern == "IPQ":
        print("2")
        command = 2
        arg = [instance_word, property_word]
    elif pattern == "IQ":
        print("5")
        command = 5
        arg = [instance_word]
    else:
        print(pattern, "is not in the valid query format.")
        command = 0
        arg = []

    if command:
        response = know.query(command, *arg)
    else:
        response = "不是正確的句型。"
    return response
