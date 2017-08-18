import query2

def main():
    print("Welcome to NUTN CSIE Chatbot System.")
    while True:
        user_input = input(">>")
        ans = query2.question(user_input)
        print(ans)


if __name__ == '__main__':
    main()
