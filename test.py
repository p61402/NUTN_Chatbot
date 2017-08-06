import query


def main():
    print("Welcome to NUTN CSIE Chatbot System.")
    while True:
        user_input = input(">>")
        if user_input.lower() == "bye":
            break
        ans = query.question(user_input)
        print(ans)


if __name__ == '__main__':
    main()
