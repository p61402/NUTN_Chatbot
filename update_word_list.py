from hanziconv import HanziConv


dir_name = "詞庫/"

with open(dir_name + "總詞庫簡體版.txt", "w") as f:
    f1 = open(dir_name + "類別.txt", encoding='utf8').read().splitlines()
    f2 = open(dir_name + "實體.txt", encoding='utf8').read().splitlines()
    f3 = open(dir_name + "關係.txt", encoding='utf8').read().splitlines()
    f4 = open(dir_name + "特質.txt", encoding='utf8').read().splitlines()
    f5 = open(dir_name + "疑問詞.txt", encoding='utf8').read().splitlines()
    f6 = open(dir_name + "冗詞.txt", encoding='utf8').read().splitlines()
    f7 = open(dir_name + "特質內容.txt", encoding='utf8').read().splitlines()

    x = f1 + f2 + f3 + f4 + f5 + f6 + f7

    x = [HanziConv.toSimplified(w) for w in x]

    for w in x:
        f.write(w + "\n")

print("done")
