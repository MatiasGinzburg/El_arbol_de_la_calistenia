import pandas as pd



matriz_ejericios = pd.read_csv('matrizEjercicios.csv',index_col=0)

#matriz_ejericios = matriz_ejericios.iloc[:, 1:]
print(matriz_ejericios)




relaciones = matriz_ejericios.isna()

print(relaciones.size)

ejercicios_ordenados=[]

while relaciones.size>0:

	ejercicios = relaciones.columns
	relaciones2 = relaciones.all(axis=0)


	ejercicios_ordenados.append(ejercicios[relaciones2])


	relaciones = relaciones.loc[~relaciones2,~relaciones2]


for i in range(len(ejercicios_ordenados)-1,-1,-1):
	print(ejercicios_ordenados[i])




