import know
import jieba_system
import random
import string


dir_path = "詞庫\\"


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
    else:
        return "is a question"
    
    # user_seg_list = list(jieba_system.start(user_input))


