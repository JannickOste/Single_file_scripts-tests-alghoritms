from datetime import datetime


class BruteForcer:
    password = None
    is_found = False
    output = None

    computed_values = 0
    character_table = [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
        'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
        'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E',
        'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
        'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '1', '2', '3', '4', '5',
        '6', '7', '8', '9', '0', '!', '$', '#', '@', '-'
    ]

    def __init__(self, target_password: str):
        self.password = target_password

    def start(self):
        start_time = datetime.now()
        current_password_length = 0
        print("Starting bruteforce attempt at:", start_time)
        while not self.is_found:
            current_password_length += 1
            self.__generateKey(0, [self.character_table[0] for _ in range(0, current_password_length)],
                               current_password_length, current_password_length - 1)

        print("\n".join(["Password: {}".format(self.output),
                         "Password found in: {}".format(datetime.now() - start_time),
                         "Computed values: {}".format(self.computed_values)]))

    def __generateKey(self, position: int, key_characters: list, password_length: int, last_index: int):
        next_position = position + 1
        for i in range(0, len(self.character_table)):
            key_characters[position] = self.character_table[i]

            if position < last_index:
                self.__generateKey(next_position, key_characters, password_length, last_index)
            else:
                self.computed_values += 1

                if "".join(key_characters) == self.password:
                    if not self.is_found:
                        self.is_found = True
                        self.output = "".join(key_characters)
                    return


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    BruteForcer("a123").start()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
