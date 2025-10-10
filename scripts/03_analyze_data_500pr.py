import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import spearmanr, pearsonr
from datetime import datetime
import os
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['font.size'] = 10
plt.rcParams['figure.figsize'] = (12, 8)

def load_and_prepare_data():
    print("Carregando dados (500 PRs)...")
    enriched_path = os.path.join("data", "pull_requests_500.participants.csv")
    base_path = os.path.join("data", "pull_requests_500.csv")
    df_path = enriched_path if os.path.exists(enriched_path) else base_path
    df = pd.read_csv(df_path)
    
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['closed_at'] = pd.to_datetime(df['closed_at'])
    df['merged_at'] = pd.to_datetime(df['merged_at'])
    
    df['analysis_time_hours'] = (df['closed_at'] - df['created_at']).dt.total_seconds() / 3600
    df['total_lines_changed'] = df['additions'] + df['deletions']
    df['total_interactions'] = df['comments'] + df['review_comments']
    df['is_merged'] = (df['state'] == 'closed') & (df['merged_at'].notna())
    
    df = df[df['analysis_time_hours'] >= 1]
    df = df[df['comments'] > 0]
    
    print(f"Dataset preparado: {len(df)} PRs válidos")
    return df

def calculate_correlations(df):
    results = {}
    
    size_vars = ['changed_files', 'total_lines_changed']
    time_var = 'analysis_time_hours'
    description_var = 'body_length'
    interaction_vars = ['participants_count', 'comments']
    
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
    
    for var in ['comments']:
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
    
    plt.suptitle('RQ01: Tamanho do PR vs Status (Merged/Closed)', fontsize=16)
    plt.tight_layout()
    plt.savefig('results_500pr/rq01_tamanho_vs_status.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    fig, ax1 = plt.subplots(1, 1, figsize=(10, 6))
    
    ax1.boxplot([merged_data['analysis_time_hours'], closed_data['analysis_time_hours']], 
                labels=['Merged', 'Closed'])
    ax1.set_title('Tempo de Análise por Status')
    ax1.set_ylabel('Tempo (horas)')
    ax1.set_yscale('log')
    
    plt.suptitle('RQ02: Tempo de Análise vs Status do PR', fontsize=16)
    plt.tight_layout()
    plt.savefig('results_500pr/rq02_tempo_vs_status.png', dpi=300, bbox_inches='tight')
    plt.close()

    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    ax.boxplot([merged_data['body_length'], closed_data['body_length']], 
               labels=['Merged', 'Closed'])
    ax.set_title('Tamanho da Descrição por Status')
    ax.set_ylabel('Caracteres na Descrição')
    plt.suptitle('RQ03: Descrição dos PRs vs Status Final', fontsize=16)
    plt.tight_layout()
    plt.savefig('results_500pr/rq03_descricao_vs_status.png', dpi=300, bbox_inches='tight')
    plt.close()

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    axes[0].boxplot([merged_data['comments'], closed_data['comments']], labels=['Merged', 'Closed'])
    axes[0].set_title('Comentários por Status')
    axes[0].set_ylabel('Número de Comentários')
    axes[1].boxplot([merged_data['review_comments'], closed_data['review_comments']], labels=['Merged', 'Closed'])
    axes[1].set_title('Review Comments por Status')
    axes[1].set_ylabel('Número de Reviews')
    axes[2].boxplot([merged_data['total_interactions'], closed_data['total_interactions']], labels=['Merged', 'Closed'])
    axes[2].set_title('Total de Interações por Status')
    axes[2].set_ylabel('Interações Totais')
    plt.suptitle('RQ04: Interações nos PRs vs Status Final', fontsize=16)
    plt.tight_layout()
    plt.savefig('results_500pr/rq04_interacoes_vs_status.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    for i, var in enumerate(['changed_files', 'additions', 'deletions', 'total_lines_changed']):
        row = i // 2
        col = i % 2
        
        axes[row, col].scatter(df[var], df['review_comments'], alpha=0.6, color='#1f77b4')
        axes[row, col].set_xlabel(var.replace('_', ' ').title())
        axes[row, col].set_ylabel('Comentários de Revisão')
        
        if var in ['additions', 'deletions', 'total_lines_changed']:
            axes[row, col].set_xscale('log')
        
        corr = df[var].corr(df['review_comments'])
        axes[row, col].set_title(f'{var.replace("_", " ").title()}\n(Corr: {corr:.3f})')
    
    plt.suptitle('RQ05: Tamanho do PR vs Número de Revisões', fontsize=16)
    plt.tight_layout()
    plt.savefig('results_500pr/rq05_tamanho_vs_revisoes.png', dpi=300, bbox_inches='tight')
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
    plt.savefig('results_500pr/rq06_tempo_vs_revisoes.png', dpi=300, bbox_inches='tight')
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
    
    plt.suptitle('RQ07: Tamanho da Descrição vs Número de Revisões', fontsize=16)
    plt.tight_layout()
    plt.savefig('results_500pr/rq07_descricao_vs_revisoes.png', dpi=300, bbox_inches='tight')
    plt.close()

    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    ax.scatter(df['comments'], df['review_comments'], alpha=0.6, color='#1f77b4')
    ax.set_xlabel('Número de Comentários')
    ax.set_ylabel('Número de Reviews')
    ax.set_title('Comentários vs Reviews')
    
    plt.suptitle('RQ08: Interações vs Número de Revisões', fontsize=16)
    plt.tight_layout()
    plt.savefig('results_500pr/rq08_interacoes_vs_revisoes.png', dpi=300, bbox_inches='tight')
    plt.close()

    correlation_vars = ['total_lines_changed', 'analysis_time_hours', 'body_length',
                        'total_interactions', 'review_comments', 'is_merged']
    
    numeric_df = df[correlation_vars].select_dtypes(include=[np.number])
    corr_matrix = numeric_df.corr().fillna(0.0)

    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, square=True, fmt='.3f')
    plt.title('Matriz de Correlação entre Variáveis')
    plt.tight_layout()
    plt.savefig('results_500pr/matriz_correlacao.png', dpi=300, bbox_inches='tight')
    plt.close()

def generate_summary(df, correlations):
    import os
    import json
    
    if not os.path.exists('results_500pr'):
        os.makedirs('results_500pr')
    
    def convert_to_json_serializable(obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return obj
    
    summary = {
        'dataset_info': {
            'total_prs': len(df),
            'merged_prs': len(df[df['is_merged'] == True]),
            'closed_prs': len(df[df['is_merged'] == False]),
            'merge_rate': len(df[df['is_merged'] == True]) / len(df)
        },
        'medians': {
            'changed_files': convert_to_json_serializable(df['changed_files'].median()),
            'total_lines_changed': convert_to_json_serializable(df['total_lines_changed'].median()),
            'analysis_time_hours': convert_to_json_serializable(df['analysis_time_hours'].median()),
            'body_length': convert_to_json_serializable(df['body_length'].median()),
            'participants_count': convert_to_json_serializable(df['participants_count'].median() if 'participants_count' in df.columns else np.nan),
            'comments': convert_to_json_serializable(df['comments'].median())
        },
        'correlations': {}
    }
    
    for key, value in correlations.items():
        summary['correlations'][key] = {
            'spearman': convert_to_json_serializable(value['spearman']),
            'spearman_p': convert_to_json_serializable(value['spearman_p']),
            'pearson': convert_to_json_serializable(value['pearson']),
            'pearson_p': convert_to_json_serializable(value['pearson_p'])
        }
        
        if 'merged_median' in value:
            summary['correlations'][key]['merged_median'] = convert_to_json_serializable(value['merged_median'])
            summary['correlations'][key]['closed_median'] = convert_to_json_serializable(value['closed_median'])
    
    with open('results_500pr/analysis_results.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

def print_results(df, correlations):
    print("\n" + "="*50)
    print("RESUMO DOS RESULTADOS (500 PRs)")
    print("="*50)
    
    print(f"\nINFORMAÇÕES DO DATASET:")
    print(f"Total de PRs analisados: {len(df)}")
    print(f"PRs merged: {len(df[df['is_merged'] == True])}")
    print(f"PRs closed: {len(df[df['is_merged'] == False])}")
    print(f"Taxa de merge: {len(df[df['is_merged'] == True]) / len(df) * 100:.1f}%")
    
    print(f"\nMEDIANAS DAS VARIÁVEIS:")
    for var in ['changed_files', 'total_lines_changed', 'analysis_time_hours', 'body_length', 'participants_count', 'comments']:
        print(f"{var}: {df[var].median():.2f}")
    
    print(f"\nCORRELAÇÕES MAIS SIGNIFICATIVAS (|r| > 0.1 e p < 0.05):")
    significant_corrs = []
    for key, value in correlations.items():
        spearman_r = abs(value['spearman'])
        spearman_p = value['spearman_p']
        if spearman_r > 0.1 and spearman_p < 0.05:
            significant_corrs.append((key, value['spearman'], spearman_p))
    
    significant_corrs.sort(key=lambda x: abs(x[1]), reverse=True)
    for key, r, p in significant_corrs:
        print(f"{key}: r={r:.3f} (p={p:.3f})")
    
    print("\n" + "="*50)
    print("ANÁLISE CONCLUÍDA! (500 PRs)")
    print("Verifique os arquivos gerados em results_500pr/")
    print("="*50)

def main():
    print("Iniciando análise dos dados (500 PRs)...")
    
    df = load_and_prepare_data()
    correlations = calculate_correlations(df)
    create_visualizations(df)
    
    print("\nGerando resumo estatístico...")
    generate_summary(df, correlations)
    
    print_results(df, correlations)

if __name__ == "__main__":
    main()
