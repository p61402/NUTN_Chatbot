import jieba


dir_path = "詞庫\\"
jieba.load_userdict(dir_path + "知識庫詞庫.txt")
jieba.load_userdict(dir_path + "人.txt")
jieba.load_userdict(dir_path + "事.txt")
jieba.load_userdict(dir_path + "物.txt")


def start(user_input):

    """
    seg_list = jieba.cut(user_input, cut_all=True)
    print("Full Mode: " + "/ ".join(seg_list))

    seg_list = list(jieba.cut(user_input, cut_all=False))
    """

    seg_list = jieba.cut_for_search(user_input)
    return seg_list
