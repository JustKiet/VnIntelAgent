with open('backend\\app\\đầu cơ.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()
    lines = [line.strip() for line in lines]
    lines = [line for line in lines if line != '\n' and len(line) > 1]
    print(lines)