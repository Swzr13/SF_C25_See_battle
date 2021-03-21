import ClassSeeBattle

print("-------------------")
print("  Приветсвуем вас  ")
print("      в игре       ")
print("    морской бой    ")
print("-------------------")
while True:
    g = ClassSeeBattle.Game()
    g.start()
    end_game = input('Хотите еще сыграть? "+" - да, "-" - нет')
    if end_game != '+': break
print('Хорошего Вам дня!!!')