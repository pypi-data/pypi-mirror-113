import csv


CANTO = '+'
LADOS = '|'
LINHA = '-'
QUEBRA = '\n'
ESPACO = ' '
class PyTabela(object):
	"""AUTHOR: 
		PABLO DUARTE SILVA E VITORIA KAROLINA FERREIRA SOUSA
	COPYRIGHT:
	 	"Copyright 2021, Por Duarte Silva & VKFS"
	VERSION:
		"1.0"
	STATUS:
		"Production"
	"""
	__slots__ = ["_campo", "_tabela", "_nColunas", "_maxLargura"]

	def __init__(self) -> None:
		self._campo = []			#	Lista de colunas
		self._tabela = []			#	Lista que armazena as linhas
		self._nColunas = 0			#	Numero de colunas
		self._maxLargura = []		#	Lista que armazena a maior largura de cada coluna

	def __str__(self) -> str:
		tabela = ''
		if(len(self._campo) > 0):
			tabela += self._cabecalho(self._campo)

			for i in range(len(self._tabela)):
				tabela += self._corpo(self._tabela[i])

			tabela += self._estremidade()

		return tabela


	def _estremidade(self):
		cabeca = CANTO
		for i in range(self._nColunas):
			for _ in range(self._maxLargura[i] + 2):
				cabeca += LINHA
			cabeca += CANTO
		cabeca += QUEBRA
		return cabeca


	def _corpo(self, elementos = []) -> str:
		linha = LADOS
		for i in range(len(elementos)):
			j = 0
			largura = self._maxLargura[i] + 2
			elemento = str(elementos[i])
			while(j < largura):
				if(j == 0):
					linha += ESPACO
					j += 1

				elif((j - 1) < len(elemento)):
					linha = linha + elemento
					j += len(elemento)

				else:
					linha += ESPACO
					j += 1
			linha += LADOS
		linha += QUEBRA
		return linha

	def _cabecalho(self, campos: list) -> str:
		cabecalho = ''
		cabecalho += self._estremidade()
		cabecalho += self._corpo(campos)
		cabecalho += self._estremidade()
		return cabecalho



	def addCampos(self, campo: list) -> None:
		"""DESCRIPTION: Função para adicionar o nome de cada coluna utilizada na tabela"""
		try:
			assert (len(campo) > 0)
			self._nColunas = len(campo)
			for i in campo:
				self._maxLargura.append(len(i))

			self._campo = campo
			self._tabela = []
		except AssertionError:
			raise Exception("Campo Inválido")




	def addLinha(self, linha: list) -> None:
		"""DESCRIPTION: Usado para adicionar as linhas da tabela com todos os campos adicionados na
		função anterior"""
		try:
			assert len(linha) == self._nColunas
			for i in range(self._nColunas):
				if(len(str(linha[i])) > self._maxLargura[i]):
					self._maxLargura[i] = len(str(linha[i]))

			self._tabela.append(linha)
		except AssertionError:
			raise Exception("Número de elementos na linha incompativel com o número de campos")


	def saveTabela(self, nomeArquivo: str) -> None:
		"""DESCRIPTION: É usado para salvar a tabela após preenchimento da mesma"""
		try:
			arquivo = open(nomeArquivo, 'w', newline='', encoding='utf-8')
		except:
			raise Exception("Falha ao criar arquivo")

		w = csv.writer(arquivo)
		w.writerow(self._campo)
		for i in range(len(self._tabela)):
			lista = self._tabela[i]
			w.writerow(lista)
		arquivo.close()

	def loadTabela(self, nomeArquivo: str) -> None:
		"""DESCRIPTION: Função utilizada para carregamento de dados de arquivos existentes """
		try:
			arquivo = open(nomeArquivo, encoding='utf-8')
		except:
			raise Exception("Arquivo ou diretório não encontrado")

		r = csv.reader(arquivo, delimiter=",")
		lista = []
		for i in r:
			if lista == []:
				lista = i
				self.addCampos(lista)
			else:
				lista = i
				self.addLinha(lista)
