
import pandas as pd
import seaborn as sns

# Importa os dados coletados do TSE
url = "https://raw.githubusercontent.com/Fernandohf/Benford-s-Law/master/eleitores_2018_set.csv"
eleitores = pd.read_csv(url, header=0, encoding='latin-1', sep=";")


# Filtra os dados
eleitores = eleitores[["Município", "Quantidade"]]
eleitores = eleitores.dropna(axis=0)

# Remove os pontos nos valores numéricos
eleitores["Quantidade"] = eleitores.Quantidade.apply(lambda x: x.replace(".",""))


print("Total de Eleitores: " + str(eleitores.Quantidade.astype('float64').sum()))


# Função que coleta a frequência dos primeiros dígitos.
def fd_freq(df, col):
    """
    Retorna a distribuição dos primeiros dígitos da coluna especificada.

    > df: DataFrame de análise
    > col: Coluna que será analisada.
    < df_freq: DataFrame com os resultados;

    """
    # lista de dígitos 1...9
    digits = [str(d) for d in range(1, 10)]
    columns = ["Ocorrências", "Porcentagem"]
    df_freq = pd.DataFrame(index=digits, columns=columns)

    # Para cada dígito
    for d in digits:
        total = df[col].apply(lambda x: x[0] == d).sum()
        df_freq.loc[d, "Ocorrências"] = total
        df_freq.loc[d, "Porcentagem"] = total / df.shape[0]
    return df_freq

first_digit_freq = fd_freq(eleitores, "Quantidade")

import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Plot dos valores observados
x_o = first_digit_freq.index.values.astype(int)
y_o = first_digit_freq["Porcentagem"].values
plt.bar(x_o, y_o, label="Valores observados")

# Plot da Lei de Bendford
x = np.linspace(1, 9, 100)
y = np.log10(1 + (1/x))
plt.plot(x, y, label = "Lei de Benford", c='r')

ax = plt.gca()
ax.set_xticks(x_o)
ax.set_ylim((0, 1))
ax.set_xlim((0, 10))


plt.show()