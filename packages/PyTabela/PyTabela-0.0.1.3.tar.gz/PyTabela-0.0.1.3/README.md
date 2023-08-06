# Pytabela

Uma biblioteca com o intuito de gerar tabelas automaticamente.

## Instalação

### Instalação via pip:

```sh
python -m pip install -U PyTabela
```
## Como Usar

### Importação
```python
from pyTabela import pyTabela
x = pyTabela.PyTabela()
```
### Adição dos campos
```python
x.addCampos(["id", "nome", "sobrenome"])
```
### Adição das linhas
```python
x.addLinha([1, "Pablo", "Silva"])
```

Voce pode adicionar uma linha a qualquer momento, mas é necessario adicionar o nome dos campos primeiramente com `addCampos`.
```python
x = pyTabela.PyTabela()
x.addCampos(["id", "nome", "sobrenome"])
x.addLinha([1, "Pablo", "Silva"])
x.addLinha([2, "Vitória", "Karolina"])
x.addLinha([3, "Fulano", "de Tal"])
print(x)
```

### Exemplo de Mostragem

```txt
+----+---------+-----------+
| id | nome    | sobrenome |
+----+---------+-----------+
| 1  | Pablo   | Silva     |
| 2  | Vitória | Karolina  |
| 3  | Fulano  | de Tal    |
+----+---------+-----------+
```

### Exportar para CSV
```python
a.saveTabela("Nome_Do_Arquivo.csv")
```
### Importar de um arquivo CSV
```python
a.loadTabela("Nome_Do_Arquivo.csv")
```

