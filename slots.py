import random
import time


possible_slots = [
                    "<:Madge:844199172751753257>",
                    "<:sramon:1049037728517472276>",
                    "<:ayaya:917438459512234045>",
                    "<:qeqr:802266069917368362>",
                    "<:qqweqe:804796225773109278>"
                 ]
slots_machine = []

def slots():
  for i in range(3):
    slots_machine.append(possible_slots[random.randrange(len(possible_slots))])
    time.sleep(0.2)
  #print(slots_machine)
  return("["+str(slots_machine[0]) +  " / "+str(slots_machine[1])+" / "+str(slots_machine[2])+"]")

def check_slots(a, b, c):

    if a == b and b == c and c == a:
        return 100
    elif a == b and a != c:
        return 50
    elif a == c and a != b:
        return 50
    elif b == c and a != b:
        return 50
    elif a != b and a != c and b != c:
        return 0

def get_result():
  return check_slots(str(slots_machine[0]),str(slots_machine[1]),str(slots_machine[2]))
  
def points():
  if get_result() == 0:#result == 0:
    return("Wygrałeś - 0$" + "\nPrzegrałeś miernoto  <:qqweqe:804796225773109278>")
  elif get_result() == 50:#result == 50:
    return("Wygrałeś - 50$" + "\nNawet mała wygrana to wciąż wygrana <:blush:917438459763884052>")
  elif get_result() == 200:#result == 100:
    return("Wygrałeś - 200$" + "\nO kurwa wygrałeś  <:pogU:917438459407384576>")
    
