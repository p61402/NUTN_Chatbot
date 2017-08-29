import know
import jieba_system
import random
import string
from hanziconv import HanziConv


dir_path = "詞庫/"

patterns = {
    0: ["我無法回答你的問題"],
    1: ["IR有以下這些:"],
    2: ["I的P是:"],
    3: [],
    4: ["在C之下有這些實體:"],
    5: ["I的父類別是:"],
    6: ["在C之下有這些子類別:"]
}

quantity_question_words = ["多少", "幾"]


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


def add_pattern(command, keyword_list):
    sentence = patterns[command][0]
    sentence = "".join([keyword_list.get(word, word) for word in sentence])
    return sentence


def question(user_input):
    response = not_a_question(user_input)
    if response:
        return response

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

    keywords = dict.fromkeys(["C", "I", "R", "P", "Pv"])
    pattern = []
    user_question_word = ""
    for word in user_seg_list:
        if word in simp_classes:
            pattern.append("C")
            keywords["C"] = classes[simp_classes.index(word)]
        elif word in simp_instances:
            pattern.append("I")
            keywords["I"] = instances[simp_instances.index(word)]
        elif word in simp_relations:
            pattern.append("R")
            keywords["R"] = relations[simp_relations.index(word)]
        elif word in simp_properties:
            pattern.append("P")
            keywords["P"] = properties[simp_properties.index(word)]
        elif word in simp_property_values:
            pattern.append("Pv")
            keywords["Pv"] = property_values[simp_property_values.index(word)]
        elif word in simp_question_words:
            user_question_word = word

    print("pattern:", pattern)
    print("question word:", user_question_word)
    arg = [keywords["I"], keywords["R"], keywords["C"], keywords["P"], keywords["Pv"]]
    for i, v in enumerate(arg[:-1]):
        if v:
            arg[i] = "rdf:" + arg[i]
    arg = [a for a in arg if a]

    if "I" in pattern and "R" in pattern:
        command = 1
    elif "C" in pattern:
        if user_question_word in quantity_question_words:
            command = 0
            print("回答在C之下(滿足Pv)的所有instance數量")
        else:
            command = 4
    elif "I" in pattern and "P" in pattern:
        command = 2
    elif "I" in pattern:
        command = 5
    else:
        print(pattern, "is not in the valid query format.")
        command = 0
        arg = []

    keywords = dict((key, value) for key, value in keywords.items() if value)

    print(arg)

    response = know.query(command, *arg)
    if command == 4 and not response:
        command = 6
        response = know.query(command, *arg)
    
    sentence = add_pattern(command, keywords)
    response = sentence + response
    
    return response
