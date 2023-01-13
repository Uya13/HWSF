def printField():
    print('  0 1 2')
    counter = 0
    for row in field:
        string = str(counter) + ' '
        counter += 1
        for element in row:
            string += element + ' '
        print(string)

def checkWin():
    isMinus = False
    for row in field:
        for element in row:
            if element == '-':
                isMinus = True
    if isMinus == False:
        print('Ничья')
        return True

    if field[0][0] == field[0][1] == field[0][2] and field[0][0] != '-':
        print(field[0][0] + ' win!')
        return True
    elif field[1][0] == field[1][1] == field[1][2] and field[1][0] != '-':
        print(field[1][0] + ' win!')
        return True
    elif field[2][0] == field[2][1] == field[2][2] and field[2][0] != '-':
        print(field[2][0] + ' win!')
        return True
    elif field[0][0] == field[1][0] == field[2][0] and field[0][0] != '-':
        print(field[0][0] + ' win!')
        return True
    elif field[0][1] == field[1][1] == field[2][1] and field[0][1] != '-':
        print(field[0][1] + ' win!')
        return True
    elif field[0][2] == field[2][1] == field[2][2] and field[0][2] != '-':
        print(field[0][2] + ' win!')
        return True
    elif field[1][1] == field[0][0] == field[2][2] and field[1][1] != '-':
        print(field[1][1] + ' win!')
        return True
    elif field[1][1] == field[0][2] == field[2][0] and field[1][1] != '-':
        print(field[1][1] + ' win!')
        return True

field = [['-', '-', '-'],
         ['-', '-', '-'],
         ['-', '-', '-']]

xVar = True

printField()

while True:
    if xVar:
        print('Ход X')

        x = int(input('Введите номер строки: '))
        y = int(input('Введите номер столбца: '))

        if field[x][y] == '-':
            field[x][y] = 'X'
            xVar = False
        else:
            print('Ячейка уже заполнена')
    else:
        print('Ход O')

        x = int(input('Введите номер строки: '))
        y = int(input('Введите номер столбца: '))

        if field[x][y] == '-':
            field[x][y] = 'O'
            xVar = True
        else:
            print('Ячейка уже заполнена')

    printField()

    if checkWin():
        break
