# Processamento dos Dados

## bibliotecas utilizadas
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

## carregamento e previa dos dados
df = pd.read_csv('cursos-prouni.csv',  encoding = 'ISO-8859-1', sep=';')
df_size = len(df)
col_size = len(df.columns)
print(f'\033[1m O dataset possui',df_size,'registros organizados em',col_size,'colunas.\033[0m\r\n')
df.head()

## detalhamento da estrutura de dados
print('\033[1m Abaixo temos um detalhamento da estrutura completa:\033[0m\r\n')
df.info()

# Limpeza e Transformacao

## calculo dos valores
col_nul_size = len(df.columns[df.isnull().any()])
val_nul_size = df.isnull().sum().sum()
cel_size = np.product(df.shape)
val_pre_size = cel_size-val_nul_size
val_nul_per = round((val_nul_size/cel_size) * 100,2)

## montagem do grafico Dados Presentes x Faltantes
labels = 'Presentes', 'Faltantes'
sizes = [val_pre_size, val_nul_size]
explode = (0, 0.1) 
fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.2f%%', shadow=True, startangle=0)
ax1.axis('equal')
plt.title('Dados Presentes x Faltantes')
plt.show()
print(f'Os dados faltantes representam',val_nul_per,'% do total de dados.')

## montagem do grafico Em quais colunas faltam dados?
data = df.isnull().sum()
plt.rcdefaults()
fig, ax = plt.subplots()
cols = len(df.columns)
y_pos = np.arange(cols)
ax.barh(y_pos, data, align='center')
ax.set_yticks(y_pos)
ax.set_yticklabels(df.columns)
ax.invert_yaxis() 
ax.set_xlabel('Linhas com valores faltantes')
ax.set_ylabel('Cursos')
ax.set_title('Em quais colunas faltam dados?')
plt.show()
print(f'Das',col_size,'colunas existentes,',col_nul_size,'delas possuem valores faltantes.')

## remove colunas com muitos valores nulos e que nao sera possivel autocompletar
df_cl = df.drop(columns=['nota_integral_cotas','nota_parcial_ampla','nota_parcial_cotas'])

## remove colunas que nao serao utilizadas na analise
df_cl = df_cl.drop(columns=['curso_id','curso_busca','cidade_filtro','campus_nome','campus_external_id'])

## autocompleta valores
df_cl.bolsa_integral_cotas = df_cl.bolsa_integral_cotas.fillna(0)
df_cl.bolsa_integral_ampla = df_cl.bolsa_integral_ampla.fillna(0)
df_cl.bolsa_parcial_cotas = df_cl.bolsa_parcial_cotas.fillna(0)
df_cl.bolsa_parcial_ampla = df_cl.bolsa_parcial_ampla.fillna(0)

## removendo registros com valores nulos
df_cl = df_cl.dropna()

## mostra o total de linhas com valores faltantes por coluna
print('Total de linhas com valores faltantes por coluna: ')
df_cl.isnull().sum()

## ajusta as colunas para float
df_cl.mensalidade = df.mensalidade.str.replace(',', '.').astype(float)
df_cl.nota_integral_ampla = df.nota_integral_ampla.str.replace(',', '.').astype(float)
df_cl

# Analise

## montagem do grafico Cursos com maior procura
df_cl.nome.value_counts().nlargest(10).plot(kind='bar', figsize=(10,6), title='Cursos com maior procura')
plt.xlabel("Cursos")
plt.ylabel("Total")

## montagem do grafico Comparativo de Bolsas por Tipo Entre os Cursos
df_cl_bol = df_cl[((df_cl.nome=='Pedagogia') | (df_cl.nome=='Administração') | (df_cl.nome=='Ciências Contábeis'))]
df_cl_bol = df_cl_bol[['nome','bolsa_integral_cotas','bolsa_integral_ampla','bolsa_parcial_cotas','bolsa_parcial_ampla']]
df_cl_bol.groupby('nome').sum().plot(kind='bar', figsize=(10,6), title='Comparativo de Bolsas por Tipo Entre os Cursos', rot=0)
plt.xlabel("Cursos")
plt.ylabel("Total")

## montagem do grafico Cursos x Mensalidade
df_cl_men = df_cl[((df_cl.nome=='Pedagogia') | (df_cl.nome=='Administração') | (df_cl.nome=='Ciências Contábeis'))]
plt.figure(figsize=(10, 3))
sns.boxplot(y=df_cl_men.nome, x=df_cl_men.mensalidade).set(xlabel='Mensalidade', ylabel='Cursos')

## deatalhamento dos quartis do grafico Cursos x Mensalidade
df_cl_men[['nome','mensalidade']].groupby(by='nome').describe()

# Extras

## mapa de calor
df_corr = df_cl.corr()
sns.set(rc = {'figure.figsize':(6,3)})
sns.heatmap(df_corr, annot=True)

## correlacao entre mensalidade e nota_integral_ampla
plt.scatter(df_cl.mensalidade, df_cl.nota_integral_ampla)
plt.title('Mensalidade x Nota Integral Ampla')
plt.show()

## cursos com maior procura por estado
df_cl.uf_busca.value_counts().nlargest(5).plot(kind='bar', figsize=(10,6), title='Cursos com maior procura por estado')