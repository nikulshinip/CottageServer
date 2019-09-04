import sys
sys.path.append('../config')
import mySQLconfig
sys.path.append('./modulLib')
import ds2408

"""ИНИЦИАЛИЗАЦИЯ"""
"""создание обьектов устройств"""
stairs = ds2408.DS2408(1)		#лестница
terraceLeft = ds2408.DS2408(2)
terraceRight = ds2408.DS2408(3)
room = ds2408.DS2408(4)			#комната 1 этажа
cook = ds2408.DS2408(5)			#кухня
bathRoom = ds2408.DS2408(6)		#ванная
garage = ds2408.DS2408(7)		#гараж

"""все обьекты ds2408 в списке"""
ds2408List = (stairs, terraceLeft, terraceRight, room, cook, bathRoom, garage)

"""функция проверки соединения"""
def checkConnect() :
	for i in ds2408List :
		i.checkConnect()

"""функция вычитывания всех сигналов типа din и помещения их в бд"""
def checkAllDin() :
	for i in ds2408List :
		i.getDinToSQL(1)
		i.getDinToSQL(2)
		i.getDinToSQL(3)
		i.getDinToSQL(4)

"""функция вычитывания всех сигналов типа dout из бд и выставления их в реале"""
def checkMySQLAndUpdateDout() :
	for i in ds2408List :
		i.setDoutStateToSQL(1)
		i.setDoutStateToSQL(2)
		i.setDoutStateToSQL(3)
		
def tackt() :
	checkConnect()
	checkAllDin()
	checkMySQLAndUpdateDout()