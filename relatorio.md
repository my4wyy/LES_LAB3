# Relatório Final – Lab03: Caracterizando a atividade de code review no GitHub

## 1. Informações do grupo
- **Curso:** Engenharia de Software  
- **Disciplina:** Laboratório de Experimentação de Software  
- **Período:** 6º Período  
- **Professor:** Prof. Dr. João Paulo Carneiro Aramuni  
- **Membros do grupo:** Gabriel Faria, Joao Victor Salim, Lucas Garcia, Maisa Pires e Miguel Vieira

---

## 2. Introdução
Este laboratório investiga a atividade de code review em repositórios populares do GitHub, analisando fatores que influenciam no merge de Pull Requests e no número de revisões realizadas.  
Foram coletados dados de 3.616 PRs válidos dos 200 repositórios mais populares do GitHub, aplicando filtros para garantir que passaram por processo de review humano.

### Hipóteses informais
- **IH01:** PRs menores (menos arquivos e linhas modificadas) têm maior probabilidade de serem merged.  
- **IH02:** PRs com descrições mais detalhadas têm maior probabilidade de serem merged.  
- **IH03:** PRs que demoram mais tempo para serem analisados têm menor probabilidade de serem merged.  
- **IH04:** PRs com mais interações (comentários e participantes) têm maior probabilidade de serem merged.  
- **IH05:** PRs maiores requerem mais revisões.

---

## 3. Tecnologias e ferramentas utilizadas
- **Linguagens:** Python  
- **Bibliotecas:** requests, pandas, numpy, matplotlib, seaborn, scipy  
- **API:** GitHub REST API  
- **Análise Estatística:** Teste de correlação de Spearman  

---

## 4. Metodologia
### 4.1 Coleta de dados
Foram coletados dados dos 200 repositórios mais populares do GitHub (por número de estrelas).  
Para cada repositório, coletamos PRs que atendessem aos critérios:
- Status: MERGED ou CLOSED 
- Interações: ≥ 1 comentário ou review

### 4.2 Métricas definidas
**Tamanho:** Número de arquivos modificados, linhas adicionadas e removidas  
**Tempo:** Intervalo entre criação e fechamento/merge do PR  
**Descrição:** Número de caracteres no corpo da descrição  
**Interações:** Número de participantes, comentários e reviews  

### 4.3 Análise estatística
Utilizamos o **teste de correlação de Spearman** por ser adequado para:
- Dados não-paramétricos
- Distribuições assimétricas típicas de repositórios GitHub
- Robustez a outliers


---

## 5. Questões de pesquisa

### RQ01: Qual a relação entre o tamanho dos PRs e o feedback final das revisões?
Esta questão investiga se PRs menores têm maior probabilidade de serem merged. Analisamos número de arquivos modificados, linhas adicionadas e removidas como métricas de tamanho.

![Tamanho vs Status](results/rq01_tamanho_vs_status.png)

### RQ02: Qual a relação entre o tempo de análise dos PRs e o feedback final das revisões?  
Examina se PRs que demoram mais para serem analisados têm menor chance de serem integrados. O tempo é medido desde a criação até o fechamento/merge.

![Tempo vs Status](results/rq02_tempo_vs_status.png)

### RQ03: Qual a relação entre a descrição dos PRs e o feedback final das revisões?
Avalia se descrições mais detalhadas (maior número de caracteres) aumentam a probabilidade de merge, facilitando o entendimento pelos revisores.

![Descrição vs Status](results/rq03_descricao_vs_status.png)

### RQ04: Qual a relação entre as interações nos PRs e o feedback final das revisões?
Analisa se maior engajamento (comentários, reviews, participantes) está associado a maior taxa de merge dos PRs.

![Interações vs Status](results/rq04_interacoes_vs_status.png)

### RQ05: Qual a relação entre o tamanho dos PRs e o número de revisões realizadas?
Investiga se PRs maiores demandam mais rounds de revisão devido à maior complexidade e probabilidade de erros.

![Tamanho vs Revisões](results/rq05_tamanho_vs_revisoes.png)

### RQ06: Qual a relação entre o tempo de análise dos PRs e o número de revisões realizadas?
Examina se PRs que permanecem abertos por mais tempo acumulam mais revisões ao longo do processo.

![Tempo vs Revisões](results/rq06_tempo_vs_revisoes.png)

### RQ07: Qual a relação entre a descrição dos PRs e o número de revisões realizadas?
Avalia se descrições mais detalhadas resultam em menos revisões por facilitarem o entendimento inicial.

![Descrição vs Revisões](results/rq07_descricao_vs_revisoes.png)

### RQ08: Qual a relação entre as interações nos PRs e o número de revisões realizadas?
Analisa a relação entre comentários e a intensidade do processo de review.

![Interações vs Revisões](results/rq08_interacoes_vs_revisoes.png)  

---

## 6. Resultados


### 6.1 Estatísticas descritivas
- **Total de PRs analisados:** 3.616
- **PRs merged:** 2.007 (55.5%)
- **PRs closed:** 1.609 (44.5%)
- **Mediana de linhas modificadas:** 24
- **Mediana de tempo de análise:** 139.1 horas
- **Mediana de tamanho da descrição:** 424 caracteres

### 6.2 Gráficos por questão de pesquisa



#### Matriz de Correlação Geral
![Matriz de Correlação](results/matriz_correlacao.png)


### 6.3 Principais correlações encontradas

#### RQ01: Tamanho vs Status
- *Arquivos modificados:* r = 0.139 (p < 0.001) - Mais arquivos = maior chance de merge
- *Total de linhas:* r = 0.055 (p < 0.001) - Correlação fraca positiva
- *Linhas adicionadas:* r = 0.059 (p < 0.001) - Correlação fraca positiva
- *Linhas removidas:* r = 0.104 (p < 0.001) - Correlação fraca positiva

#### RQ02: Tempo vs Status  
- *Tempo de análise:* r = -0.355 (p < 0.001) - *Correlação negativa forte*
  - PRs merged: mediana 51.7 horas
  - PRs closed: mediana 587.4 horas

#### RQ03: Descrição vs Status
- *Tamanho da descrição:* r = -0.005 (p = 0.749) - Sem correlação significativa
  - PRs merged: mediana 419 caracteres
  - PRs closed: mediana 431 caracteres

#### RQ04: Interações vs Status
- *Review comments:* r = 0.196 (p < 0.001) - Mais reviews = maior chance de merge
- *Comments:* r = -0.061 (p < 0.001) - Mais comentários = menor chance de merge
- *Participantes:* sem correlação significativa

#### RQ05: Tamanho vs Revisões
- *Linhas adicionadas:* r = 0.298 (p < 0.001) - *Correlação mais forte*
- *Total de linhas:* r = 0.270 (p < 0.001)
- *Arquivos modificados:* r = 0.239 (p < 0.001)
- *Linhas removidas:* r = 0.140 (p < 0.001)

#### RQ06: Tempo vs Revisões
- *Tempo de análise:* r = 0.096 (p < 1e-8) - Correlação muito fraca (significativa)

#### RQ07: Descrição vs Revisões  
- *Tamanho da descrição:* r = 0.156 (p < 0.001) - Correlação fraca positiva

#### RQ08: Interações vs Revisões
- *Comments vs Reviews:* r = 0.067 (p = 5.0e-05) - Correlação muito fraca positiva
- *Participantes vs Reviews:* sem correlação

---

## 7. Discussão
A análise revelou padrões importantes na atividade de code review no GitHub:

### 7.1 Principais achados

*Tempo é o fator mais determinante:* A correlação mais forte encontrada (r = -0.355) foi entre tempo de análise e probabilidade de merge. PRs que demoram mais para serem analisados têm menor chance de serem integrados.

*Tamanho influencia revisões:* PRs maiores (mais linhas adicionadas) requerem significativamente mais revisões (r = 0.298), confirmando a hipótese IH05.

*Reviews vs Comments:* Interessantemente, review comments aumentam a chance de merge (r = 0.196), enquanto comments gerais a diminuem (r = -0.061), sugerindo que feedback estruturado é mais efetivo.

### 7.2 Validação das hipóteses

- *IH01 (PRs menores → maior merge):* *NÃO CONFIRMADA* - Correlações observadas indicam leve tendência oposta (PRs maiores com chance um pouco maior de merge).
- *IH02 (Descrições detalhadas → maior merge):* *NÃO CONFIRMADA* - Sem correlação significativa entre tamanho da descrição e merge.
- *IH03 (Tempo longo → menor merge):* *CONFIRMADA* - Correlação negativa forte (r = -0.355).
- *IH04 (Mais interações → maior merge):* *PARCIALMENTE CONFIRMADA* - Depende do tipo de interação (reviews aumentam chance; comments gerais reduzem levemente).
- *IH05 (PRs maiores → mais revisões):* *CONFIRMADA* - Correlação positiva (r ≈ 0.27–0.30 para tamanho).

---

## 8. Conclusão
O estudo de 3.616 PRs de repositórios populares do GitHub revelou que:

1. *O tempo de análise é o fator mais crítico* para o sucesso de um PR (r = -0.355)
2. *PRs maiores demandam mais revisões*, mas não necessariamente são rejeitados
3. *A qualidade das interações importa mais que a quantidade* (reviews > comments)
4. *Descrições detalhadas aumentam ligeiramente as chances de merge*

A taxa geral de merge de 55.5% indica um processo seletivo, mas equilibrado nos repositórios analisados.

---

## 9. Referências
- GitHub REST API: https://docs.github.com/en/rest  
- Pandas: https://pandas.pydata.org/  
- Matplotlib: https://matplotlib.org/  
- Seaborn: https://seaborn.pydata.org/  
- SciPy: https://scipy.org/  

---

## 10. Apêndices
- Scripts em scripts/  
- Dataset em data/pull_requests.csv
- Resultados detalhados em results/analysis_results.json
- Visualizações em results/*.png
