import query3


def main():
    print("Welcome to NUTN CSIE Chatbot System.")
    while True:
        user_input = input(">>")
        ans, match_number = query3.question(user_input)
        print(ans, match_number)


if __name__ == '__main__':
    main()
