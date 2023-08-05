from pandas import pandas as pd
from matplotlib import pyplot as plt
from speedtest import Speedtest


class Speedevo:
	__slots__ = ['servers', 'threads', 'speed', 'path']

	def __init__(self):
		self.servers = [16438]  # Local do servidor
		self.threads = 16  # Quantidade de threads que vai ser utilizada
		self.speed = Speedtest()
		self.path = None

		try:
			self.speed.get_servers(self.servers)
		except Exception:
			self.speed.get_closest_servers()
			self.speed.get_best_server()

	"""
	Parametros
	----------
	Nome do arquivo: str
		Nome do arquivo onde ira armazenar as informações em .xlxs
		Nome do arquivo não pode ser vazio
	"""

	def speed_test(self, name_file=str):
		self.speed.download(threads=self.threads)  # threads de download
		self.speed.upload(threads=self.threads)  # threads de upload
		self.speed.results.share()

		results_dict = {
			'Download': [self.speed.results.download],
			'Upload': [self.speed.results.upload],
			'Ping': [self.speed.results.ping],
			'Server': [self.speed.results.server],
			'Times Tamp': [self.speed.results.timestamp],
			'Bytes Sent': [self.speed.results.bytes_sent],
			'Bytes Received': [self.speed.results.bytes_received],
			'Share': [self.speed.results.share],
			'Client': [self.speed.results.client],
		}

		dice = pd.DataFrame(data=results_dict)
		self.path = name_file + '.xlsx'
		print(self.path)

		try:
			file = open(self.path, mode='x', encoding='UTF8')
			file.close()

			with open(self.path, mode='w', newline='', encoding='UTF8'):
				dice.to_excel(self.path)

		except IOError:
			with open(self.path, mode='a', newline='', encoding='UTF8'):
				previous = pd.read_excel(self.path)
				previous = previous.drop(columns=['Unnamed: 0'])
				previous.head()
				new = pd.concat((previous, dice), axis=0, ignore_index=True)
				new.to_excel(self.path)

	"""
	Parametros
	----------
	Nome do arquivo: str
		Nome do arquivo onde ira armazenar as informações em .xlxs
		Nome do arquivo não pode ser vazio
	histogram: str
		Nome da coluna que deseja visualizar
	"""

	def histogram(self, name_file=str, columns=str):
		previous = pd.read_excel(name_file + '.xlsx')
		plt.hist(previous[columns], bins=20)
		plt.show()
