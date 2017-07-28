import jieba

jieba.load_userdict("知識庫詞庫.txt")


def start(user_input):

    """
    seg_list = jieba.cut(user_input, cut_all=True)
    print("Full Mode: " + "/ ".join(seg_list))

    seg_list = jieba.cut_for_search(user_input)
    print(", ".join(seg_list))
    """

    seg_list = list(jieba.cut(user_input, cut_all=False))
    return seg_list
