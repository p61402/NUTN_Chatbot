import query3
import know2


def main():
    print(know2.instance_relation("rdf:錢炳全"))
    print("Welcome to NUTN CSIE Chatbot System.")
    while True:
        user_input = input(">>")
        ans, match_number = query3.question(user_input)
        print(ans, match_number)


if __name__ == '__main__':
    main()
