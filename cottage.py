import sys
sys.path.append('/srv/root/py/config')
import mySQLconfig
sys.path.append('/srv/root/py/moduls/modulLib')
import gpioInOut, temperatureIn, wifiTemperatureIn, kotelOption, kotelTimeout, kotelLog, ds2408
sys.path.append('/srv/root/py/moduls')
import kotel, temperature, pollds2408

while True :
	kotel.tackt()
	temperature.tackt()
	pollds2408.tackt()