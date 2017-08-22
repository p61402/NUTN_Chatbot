import jieba


dir_path = "詞庫/"
jieba.load_userdict(dir_path + "總詞庫簡體版.txt")


def start(user_input):

    """
    seg_list = jieba.cut(user_input, cut_all=True)
    print("Full Mode: " + "/ ".join(seg_list))

    seg_list = list(jieba.cut(user_input, cut_all=False))
    """

    seg_list = jieba.cut(user_input)
    return seg_list
