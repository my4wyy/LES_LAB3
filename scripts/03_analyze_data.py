import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import spearmanr, pearsonr
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import spearmanr, pearsonr
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['font.size'] = 10
plt.rcParams['figure.figsize'] = (12, 8)

def load_and_prepare_data():
    print("Carregando dados...")
    df = pd.read_csv("data/pull_requests.csv")
    
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['closed_at'] = pd.to_datetime(df['closed_at'])
    df['merged_at'] = pd.to_datetime(df['merged_at'])
    
    df['analysis_time_hours'] = (df['closed_at'] - df['created_at']).dt.total_seconds() / 3600
    
    df['total_lines_changed'] = df['additions'] + df['deletions']
    
    df['total_interactions'] = df['comments'] + df['review_comments']
    
    df['is_merged'] = (df['state'] == 'closed') & (df['merged_at'].notna())
    
    df = df[df['analysis_time_hours'] >= 1]
    df = df[df['total_interactions'] > 0]
    
    print(f"Dataset preparado: {len(df)} PRs válidos")
    return df

def calculate_correlations(df):
    results = {}
    
    size_vars = ['changed_files', 'total_lines_changed', 'additions', 'deletions']
    time_var = 'analysis_time_hours'
    description_var = 'body_length'
    interaction_vars = ['participants_count', 'total_interactions', 'comments', 'review_comments']
    
    status_var = 'is_merged'
    review_count_var = 'review_comments'
    
    print("\n=== ANÁLISE: STATUS DO PR (MERGED vs CLOSED) ===")
    
    for var in size_vars:
        merged_data = df[df['is_merged'] == True][var]
        closed_data = df[df['is_merged'] == False][var]
        
        corr_spearman, p_spearman = spearmanr(df[var], df[status_var])
        corr_pearson, p_pearson = pearsonr(df[var], df[status_var])
        
        results[f'status_vs_{var}'] = {
            'spearman': corr_spearman,
            'spearman_p': p_spearman,
            'pearson': corr_pearson,
            'pearson_p': p_pearson,
            'merged_median': merged_data.median(),
            'closed_median': closed_data.median()
        }
    
    merged_time = df[df['is_merged'] == True][time_var]
    closed_time = df[df['is_merged'] == False][time_var]
    
    corr_spearman, p_spearman = spearmanr(df[time_var], df[status_var])
    corr_pearson, p_pearson = pearsonr(df[time_var], df[status_var])
    
    results[f'status_vs_{time_var}'] = {
        'spearman': corr_spearman,
        'spearman_p': p_spearman,
        'pearson': corr_pearson,
        'pearson_p': p_pearson,
        'merged_median': merged_time.median(),
        'closed_median': closed_time.median()
    }
    
    merged_desc = df[df['is_merged'] == True][description_var]
    closed_desc = df[df['is_merged'] == False][description_var]
    
    corr_spearman, p_spearman = spearmanr(df[description_var], df[status_var])
    corr_pearson, p_pearson = pearsonr(df[description_var], df[status_var])
    
    results[f'status_vs_{description_var}'] = {
        'spearman': corr_spearman,
        'spearman_p': p_spearman,
        'pearson': corr_pearson,
        'pearson_p': p_pearson,
        'merged_median': merged_desc.median(),
        'closed_median': closed_desc.median()
    }
    
    for var in interaction_vars:
        merged_data = df[df['is_merged'] == True][var]
        closed_data = df[df['is_merged'] == False][var]
        
        corr_spearman, p_spearman = spearmanr(df[var], df[status_var])
        corr_pearson, p_pearson = pearsonr(df[var], df[status_var])
        
        results[f'status_vs_{var}'] = {
            'spearman': corr_spearman,
            'spearman_p': p_spearman,
            'pearson': corr_pearson,
            'pearson_p': p_pearson,
            'merged_median': merged_data.median(),
            'closed_median': closed_data.median()
        }
    
    print("\n=== ANÁLISE: NÚMERO DE REVISÕES ===")
    
    for var in size_vars:
        corr_spearman, p_spearman = spearmanr(df[var], df[review_count_var])
        corr_pearson, p_pearson = pearsonr(df[var], df[review_count_var])
        
        results[f'reviews_vs_{var}'] = {
            'spearman': corr_spearman,
            'spearman_p': p_spearman,
            'pearson': corr_pearson,
            'pearson_p': p_pearson
        }
    
    corr_spearman, p_spearman = spearmanr(df[time_var], df[review_count_var])
    corr_pearson, p_pearson = pearsonr(df[time_var], df[review_count_var])
    
    results[f'reviews_vs_{time_var}'] = {
        'spearman': corr_spearman,
        'spearman_p': p_spearman,
        'pearson': corr_pearson,
        'pearson_p': p_pearson
    }
    
    corr_spearman, p_spearman = spearmanr(df[description_var], df[review_count_var])
    corr_pearson, p_pearson = pearsonr(df[description_var], df[review_count_var])
    
    results[f'reviews_vs_{description_var}'] = {
        'spearman': corr_spearman,
        'spearman_p': p_spearman,
        'pearson': corr_pearson,
        'pearson_p': p_pearson
    }
    
    for var in ['participants_count', 'comments']:
        corr_spearman, p_spearman = spearmanr(df[var], df[review_count_var])
        corr_pearson, p_pearson = pearsonr(df[var], df[review_count_var])
        
        results[f'reviews_vs_{var}'] = {
            'spearman': corr_spearman,
            'spearman_p': p_spearman,
            'pearson': corr_pearson,
            'pearson_p': p_pearson
        }
    
    return results

def create_visualizations(df):
    print("\nCriando visualizações...")
    
    plt.style.use('seaborn-v0_8')
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    merged_data = df[df['is_merged'] == True]
    closed_data = df[df['is_merged'] == False]
    
    axes[0,0].boxplot([merged_data['changed_files'], closed_data['changed_files']], 
                      labels=['Merged', 'Closed'])
    axes[0,0].set_title('Arquivos Modificados')
    axes[0,0].set_ylabel('Número de Arquivos')
    
    axes[0,1].boxplot([merged_data['additions'], closed_data['additions']], 
                      labels=['Merged', 'Closed'])
    axes[0,1].set_title('Linhas Adicionadas')
    axes[0,1].set_ylabel('Linhas Adicionadas')
    axes[0,1].set_yscale('log')
    
    axes[1,0].boxplot([merged_data['deletions'], closed_data['deletions']], 
                      labels=['Merged', 'Closed'])
    axes[1,0].set_title('Linhas Removidas')
    axes[1,0].set_ylabel('Linhas Removidas')
    axes[1,0].set_yscale('log')
    
    axes[1,1].boxplot([merged_data['total_lines_changed'], closed_data['total_lines_changed']], 
                      labels=['Merged', 'Closed'])
    axes[1,1].set_title('Total de Linhas Modificadas')
    axes[1,1].set_ylabel('Linhas Totais')
    axes[1,1].set_yscale('log')
    
    plt.suptitle('RQ01: Tamanho dos PRs vs Status Final', fontsize=16)
    plt.tight_layout()
    plt.savefig('results/rq01_tamanho_vs_status.png', dpi=300, bbox_inches='tight')
    plt.close()
    
   
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    
    ax.boxplot([merged_data['analysis_time_hours'], closed_data['analysis_time_hours']], 
               labels=['Merged', 'Closed'])
    ax.set_title('Distribuição do Tempo de Análise')
    ax.set_ylabel('Tempo (horas)')
    ax.set_yscale('log')
    
    plt.suptitle('RQ02: Tempo de Análise vs Status Final', fontsize=16)
    plt.tight_layout()
    plt.savefig('results/rq02_tempo_vs_status.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    
    ax.boxplot([merged_data['body_length'], closed_data['body_length']], 
               labels=['Merged', 'Closed'])
    ax.set_title('Tamanho da Descrição por Status')
    ax.set_ylabel('Caracteres na Descrição')
    
    plt.suptitle('RQ03: Descrição dos PRs vs Status Final', fontsize=16)
    plt.tight_layout()
    plt.savefig('results/rq03_descricao_vs_status.png', dpi=300, bbox_inches='tight')
    plt.close()
    

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    

    axes[0].boxplot([merged_data['comments'], closed_data['comments']], 
                    labels=['Merged', 'Closed'])
    axes[0].set_title('Comentários por Status')
    axes[0].set_ylabel('Número de Comentários')
    
    axes[1].boxplot([merged_data['review_comments'], closed_data['review_comments']], 
                    labels=['Merged', 'Closed'])
    axes[1].set_title('Review Comments por Status')
    axes[1].set_ylabel('Número de Reviews')
    
    axes[2].boxplot([merged_data['total_interactions'], closed_data['total_interactions']], 
                    labels=['Merged', 'Closed'])
    axes[2].set_title('Total de Interações por Status')
    axes[2].set_ylabel('Interações Totais')
    
    plt.suptitle('RQ04: Interações nos PRs vs Status Final', fontsize=16)
    plt.tight_layout()
    plt.savefig('results/rq04_interacoes_vs_status.png', dpi=300, bbox_inches='tight')
    plt.close()

    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    axes[0,0].scatter(df['changed_files'], df['review_comments'], alpha=0.6, color='#1f77b4')
    axes[0,0].set_xlabel('Arquivos Modificados')
    axes[0,0].set_ylabel('Número de Reviews')
    axes[0,0].set_title('Arquivos vs Reviews')
    
    axes[0,1].scatter(df['additions'], df['review_comments'], alpha=0.6, color='#1f77b4')
    axes[0,1].set_xlabel('Linhas Adicionadas')
    axes[0,1].set_ylabel('Número de Reviews')
    axes[0,1].set_title('Adições vs Reviews')
    axes[0,1].set_xscale('log')
    
    axes[1,0].scatter(df['deletions'], df['review_comments'], alpha=0.6, color='#1f77b4')
    axes[1,0].set_xlabel('Linhas Removidas')
    axes[1,0].set_ylabel('Número de Reviews')
    axes[1,0].set_title('Remoções vs Reviews')
    axes[1,0].set_xscale('log')
    
    axes[1,1].scatter(df['total_lines_changed'], df['review_comments'], alpha=0.6, color='#1f77b4')
    axes[1,1].set_xlabel('Total de Linhas Modificadas')
    axes[1,1].set_ylabel('Número de Reviews')
    axes[1,1].set_title('Total de Linhas vs Reviews')
    axes[1,1].set_xscale('log')
    
    plt.suptitle('RQ05: Tamanho dos PRs vs Número de Revisões', fontsize=16)
    plt.tight_layout()
    plt.savefig('results/rq05_tamanho_vs_revisoes.png', dpi=300, bbox_inches='tight')
    plt.close()

    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    axes[0].scatter(df['analysis_time_hours'], df['review_comments'], alpha=0.6, color='#1f77b4')
    axes[0].set_xlabel('Tempo de Análise (horas)')
    axes[0].set_ylabel('Número de Reviews')
    axes[0].set_title('Tempo vs Reviews - Visão Geral')
    axes[0].set_xscale('log')

    time_bins = pd.cut(df['analysis_time_hours'], bins=10)
    binned_reviews = df.groupby(time_bins)['review_comments'].mean()
    bin_centers = [(interval.left + interval.right) / 2 for interval in binned_reviews.index]
    
    axes[1].plot(bin_centers, binned_reviews.values, marker='o', linewidth=2, markersize=8, color='#1f77b4')
    axes[1].set_xlabel('Tempo de Análise (horas) - Médias por Faixa')
    axes[1].set_ylabel('Média de Reviews')
    axes[1].set_title('Tendência: Tempo vs Reviews')
    axes[1].set_xscale('log')
    
    plt.suptitle('RQ06: Tempo de Análise vs Número de Revisões', fontsize=16)
    plt.tight_layout()
    plt.savefig('results/rq06_tempo_vs_revisoes.png', dpi=300, bbox_inches='tight')
    plt.close()

    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    axes[0].scatter(df['body_length'], df['review_comments'], alpha=0.6, color='#1f77b4')
    axes[0].set_xlabel('Tamanho da Descrição (caracteres)')
    axes[0].set_ylabel('Número de Reviews')
    axes[0].set_title('Descrição vs Reviews - Todos os PRs')

    desc_bins = pd.cut(df['body_length'], bins=8)
    binned_desc_reviews = df.groupby(desc_bins)['review_comments'].mean()
    bin_centers_desc = [(interval.left + interval.right) / 2 for interval in binned_desc_reviews.index]
    
    axes[1].plot(bin_centers_desc, binned_desc_reviews.values, marker='s', linewidth=2, markersize=8, color='#1f77b4')
    axes[1].set_xlabel('Tamanho da Descrição (caracteres) - Médias por Faixa')
    axes[1].set_ylabel('Média de Reviews')
    axes[1].set_title('Tendência: Descrição vs Reviews')
    
    plt.suptitle('RQ07: Descrição dos PRs vs Número de Revisões', fontsize=16)
    plt.tight_layout()
    plt.savefig('results/rq07_descricao_vs_revisoes.png', dpi=300, bbox_inches='tight')
    plt.close()

    fig, ax = plt.subplots(1, 1, figsize=(10, 6))

    ax.scatter(df['comments'], df['review_comments'], alpha=0.6, color='#1f77b4')
    ax.set_xlabel('Número de Comentários')
    ax.set_ylabel('Número de Reviews')
    ax.set_title('Comentários vs Reviews')
    
    plt.suptitle('RQ08: Interações vs Número de Revisões', fontsize=16)
    plt.tight_layout()
    plt.savefig('results/rq08_interacoes_vs_revisoes.png', dpi=300, bbox_inches='tight')
    plt.close()

    correlation_vars = ['total_lines_changed', 'analysis_time_hours', 'body_length', 
                       'total_interactions', 'review_comments', 'is_merged']
    corr_matrix = df[correlation_vars].corr()
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
                square=True, fmt='.3f')
    plt.title('Matriz de Correlação entre Variáveis')
    plt.tight_layout()
    plt.savefig('results/matriz_correlacao.png', dpi=300, bbox_inches='tight')
    plt.close()

def generate_statistics_summary(df, results):
    """Gera resumo estatístico dos dados"""
    print("\nGerando resumo estatístico...")
    
    summary = {
        'dataset_info': {
            'total_prs': len(df),
            'merged_prs': len(df[df['is_merged'] == True]),
            'closed_prs': len(df[df['is_merged'] == False]),
            'merge_rate': len(df[df['is_merged'] == True]) / len(df) * 100
        },
        'medians': {
            'total_lines_changed': df['total_lines_changed'].median(),
            'analysis_time_hours': df['analysis_time_hours'].median(),
            'body_length': df['body_length'].median(),
            'total_interactions': df['total_interactions'].median(),
            'review_comments': df['review_comments'].median(),
            'participants_count': df['participants_count'].median()
        },
        'correlations': results
    }
    
    return summary

def save_results(summary):
    """Salva os resultados em arquivo"""
    import json

    import os
    os.makedirs('results', exist_ok=True)

    def convert_numpy(obj):
        if isinstance(obj, np.float64):
            return float(obj)
        elif isinstance(obj, np.int64):
            return int(obj)
        elif isinstance(obj, dict):
            return {key: convert_numpy(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [convert_numpy(item) for item in obj]
        return obj
    
    summary_clean = convert_numpy(summary)
    
    with open('results/analysis_results.json', 'w', encoding='utf-8') as f:
        json.dump(summary_clean, f, indent=2, ensure_ascii=False)
    
    print("Resultados salvos em results/analysis_results.json")

def print_results_summary(summary):
    """Imprime resumo dos resultados"""
    print("\n" + "="*50)
    print("RESUMO DOS RESULTADOS")
    print("="*50)
    
    print(f"\nINFORMAÇÕES DO DATASET:")
    print(f"Total de PRs analisados: {summary['dataset_info']['total_prs']}")
    print(f"PRs merged: {summary['dataset_info']['merged_prs']}")
    print(f"PRs closed: {summary['dataset_info']['closed_prs']}")
    print(f"Taxa de merge: {summary['dataset_info']['merge_rate']:.1f}%")
    
    print(f"\nMEDIANAS DAS VARIÁVEIS:")
    for var, value in summary['medians'].items():
        print(f"{var}: {value:.2f}")
    
    print(f"\nCORRELAÇÕES MAIS SIGNIFICATIVAS (|r| > 0.1 e p < 0.05):")
    
    significant_corrs = []
    for key, values in summary['correlations'].items():
        if abs(values['spearman']) > 0.1 and values['spearman_p'] < 0.05:
            significant_corrs.append((key, values['spearman'], values['spearman_p']))
    
    significant_corrs.sort(key=lambda x: abs(x[1]), reverse=True)
    
    for corr_name, corr_value, p_value in significant_corrs[:10]:
        print(f"{corr_name}: r={corr_value:.3f} (p={p_value:.3f})")

def main():
    """Função principal"""
    print("Iniciando análise completa dos dados...")
    
    df = load_and_prepare_data()

    results = calculate_correlations(df)

    create_visualizations(df)

    summary = generate_statistics_summary(df, results)

    save_results(summary)

    print_results_summary(summary)
    
    print("\n" + "="*50)
    print("ANÁLISE CONCLUÍDA!")
    print("Verifique os arquivos gerados em results/")
    print("="*50)

if __name__ == "__main__":
    main()
