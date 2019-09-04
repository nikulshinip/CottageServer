import sys
sys.path.append('../config')
import mySQLconfig
sys.path.append('./modulLib')
import temperatureIn

"""ИНИЦИАЛИЗАЦИЯ"""
"""создание сигналов температур"""
tempBoiler = temperatureIn.TempIn(13)	#температура котла
tempObratki = temperatureIn.TempIn(11)	#температура обратки котла
tempOut = temperatureIn.TempIn(12)		#температура на выходе из котла
tempStairs = temperatureIn.TempIn(5)	#лесница
tempTerrace = temperatureIn.TempIn(6)	#терасса
tempRoom = temperatureIn.TempIn(10)		#комната 1 этажа
tempCook = temperatureIn.TempIn(8)		#кухня
tempBathRoom = temperatureIn.TempIn(9)	#ванная
tempOut = temperatureIn.TempIn(7)		#с наружи

def tackt() :
	tempBoiler.getStateToSQL()
	tempObratki.getStateToSQL()
	tempOut.getStateToSQL()
	tempStairs.getStateToSQL()
	tempTerrace.getStateToSQL()
	tempRoom.getStateToSQL()
	tempCook.getStateToSQL()
	tempBathRoom.getStateToSQL()
	tempOut.getStateToSQL()