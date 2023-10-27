PESEL_LENGTH = 11
PESEL_WEIGHT = (1, 3, 7, 9, 1, 3, 7, 9, 1, 3)


def is_length_valid(number: str) -> bool:
    """verifies length of PESEL number"""
    return len(number) == 11


def is_pesel_numerical(number: str) -> bool:
    """verifies if PESEL contains only numbers"""
    return number.isdigit()


def is_date_valid(date: str) -> bool:
    """verifies if date exists"""
    return is_month_valid(date[2:4]) and is_day_valid(date)


def is_month_valid(month: str) -> bool:
    """verifies if month exists"""

    # first digit is even (Jan-Sep) and second digit is 0
    if int(month[0]) % 2 == 0 and not int(month[0]):
        return False

    # first digit is odd (Oct-Dec) and second digit is greater than 2
    if int(month[0]) % 2 and int(month[1]) >= 3:
        return False

    return True


def is_day_valid(date: str) -> bool:
    """verifies if day exists adequately to month"""
    month = (int(date[2]) % 2)*10 + int(date[3])
    day = int(date[4:6])

    # months with 31 days
    if month in [1, 3, 5, 7, 8, 10, 12] and 1 <= day <= 31:
        return True

    # months with 30 days
    if month in [4, 6, 9, 11] and 1 <= day <= 30:
        return True

    # February
    if month == 2 and 1 <= day <= 28:
        return True

    return False


def is_checksum_valid(number: str) -> bool:
    """verify if checksum is correct"""
    checksum = 0

    for i in range(PESEL_LENGTH - 1):
        checksum += PESEL_WEIGHT[i] * int(number[i])
    checksum = (10 - (checksum % 10)) % 10

    return checksum == int(number[10])


def increment_sex_counters(male: int, female: int, sex_digit: int) -> tuple:
    """increments adequate counter in relation to sex"""
    if sex_digit % 2:
        male += 1
    else:
        female += 1
    return male, female


# counters
total = correct = male = female = 0
invalid_length = invalid_digit = invalid_date = invalid_checksum = 0

file = open("1e6.dat", 'r')

# main processing loop
for pesel in file:
    pesel = pesel.strip()
    total += 1

    if is_length_valid(pesel):
        if is_pesel_numerical(pesel):
            if is_date_valid(pesel[:6]):
                if is_checksum_valid(pesel):
                    correct += 1
                    male, female = increment_sex_counters(male, female,
                                                          int(pesel[9]))
                else:
                    invalid_checksum += 1
            else:
                invalid_date += 1
        else:
            invalid_digit += 1
    else:
        invalid_length += 1

file.close()

# show results
print(total, correct, female, male)
print(invalid_length, invalid_digit, invalid_date, invalid_checksum)
