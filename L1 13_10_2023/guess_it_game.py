import random


def read_guess():
    user_input = input()
    while not user_input.isdigit():
        print("Try again")
        user_input = input()
    return int(user_input)


if __name__ == "__main__":
    goal = random.randint(1, 100)

    while True:
        guess = read_guess()
        if guess > goal:
            print("Too big")
        elif guess < goal:
            print("Too small")
        else:
            print("You got it")
            break
