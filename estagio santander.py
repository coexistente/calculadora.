import pandas as pd
import matplotlib.pyplot as plt


file_path = "base_Investidores.csv"  
df = pd.read_csv(file_path, sep=';')


colunas_numericas = ['Posicao_Atual', 'Rentabilidade_12M', 'Aportes_12M', 'Resgates_12M']

for col in colunas_numericas:
    df[col] = (
        df[col]
        .astype(str)
        .str.replace('.', '', regex=False)  
        .str.replace(',', '.', regex=False)  
        .astype(float)
    )

estatisticas = df.describe(include='all')
print("\n=== Estatísticas da base ===")
print(estatisticas)


plt.figure(figsize=(6, 4))
df['Perfil'].value_counts().plot(kind='bar', color='skyblue')
plt.title("Distribuição de Perfis de Investidores")
plt.ylabel("Quantidade")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

print( )


plt.figure(figsize=(6, 4))
df.groupby('Perfil')['Rentabilidade_12M'].mean().plot(kind='bar', color='orange')
plt.title("Rentabilidade Média (12M) por Perfil")
plt.ylabel("% ao ano")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

print( )


plt.figure(figsize=(6, 4))
df.groupby('Classe_Ativo')['Posicao_Atual'].mean().plot(kind='bar', color='green')
plt.title("Patrimônio Médio por Classe de Ativo")
plt.ylabel("R$")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

print( )

plt.figure(figsize=(8, 5))
df['Estado'].value_counts().plot(kind='bar', color='purple')
plt.title("Quantidade de Clientes por Estado")
plt.xlabel("Estado")
plt.ylabel("Quantidade")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()




print( )





media_rent = df['Rentabilidade_12M'].mean()


plt.figure(figsize=(10, 6))
plt.hist(df['Rentabilidade_12M'], bins=15, color='skyblue', edgecolor='black', alpha=0.8)


plt.axvline(media_rent, color='red', linestyle='--', linewidth=2, label=f"Média: {media_rent:.2f}%")


plt.title("Distribuição da Rentabilidade dos Clientes (12M)", fontsize=14, fontweight='bold')
plt.xlabel("Rentabilidade (%)", fontsize=12)
plt.ylabel("Quantidade de Clientes", fontsize=12)
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
print( )



media_aporte = df['Aportes_12M'].mean()


plt.figure(figsize=(10, 6))
plt.hist(df['Aportes_12M'], bins=15, color='lightgreen', edgecolor='black', alpha=0.8)


plt.axvline(media_aporte, color='red', linestyle='--', linewidth=2, label=f"Média: R$ {media_aporte:,.2f}")


plt.title("Distribuição dos Aportes dos Clientes (12M)", fontsize=14, fontweight='bold')
plt.xlabel("Aportes (R$)", fontsize=12)
plt.ylabel("Quantidade de Clientes", fontsize=12)
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()

print( )





media_resgate = df['Resgates_12M'].mean()


plt.figure(figsize=(10, 6))
plt.hist(df['Resgates_12M'], bins=15, color='salmon', edgecolor='black', alpha=0.8)


plt.axvline(media_resgate, color='blue', linestyle='--', linewidth=2, label=f"Média: R$ {media_resgate:,.2f}")


plt.title("Distribuição dos Resgates dos Clientes (12M)", fontsize=14, fontweight='bold')
plt.xlabel("Resgates (R$)", fontsize=12)
plt.ylabel("Quantidade de Clientes", fontsize=12)
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()


print( )






df['Idade'] = pd.to_numeric(df['Idade'], errors='coerce')


clientes_unicos = (
    df[['ID_Cliente', 'Idade', 'Classe_Ativo']]
    .dropna(subset=['Idade', 'Classe_Ativo'])
    .drop_duplicates(subset='ID_Cliente', keep='first')
)


bins = [0, 25, 35, 45, 55, 65, 200]
labels = ['Até 25', '26-35', '36-45', '46-55', '56-65', '65+']
clientes_unicos['Faixa_Etaria'] = pd.cut(clientes_unicos['Idade'], bins=bins, labels=labels, right=True)


tabela_faixa_ativo = clientes_unicos.groupby(['Faixa_Etaria', 'Classe_Ativo'])['ID_Cliente'].count().unstack(fill_value=0)


tabela_faixa_ativo.plot(kind='bar', stacked=True, figsize=(10, 6), colormap='tab20')
plt.title("Faixa Etária x Classe de Ativo")
plt.xlabel("Faixa Etária")
plt.ylabel("Quantidade de Clientes")
plt.legend(title="Classe de Ativo", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()


print(tabela_faixa_ativo)


clientes_unicos = (
    df[['ID_Cliente', 'Perfil', 'Fundo', 'Classe_Ativo']]
    .drop_duplicates(subset='ID_Cliente', keep='first')
)


perfil_counts = clientes_unicos['Perfil'].value_counts()

plt.figure(figsize=(6,4))
perfil_counts.plot(kind='bar', color='skyblue')
plt.title("Perfis Predominantes na Carteira")
plt.ylabel("Quantidade de Clientes")
plt.xticks(rotation=45)
for i, v in enumerate(perfil_counts.values):
    plt.text(i, v, str(v), ha='center', va='bottom')
plt.tight_layout()
plt.show()

print("Perfis mais comuns:")
print(perfil_counts)


fundo_counts = clientes_unicos['Fundo'].value_counts()

plt.figure(figsize=(8,4))
fundo_counts.head(10).plot(kind='bar', color='orange')
plt.title("Top 10 Fundos Mais Investidos")
plt.ylabel("Quantidade de Clientes")
plt.xticks(rotation=45, ha='right')
for i, v in enumerate(fundo_counts.head(10).values):
    plt.text(i, v, str(v), ha='center', va='bottom', fontsize=8)
plt.tight_layout()
plt.show()

print("\nFundos mais comuns:")
print(fundo_counts.head(10))


classe_counts = clientes_unicos['Classe_Ativo'].value_counts()

plt.figure(figsize=(6,4))
classe_counts.plot(kind='bar', color='green')
plt.title("Classes de Ativo Predominantes")
plt.ylabel("Quantidade de Clientes")
plt.xticks(rotation=45)
for i, v in enumerate(classe_counts.values):
    plt.text(i, v, str(v), ha='center', va='bottom')
plt.tight_layout()
plt.show()

print("\nClasses de ativo mais comuns:")
print(classe_counts)


perfil_top = df['Perfil'].value_counts().idxmax()


classe_top = df['Classe_Ativo'].value_counts().idxmax()


estado_top = df.groupby('Estado')['Posicao_Atual'].sum().idxmax()


rent_media = df['Rentabilidade_12M'].mean()

print("\n===== RESUMO DA ANÁLISE =====")
print(f"Perfil mais comum: {perfil_top}")
print(f"Classe de ativo predominante: {classe_top}")
print(f"Estado com maior patrimônio total: {estado_top}")
print(f"Rentabilidade média dos clientes: {rent_media:.2f}% ao ano")


print("\n===== RECOMENDAÇÃO =====")
if rent_media < 5:
    print("A rentabilidade média está baixa. Considere revisar a alocação de ativos e buscar fundos com melhor desempenho.")
else:
    print("A rentabilidade média está positiva. Avalie manter a alocação atual e monitorar oportunidades de diversificação.")

