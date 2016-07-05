birthday_data = [
    [0x00 for _ in range(0, 16)],
    [0x00 for _ in range(0, 16)],
    [0x00 for _ in range(0, 16)],
    [0x00 for _ in range(0, 16)],
    [0x00 for _ in range(0, 16)],
    [0x00 for _ in range(0, 16)],
    [0x00 for _ in range(0, 16)],
    [0x00 for _ in range(0, 16)],
    [ord(i) for i in list("#" * 16)],
    [ord(i) for i in list("# {:^12} #".format("Happy"))],
    [ord(i) for i in list("# {:^12} #".format("Birthday"))],
    [ord(i) for i in list("# {:^12} #".format("to"))],
    [ord(i) for i in list("# {:^12} #".format("you,"))],
    [ord(i) for i in list("# {:^12} #".format("Happy"))],
    [ord(i) for i in list("# {:^12} #".format("Birthday"))],
    [ord(i) for i in list("# {:^12} #".format("to"))],
    [ord(i) for i in list("# {:^12} #".format("you,"))],
    [ord(i) for i in list("# {:^12} #".format("Happy"))],
    [ord(i) for i in list("# {:^12} #".format("Birthday"))],
    [ord(i) for i in list("# {:^12} #".format("dear"))],
    [ord(i) for i in list("# {:^12} #".format("Kai,"))],
    [ord(i) for i in list("# {:^12} #".format("Happy"))],
    [ord(i) for i in list("# {:^12} #".format("Birthday"))],
    [ord(i) for i in list("# {:^12} #".format("to"))],
    [ord(i) for i in list("# {:^12} #".format("you!"))],
    [ord(i) for i in list("#" * 16)],
    [ord(i) for i in list("{:^16}".format("   (   "))],
    [ord(i) for i in list("{:^16}".format("   )\  "))],
    [ord(i) for i in list("{:^16}".format("  /  ) "))],
    [ord(i) for i in list("{:^16}".format(" ( * ( "))],
    [ord(i) for i in list("{:^16}".format("  \#/  "))],
    [ord(i) for i in list("{:^16}".format(".-\"#'-."))],
    [ord(i) for i in list("{:^16}".format("|\"-.-\"|"))],
    [ord(i) for i in list("{:^16}".format("|     |"))],
    [ord(i) for i in list("{:^16}".format("|     |"))],
    [ord(i) for i in list("{:^16}".format("|     |"))],
    [ord(i) for i in list("{:^16}".format("'-._,-'"))],
    [ord(i) for i in list(" " * 16)],
    [ord(i) for i in list("{:^16}".format(" #####   ##### "))],
    [ord(i) for i in list("{:^16}".format("#     # #     #"))],
    [ord(i) for i in list("{:^16}".format("      #       #"))],
    [ord(i) for i in list("{:^16}".format(" #####   ##### "))],
    [ord(i) for i in list("{:^16}".format("#             #"))],
    [ord(i) for i in list("{:^16}".format("#       #     #"))],
    [ord(i) for i in list("{:^16}".format("#######  ##### "))]
]


def write_message(message):
    for i in range(0, len(message), 3):
        print(message[i])
        print(message[i + 1])
        print(message[i + 2])

write_message(birthday_data)
