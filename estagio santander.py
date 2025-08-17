import pandas as pd
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore")

file_path = "Base_Investidores.csv"  
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
contagem = df['Perfil'].value_counts()
plt.figure(figsize=(6, 7))
ax = contagem.plot(kind='bar', color='skyblue')
plt.title("Distribuição de Perfis de Investidores")
plt.ylabel("Quantidade")
plt.xticks(rotation=45)
for i, v in enumerate(contagem):
    ax.text(i, v + 0.5, str(v), ha='center', va='bottom')
plt.tight_layout()
plt.show()
print( )
rentabilidade_media = df.groupby('Perfil')['Rentabilidade_12M'].mean()
plt.figure(figsize=(7, 6))
ax = rentabilidade_media.plot(kind='bar', color='orange')
plt.title("Rentabilidade Média (12M) por Perfil")
plt.ylabel("% ao ano")
plt.xticks(rotation=45)
for i, v in enumerate(rentabilidade_media):
    ax.text(i, v + 0.1, f"{v:.2f}%", ha='center', va='bottom')  
plt.tight_layout()
plt.show()
print( )
df['Rentabilidade_12M'] = (
    df['Rentabilidade_12M']
    .astype(str)
    .str.replace(',', '.', regex=False)
)
df['Rentabilidade_12M'] = pd.to_numeric(df['Rentabilidade_12M'], errors='coerce')
rentab_media = df.groupby('Classe_Ativo')['Rentabilidade_12M'].mean().sort_values(ascending=False)
plt.figure(figsize=(8,5))
ax = rentab_media.plot(kind='bar', color='teal')
plt.title("Rentabilidade Média (12M) por Classe de Ativo", fontsize=14)
plt.ylabel("Rentabilidade Média (%)", fontsize=12)
plt.xlabel("Classe de Ativo", fontsize=12)
plt.xticks(rotation=45)
for i, v in enumerate(rentab_media):
    ax.text(i, v + 0.1, f"{v:.2f}%", ha='center', fontsize=10, fontweight='bold')
plt.tight_layout()
plt.show()
print( )
df['Rentabilidade_12M'] = (
    df['Rentabilidade_12M']
    .astype(str)
    .str.replace(',', '.', regex=False)
)
df['Rentabilidade_12M'] = pd.to_numeric(df['Rentabilidade_12M'], errors='coerce')
rentab_media_perfil = (
    df.groupby(['Perfil', 'Classe_Ativo'])['Rentabilidade_12M']
    .mean()
    .unstack(fill_value=0)
)
plt.figure(figsize=(10,6))
rentab_media_perfil.plot(kind='bar', figsize=(10,6))
plt.title("Rentabilidade Média (12M) por Classe de Ativo e Perfil", fontsize=14)
plt.ylabel("Rentabilidade Média (%)", fontsize=12)
plt.xlabel("Perfil do Cliente", fontsize=12)
plt.xticks(rotation=0)
plt.legend(title="Classe de Ativo")
plt.tight_layout()
plt.show()
print( )
clientes_resgataram = df[df['Resgates_12M'] > 0].groupby('Perfil')['Resgates_12M'].count()
perfil_max_clientes = clientes_resgataram.idxmax()
quantidade_max_clientes = clientes_resgataram.max()
print(f"O perfil com mais clientes que resgataram nos últimos 12 meses foi: {perfil_max_clientes} ({quantidade_max_clientes} clientes)")
plt.figure(figsize=(6, 7))
ax = clientes_resgataram.plot(kind='bar', color='purple')
plt.title("Quantidade de Clientes que Resgataram nos Últimos 12 Meses por Perfil")
plt.ylabel("Quantidade de Clientes")
plt.xticks(rotation=45)
for i, v in enumerate(clientes_resgataram):
    ax.text(i, v + 0.5, str(v), ha='center', va='bottom')
plt.tight_layout()
plt.show()
print( )
clientes_que_aportaram = df[df['Aportes_12M'] > 0].groupby('Perfil')['Aportes_12M'].count()
perfil_max_clientes = clientes_que_aportaram.idxmax()
quantidade_max_clientes = clientes_que_aportaram.max()
print(f"O perfil com mais clientes que fizeram aportes nos últimos 12 meses foi: {perfil_max_clientes} ({quantidade_max_clientes} clientes)")
plt.figure(figsize=(6, 4))
ax = clientes_que_aportaram.plot(kind='bar', color='blue')
plt.title("Quantidade de Clientes que Fizeram Aportes nos Últimos 12 Meses por Perfil")
plt.ylabel("Quantidade de Clientes")
plt.xticks(rotation=45)
for i, v in enumerate(clientes_que_aportaram):
    ax.text(i, v + 0.5, str(v), ha='center', va='bottom')
plt.tight_layout()
plt.show()
print()
plt.figure(figsize=(8, 5))
df['Estado'].value_counts().plot(kind='bar', color='purple')
plt.title("Quantidade de Clientes por Estado")
plt.xlabel("Estado")
plt.ylabel("Quantidade")
plt.xticks(rotation=45)
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
print()
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
print()
print("Perfis mais comuns:")
print(classe_counts.to_string()) 
fundo_counts = clientes_unicos['Fundo'].value_counts()
plt.figure(figsize=(8,4))
fundo_counts.head(10).plot(kind='bar', color='orange')
plt.title("Os 10 Fundos Mais Investidos foram")
plt.ylabel("Quantidade de Clientes")
plt.xticks(rotation=45, ha='right')
for i, v in enumerate(fundo_counts.head(10).values):
    plt.text(i, v, str(v), ha='center', va='bottom', fontsize=8)
plt.tight_layout()
plt.show()
print("\nFundos mais comuns:")
print(classe_counts.to_string()) 
print( )
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
print()
print("\nClasses de ativo mais comuns:");
print(classe_counts.to_string()) 
perfil_top = df['Perfil'].value_counts().idxmax();
classe_top = df['Classe_Ativo'].value_counts().idxmax();
estado_top = df.groupby('Estado')['Posicao_Atual'].sum().idxmax();
rent_media = df['Rentabilidade_12M'].mean();
print()
print("\n===== RESUMO DA ANÁLISE =====")
print(f"O perfil mais comum foi: {perfil_top}")
print(f"A classe de ativo predominante e: {classe_top}")
print(f"Rentabilidade média dos clientes: {rent_media:.2f}% ao ano")

print("\n===== RECOMENDAÇÃO =====")
if rent_media < 8:
    print("A rentabilidade média tá baixa. E bom revisar a alocação de ativos e buscar fundos com melhor desempenho.")
else:
    print("A rentabilidade média tá positiva. E interessante manter a alocação atual e analisar novas oportunidades de diversificação.")

