import sys
sys.path.append('../config')
import mySQLconfig
sys.path.append('./modulLib')
import gpioInOut, wifiTemperatureIn, kotelOption, kotelTimeout, kotelLog

"""ИНИЦИАЛИЗАЦИЯ"""

"""создание сигналов DIN"""
dinOnOff = gpioInOut.Din(1)			#положение главного пускателя
dinOverheating = gpioInOut.Din(2)	#положение пускателя перегрева
dinStage1 = gpioInOut.Din(3)		#положение 1 ступени котла
dinStage2 = gpioInOut.Din(4)		#положение 2 ступени котла
dinStage3 = gpioInOut.Din(5)		#положение 3 ступени котла
dinStage4 = gpioInOut.Din(6)		#положение 4 ступени котла
dinStage5 = gpioInOut.Din(7)		#положение 5 ступени котла
dinStage6 = gpioInOut.Din(8)		#положение 6 ступени котла
dinPump1 = gpioInOut.Din(9)			#работа насоса системы отопления
#dinPump2 = gpioInOut.Din(10)		#работа насоса 2 						#удалено

"""создание сигналов DOUT"""
doutOnOff = gpioInOut.Dout(1)		#вкл/откл главного пускателя
doutOverheating = gpioInOut.Dout(2)	#вкл/откл пускателя перегрева
doutStage1 = gpioInOut.Dout(3)		#вкл/откл 1 ступени котла
doutStage2 = gpioInOut.Dout(4)		#вкл/откл 2 ступени котла
doutStage3 = gpioInOut.Dout(5)		#вкл/откл 3 ступени котла
doutStage4 = gpioInOut.Dout(6)		#вкл/откл 4 ступени котла
doutStage5 = gpioInOut.Dout(7)		#вкл/откл 5 ступени котла
doutStage6 = gpioInOut.Dout(8)		#вкл/откл 6 ступени котла
doutPump1 = gpioInOut.Dout(9)		#вкл/откл насоса системы отопления
doutPump2 = gpioInOut.Dout(10)		#вкл/откл насоса2 						#удалено	#возврат из-за постоянно подтянутого пускателя

"""создание сигналов температур"""
#tempBoiler = temperatureIn.TempIn(1)	#температура котла
tempBoiler = wifiTemperatureIn.WiFiTempIn(1)	#температура котла wi-fi
#tempObratki = temperatureIn.TempIn(2)	#температура обратки котла
tempObratki = wifiTemperatureIn.WiFiTempIn(2)	#температура обратки котла wi-fi
tempFloor1 = wifiTemperatureIn.WiFiTempIn(4)	#температура с конечного датчика температуры wi-fi
#tempOut = temperatureIn.TempIn(3)		#температура на выходе из котла
tempOut = wifiTemperatureIn.WiFiTempIn(3)		#температура на выходе из котла wi-fi

"""создание сигналов дополнительных опций"""
optOnOff = kotelOption.Opt(1)		#опция вкл/откл отопления
optMode = kotelOption.Opt(2)		#режим работы котла по комнате/по обратке
optAutoPower = kotelOption.Opt(3)	#автоматическая регулировка мощности котла
optTimeout = kotelOption.Opt(4)		#опция вкл/откл работы таймаутов
optTemp1 = kotelOption.Opt(5)		#опция предела температуры 1 этажа
optTempBack = kotelOption.Opt(6)	#опция предела температуры обратки
optDeltaTemp1 = kotelOption.Opt(7)	#дельта температурного режима при работе по температуре комнаты
optDeltaBack = kotelOption.Opt(8)	#дельта температурного режима при работе по температуре обратки

"""вычитывание для необновляемых параметров"""
optDeltaTemp1.getSQL()				
optDeltaBack.getSQL()
"""создание обьекта таймаута"""
timeout = kotelTimeout.TimeOut()
"""создание обьекта логирования"""
log = kotelLog.Log
"""блокировки для логов"""
logBloking = {
	'floor1On' : False,				#вкл.  отопления 1 этажа
	'floor1Off' : False,			#откл. отопления 1 этажа
	'modeRoom' : False,				#Режим по температуре комнаты
	'modeBack' : False,				#Режим по температуре обратки
	'autoPowerOn' : False,			#режим автоматической регулировки мощности
	'autoPowerOff' : False,			#режим ручной регулировки мощности
	'overheating' : False,			#перегрев
	'timeout' : False				#таймауты
	}
"""функция опроса датчиков и установки по ним значений в базу данных"""
def setSqlSistemParamiter() :
	dinOnOff.getStateToSQL()
	dinOverheating.getStateToSQL()
	dinStage1.getStateToSQL()
	dinStage2.getStateToSQL()
	dinStage3.getStateToSQL()
	dinStage4.getStateToSQL()
	dinStage5.getStateToSQL()
	dinStage6.getStateToSQL()
	dinPump1.getStateToSQL()
#	dinPump2.getStateToSQL()												#удалить 2 насос
	tempBoiler.getStateToSQL()
	tempObratki.getStateToSQL()
	tempFloor1.getStateToSQL()
	tempOut.getStateToSQL()
	return True
"""функция обновления дополнительных опций из базы данных"""
def getSqlAddOptions() :
	optOnOff.getSQL()
	optMode.getSQL()
	optAutoPower.getSQL()
	optTimeout.getSQL()
	optTemp1.getSQL()
	optTempBack.getSQL()
	return True
"""функция выставления мощности котла всоответствии с задаными параметрами"""
def setPower() :
	if optAutoPower.state :
		"""автоматический режим"""
		if tempBoiler.state < 20 :
			doutStage1.setStateTrueToSQL()
			doutStage2.setStateTrueToSQL()
			doutStage3.setStateTrueToSQL()
			doutStage4.setStateFalseToSQL()
			doutStage5.setStateFalseToSQL()
			doutStage6.setStateFalseToSQL()
		elif tempBoiler.state > 20 and tempBoiler.state < 40 :
			doutStage1.setStateTrueToSQL()
			doutStage2.setStateTrueToSQL()
			doutStage3.setStateTrueToSQL()
			doutStage4.setStateFalseToSQL()
			doutStage5.setStateFalseToSQL()
			doutStage6.setStateFalseToSQL()
		elif tempBoiler.state > 40 and tempBoiler.state < 60 :
			doutStage1.setStateTrueToSQL()
			doutStage2.setStateTrueToSQL()
			doutStage3.setStateFalseToSQL()
			doutStage4.setStateFalseToSQL()
			doutStage5.setStateFalseToSQL()
			doutStage6.setStateFalseToSQL()
		elif tempBoiler.state > 60 and tempBoiler.state < 80 :
			doutStage1.setStateTrueToSQL()
			doutStage2.setStateFalseToSQL()
			doutStage3.setStateFalseToSQL()
			doutStage4.setStateFalseToSQL()
			doutStage5.setStateFalseToSQL()
			doutStage6.setStateFalseToSQL()
		else :
			doutStage1.setStateFalseToSQL()
			doutStage2.setStateFalseToSQL()
			doutStage3.setStateFalseToSQL()
			doutStage4.setStateFalseToSQL()
			doutStage5.setStateFalseToSQL()
			doutStage6.setStateFalseToSQL()
		if not logBloking['autoPowerOn'] :
			log.addLog('включен режим автоматической регулировки мощности котла')
			logBloking['autoPowerOn'] = True
			logBloking['autoPowerOff'] = False
	else :
		"""ручной режим"""
		doutStage1.setStateToSQL()
		doutStage2.setStateToSQL()
		doutStage3.setStateToSQL()
		doutStage4.setStateToSQL()
		doutStage5.setStateToSQL()
		doutStage6.setStateToSQL()
		if not logBloking['autoPowerOff'] :
			log.addLog('включен режим ручной регулировки мощности котла')
			logBloking['autoPowerOff'] = True
			logBloking['autoPowerOn'] = False
"""функция отключения мощности котла"""
def offPower() :
	doutStage1.setStateFalse()
	doutStage2.setStateFalse()
	doutStage3.setStateFalse()
	doutStage4.setStateFalse()
	doutStage5.setStateFalse()
	doutStage6.setStateFalse()
"""обновление таблицы исходящих сигналов в соответствии с положением GPIO контактов"""
def updateBdDout() :
	doutOnOff.getStateToSQL()
	doutPump1.getStateToSQL()
	doutOverheating.getStateToSQL()

"""алгоритм работы котла по температуре обратки"""
def kotelAlgBack() :
	setPower()										#выставление мощности котла
	doutOnOff.setStateTrue()						#включение главного пускателя
	doutPump1.setStateTrue()						#включение насоса
	
	if tempObratki.state < optTempBack.state-(optDeltaBack.state/2) and tempBoiler.state<90 :
		doutOverheating.setStateTrue()				#включение котла
		if not logBloking['floor1On'] :
			log.addLog('тепература упала до '+str(tempObratki.state)+'°C. Включено отопление.')
			logBloking['floor1On'] = True
			logBloking['floor1Off'] = False
		if tempBoiler.state < 90 :
			logBloking['overheating'] = False		#разрешение логирования перегрева котла
	elif tempObratki.state > optTempBack.state+(optDeltaBack.state/2) or tempBoiler.state>90 :
		doutOverheating.setStateFalse()				#отключение котла
		if not logBloking['floor1Off'] :
			log.addLog('тепература  поднялась до '+str(tempObratki.state)+'°C. Отопление отключено.')
			logBloking['floor1Off'] = True
			logBloking['floor1On'] = False
		if tempBoiler.state > 90 :
			if not logBloking['overheating'] :
				log.addLog('Высокая температура котла!!! Котел временно отключен!!!', 'ERROR')
				logBloking['overheating'] = True	#запрет логирования перегрева котла

"""алгоритм работы котла по температуре комнаты"""
def kotelAlgRoom() :
	setPower()										#выставление мощности котла
	doutOnOff.setStateTrue()
	
	if tempFloor1.state < optTemp1.state-(optDeltaTemp1.state/2) :
		doutPump1.setStateTrue()
		if not logBloking['floor1On'] :
			log.addLog('тепература упала до '+str(tempFloor1.state)+'°C. Включено отопление.')
			logBloking['floor1On'] = True
			logBloking['floor1Off'] = False
	elif tempFloor1.state > optTemp1.state+(optDeltaTemp1.state/2) :
		doutPump1.setStateFalse()
		if not logBloking['floor1Off'] :
			log.addLog('тепература  поднялась до '+str(tempFloor1.state)+'°C. Отопление отключено.')
			logBloking['floor1Off'] = True
			logBloking['floor1On'] = False
	if dinPump1.getState() :
		if tempBoiler.state < 90 :
			doutOverheating.setStateTrue()
			logBloking['overheating'] = False 		#разрешение логирования перегрева
		else :
			doutOverheating.setStateFalse()
			if not logBloking['overheating'] :
				log.addLog('Высокая температура котла!!! Котел временно отключен!!!', 'ERROR')
				logBloking['overheating'] = True	#запрет логирования перегрева котла
	else :
		if tempBoiler.state > 90 :
			if not logBloking['overheating'] :
				log.addLog('Высокая температура котла!!! Котел временно отключен!!!', 'ERROR')
				logBloking['overheating'] = True	#запрет логирования перегрева котла
		doutOverheating.setStateFalse()

"""выбор режима работы котла"""
def kotelModeOn() :
	if optMode.state :														#если режим котла по температуре обратки
		kotelAlgBack()														#включение котла по температуре обратки
		if not logBloking['modeBack'] :
			log.addLog('включен режим работы по температуре обратки.')
			logBloking['modeBack'] = True
			logBloking['modeRoom'] = False
	else :																	#иначе
		kotelAlgRoom()														#включение котла по температуре комнаты
		if not logBloking['modeRoom'] :
			log.addLog('включен режим работы по температуре комнаты')
			logBloking['modeRoom'] = True
			logBloking['modeBack'] = False
"""отключение котла"""
def kotelOff() :
	doutOnOff.setStateFalse()
	doutOverheating.setStateFalse()
	offPower()
	doutPump1.setStateFalse()

log.addLog("запуск программного обеспечения")
def tackt() :
	setSqlSistemParamiter()
	getSqlAddOptions()
	if optOnOff.state :
		if not optTimeout.state :
			kotelModeOn()
		else :
			if not timeout.getSQL() :
				kotelModeOn()
				logBloking['timeout'] = False
			else :
				kotelOff()
				if not logBloking['timeout'] :
					log.addLog('Котел отключен на время таймаута.')
					logBloking['timeout'] = True
	else :
		kotelOff()
	updateBdDout()