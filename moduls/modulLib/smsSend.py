import urllib.request

class SMSSend() :
	def __init__(self) :
		self.url = "http://sms.ru/sms/send" #URL отправки запроса
		self.data = {
			'api_id' : '9a9d843b-502a-5524-b1c1-63819eb0014f',
			'to' : '79261770280'
			}
	def send(self, text) :
		data = self.data
		data['text'] = text[:60]
		try :
			req = urllib.request.Request(url=self.url, data=urllib.parse.urlencode(data).encode())
			open = urllib.request.urlopen(req)
			string = open.read().decode('utf-8')
			if string[:3]=='100' :
				return True
			else :
				return False
		except:
			return False