"""
Evaluate rankings generated for CSFCube.
"""
import sys
import os
import argparse
import statistics
import codecs
import json
import csv

import rank_metrics as rm

# paper-ids for the different folds for cross-validatio; Ugly but easier to have it here.
facet2folds = {
    "background": {"fold1_dev": ["3264891_background", "1936997_background", "11844559_background",
                                 "52194540_background", "1791179_background", "6431039_background",
                                 "6173686_background", "7898033_background"],
                   "fold2_dev": ["5764728_background", "10014168_background", "10695055_background",
                                 "929877_background", "1587_background", "51977123_background",
                                 "8781666_background", "189897839_background"],
                   "fold1_test": ["5764728_background", "10014168_background", "10695055_background",
                                  "929877_background", "1587_background", "51977123_background",
                                  "8781666_background", "189897839_background"],
                   "fold2_test": ["3264891_background", "1936997_background", "11844559_background",
                                  "52194540_background", "1791179_background", "6431039_background",
                                  "6173686_background", "7898033_background"]},
    "method": {"fold1_dev": ["189897839_method", "1791179_method", "11310392_method", "2468783_method",
                             "13949438_method", "5270848_method", "52194540_method", "929877_method"],
               "fold2_dev": ["5052952_method", "10010426_method", "102353905_method", "174799296_method",
                             "1198964_method", "53080736_method", "1936997_method", "80628431_method",
                             "53082542_method"],
               "fold1_test": ["5052952_method", "10010426_method", "102353905_method", "174799296_method",
                              "1198964_method", "53080736_method", "1936997_method", "80628431_method",
                              "53082542_method"],
               "fold2_test": ["189897839_method", "1791179_method", "11310392_method", "2468783_method",
                              "13949438_method", "5270848_method", "52194540_method", "929877_method"]},
    "result": {"fold1_dev": ["2090262_result", "174799296_result", "11844559_result", "2468783_result",
                             "1306065_result", "5052952_result", "3264891_result", "8781666_result"],
               "fold2_dev": ["2865563_result", "10052042_result", "11629674_result", "1587_result",
                             "1198964_result", "53080736_result", "2360770_result", "80628431_result",
                             "6431039_result"],
               "fold1_test": ["2865563_result", "10052042_result", "11629674_result", "1587_result",
                              "1198964_result", "53080736_result", "2360770_result", "80628431_result",
                              "6431039_result"],
               "fold2_test": ["2090262_result", "174799296_result", "11844559_result", "2468783_result",
                              "1306065_result", "5052952_result", "3264891_result", "8781666_result"]},
    "all": {"fold1_dev": ["3264891_background", "1936997_background", "11844559_background",
                          "52194540_background", "1791179_background", "6431039_background",
                          "6173686_background", "7898033_background", "189897839_method",
                          "1791179_method", "11310392_method", "2468783_method", "13949438_method",
                          "5270848_method", "52194540_method", "929877_method", "2090262_result",
                          "174799296_result", "11844559_result", "2468783_result", "1306065_result",
                          "5052952_result", "3264891_result", "8781666_result"],
            "fold2_dev": ["5764728_background", "10014168_background", "10695055_background",
                          "929877_background", "1587_background", "51977123_background",
                          "8781666_background", "189897839_background", "5052952_method", "10010426_method",
                          "102353905_method", "174799296_method", "1198964_method", "53080736_method",
                          "1936997_method", "80628431_method", "53082542_method", "2865563_result",
                          "10052042_result", "11629674_result", "1587_result", "1198964_result",
                          "53080736_result", "2360770_result", "80628431_result", "6431039_result"],
            "fold1_test": ["5764728_background", "10014168_background", "10695055_background",
                           "929877_background", "1587_background", "51977123_background", "8781666_background",
                           "189897839_background", "5052952_method", "10010426_method", "102353905_method",
                           "174799296_method", "1198964_method", "53080736_method", "1936997_method",
                           "80628431_method", "53082542_method", "2865563_result", "10052042_result",
                           "11629674_result", "1587_result", "1198964_result", "53080736_result",
                           "2360770_result", "80628431_result", "6431039_result"],
            "fold2_test": ["3264891_background", "1936997_background", "11844559_background",
                           "52194540_background", "1791179_background", "6431039_background",
                           "6173686_background", "7898033_background", "189897839_method", "1791179_method",
                           "11310392_method", "2468783_method", "13949438_method", "5270848_method",
                           "52194540_method", "929877_method", "2090262_result", "174799296_result",
                           "11844559_result", "2468783_result", "1306065_result", "5052952_result",
                           "3264891_result", "8781666_result"]
            }
}


def recall_at_k(ranked_rel, atk, max_total_relevant):
    """
    Compute recall at k.
    :param ranked_rel: list(int); ranked list of relevance judged data.
    :param atk: int; rank at which to compute metric.
    :param max_total_relevant: int; maximum relevant to consider in
        case there are more relevant in total.
    :return: recall: float.
    """
    total_relevant = sum(ranked_rel)
    total_relevant = min(max_total_relevant, total_relevant)
    relatk = sum(ranked_rel[:atk])
    if total_relevant > 0:
        recall_atk = float(relatk)/total_relevant
    else:
        recall_atk = 0.0
    return recall_atk


def read_facet_specific_relevances(data_path, run_path, dataset, facet, method_name):
    """
    Read the gold data and the model rankings and the relevances for the
    model.
    :param data_path: string; directory with gold citations for test pids and rankings
        from baseline methods in subdirectories.
    :param run_path: string; directory with ranked candidates for baselines a subdir of
        data_path else is a model run.
    :param method_name: string; method with which ranks were created.
    :param dataset: string; eval dataset.
    :param facet: string; facet for eval.
    :return: qpid2rankedcand_relevances: dict('qpid_facet': [relevances]);
        candidate gold relevances for the candidates in order ranked by the
        model.
    """
    gold_fname = os.path.join(data_path, 'test-pid2anns-{:s}-{:s}.json'.format(dataset, facet))
    ranked_fname = os.path.join(run_path, 'test-pid2pool-{:s}-{:s}-{:s}-ranked.json'.
                                format(dataset, method_name, facet))
    # Load gold test data (citations).
    with codecs.open(gold_fname, 'r', 'utf-8') as fp:
        pid2pool_source = json.load(fp)
        num_query = len(pid2pool_source)
        print('Gold query pids: {:d}'.format(num_query))
        pid2rels_gold = {}
        for qpid, pool_rel in pid2pool_source.items():
            pool = pool_rel['cands']
            cands_rels = pool_rel['relevance_adju']
            pid2rels_gold['{:s}_{:s}'.format(qpid, facet)] = \
                dict([(pid, rel) for pid, rel in zip(pool, cands_rels)])
    # Load ranked predictions on test data with methods.
    with codecs.open(ranked_fname, 'r', 'utf-8') as fp:
        pid2ranks = json.load(fp)
        print('Valid ranked query pids: {:d}'.format(len(pid2ranks)))
        qpid2rankedcand_relevances = {}
        for qpid, citranks in pid2ranks.items():
            candpids = [pid_score[0] for pid_score in citranks]
            cand_relevances = [pid2rels_gold['{:s}_{:s}'.format(qpid, facet)][pid] for pid in candpids]
            qpid2rankedcand_relevances['{:s}_{:s}'.format(qpid, facet)] = cand_relevances
    return qpid2rankedcand_relevances


def read_all_facet_relevances(data_path, run_path, dataset, method_name, facets):
    """
    Read the gold data and the model rankings and the relevances for the
    model.
    :param data_path: string; directory with gold citations for test pids and rankings
        from baseline methods in subdirectories.
    :param run_path: string; directory with ranked candidates for baselines a subdir of
        data_path else is a model run.
    :param method_name: string; method with which ranks were created.
    :param dataset: string; eval dataset.
    :param facets: list(string); what facets to read/what counts as "all".
    :return: qpid2rankedcand_relevances: dict('qpid_facet': [relevances]);
        candidate gold relevances for the candidates in order ranked by the
        model.
    """
    qpid2rankedcand_relevances = {}
    for facet in facets:
        print('Reading facet: {:s}'.format(facet))
        gold_fname = os.path.join(data_path, 'test-pid2anns-{:s}-{:s}.json'.format(dataset, facet))
        ranked_fname = os.path.join(run_path, 'test-pid2pool-{:s}-{:s}-{:s}-ranked.json'.
                                    format(dataset, method_name, facet))
        # Load gold test data (citations).
        with codecs.open(gold_fname, 'r', 'utf-8') as fp:
            pid2pool_source = json.load(fp)
            num_query = len(pid2pool_source)
            print('Gold query pids: {:d}'.format(num_query))
            pid2rels_gold = {}
            for qpid, pool_rel in pid2pool_source.items():
                pool = pool_rel['cands']
                cands_rels = pool_rel['relevance_adju']
                pid2rels_gold['{:s}_{:s}'.format(qpid, facet)] = \
                    dict([(pid, rel) for pid, rel in zip(pool, cands_rels)])
        # Load ranked predictions on test data with methods.
        with codecs.open(ranked_fname, 'r', 'utf-8') as fp:
            pid2ranks = json.load(fp)
            print('Valid ranked query pids: {:d}'.format(len(pid2ranks)))
            for qpid, citranks in pid2ranks.items():
                candpids = [pid_score[0] for pid_score in citranks]
                cand_relevances = [pid2rels_gold['{:s}_{:s}'.format(qpid, facet)][pid] for pid in candpids]
                qpid2rankedcand_relevances['{:s}_{:s}'.format(qpid, facet)] = cand_relevances
    print('Total queries: {:d}'.format(len(qpid2rankedcand_relevances)))
    return qpid2rankedcand_relevances


def compute_metrics(ranked_judgements, pr_atk, threshold_grade):
    """
    Given the ranked judgements compute the metrics for a query.
    :param ranked_judgements: list(int); graded or binary relevances in rank order.
    :param pr_atk: int; the @K value to use for computing precision and recall.
    :param threshold_grade: int; Assuming 0-3 graded relevances, threshold at some point
        and convert graded to binary relevance.
    :return:
    """
    graded_judgements = ranked_judgements
    ranked_judgements = [1 if rel >= threshold_grade else 0 for rel in graded_judgements]
    # Use the full set of candidate not the pr_atk.
    ndcg = rm.ndcg_at_k(graded_judgements, len(ranked_judgements))
    ndcg_pr = rm.ndcg_at_k(graded_judgements, int(0.20*len(ranked_judgements)))
    ndcg_20 = rm.ndcg_at_k(graded_judgements, 20)
    max_total_relevant = sum(ranked_judgements)
    recall = recall_at_k(ranked_rel=ranked_judgements,
                         atk=pr_atk, max_total_relevant=max_total_relevant)
    precision = rm.precision_at_k(r=ranked_judgements, k=pr_atk)
    r_precision = rm.r_precision(r=ranked_judgements)
    f1 = 2*precision*recall/(precision + recall) if (precision + recall) > 0 else 0.0
    av_precision = rm.average_precision(r=ranked_judgements)
    reciprocal_rank = rm.mean_reciprocal_rank(rs=[ranked_judgements])
    metrics = {
        'recall': float(recall),
        'precision': float(precision),
        'f1': float(f1),
        'r_precision': float(r_precision),
        'av_precision': float(av_precision),
        'reciprocal_rank': float(reciprocal_rank),
        'ndcg': ndcg,
        'ndcg@20': ndcg_20,
        'ndcg%20': ndcg_pr
    }
    return metrics


def aggregate_metrics_crossval(query_metrics, split_str, facet_str):
    """
    Given metrics over individual queries aggregate over different
    queries.
    :param query_metrics: dict(query_id: metrics_dict from compute_metrics)
    :param split_str: string; {dev, test}
    :param facet_str: string; {background, method, result}
    :return:
    """
    aggmetrics = {
        'precision': [],
        'recall': [],
        'f1': [],
        'r_precision': [],
        'mean_av_precision': [],
        'mean_reciprocal_rank': [],
        'ndcg': [],
        'ndcg@20': [],
        'ndcg%20': []
    }
    # For dev only use a part of the fold - using both makes it identical to test.
    if split_str == 'dev':
        folds = ['fold1_{:s}'.format(split_str)]
    elif split_str == 'test':
        folds = ['fold1_{:s}'.format(split_str), 'fold2_{:s}'.format(split_str)]
    for fold_str in folds:
        fold_pids = facet2folds[facet_str][fold_str]
        precision, recall, f1, av_precision, mrr, ndcg, r_precision = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
        ndcg_20, ndcg_pr = 0.0, 0.0
        for query_id in fold_pids:
            # Aggregate across paper types in the fold.
            metrics = query_metrics[query_id]
            # Aggregate across all papers in the fold
            precision += metrics['precision']
            recall += metrics['recall']
            f1 += metrics['f1']
            av_precision += metrics['av_precision']
            mrr += metrics['reciprocal_rank']
            r_precision += metrics['r_precision']
            ndcg += metrics['ndcg']
            ndcg_20 += metrics['ndcg@20']
            ndcg_pr += metrics['ndcg%20']
        # Average all folds
        num_queries = len(fold_pids)
        precision, recall, f1 = precision/num_queries, recall/num_queries, f1/num_queries
        av_precision = av_precision/num_queries
        mrr, ndcg, r_precision = mrr/num_queries, ndcg/num_queries, r_precision/num_queries
        ndcg_20, ndcg_pr = ndcg_20/num_queries, ndcg_pr/num_queries
        # Save the averaged metric for every fold.
        aggmetrics['precision'].append(precision)
        aggmetrics['recall'].append(recall)
        aggmetrics['f1'].append(f1)
        aggmetrics['r_precision'].append(r_precision)
        aggmetrics['mean_av_precision'].append(av_precision)
        aggmetrics['mean_reciprocal_rank'].append(mrr)
        aggmetrics['ndcg'].append(ndcg)
        aggmetrics['ndcg@20'].append(ndcg_20)
        aggmetrics['ndcg%20'].append(ndcg_pr)

    aggmetrics = {
        'precision': statistics.mean(aggmetrics['precision']),
        'recall': statistics.mean(aggmetrics['recall']),
        'f1': statistics.mean(aggmetrics['f1']),
        'r_precision': statistics.mean(aggmetrics['r_precision']),
        'mean_av_precision': statistics.mean(aggmetrics['mean_av_precision']),
        'mean_reciprocal_rank': statistics.mean(aggmetrics['mean_reciprocal_rank']),
        'ndcg': statistics.mean(aggmetrics['ndcg']),
        'ndcg@20': statistics.mean(aggmetrics['ndcg@20']),
        'ndcg%20': statistics.mean(aggmetrics['ndcg%20'])
    }
    return aggmetrics


def graded_eval_pool_rerank(data_path, run_path, method_name, dataset, facet, split):
    """
    Evaluate the re-ranked pool for the faceted data. Anns use graded relevance scores.
    :param data_path: string; directory with gold citations for test pids and rankings
        from baseline methods in subdirectories.
    :param run_path: string; directory with ranked candidates for baselines a subdir of
        data_path else is a model run.
    :param method_name: string; method with which ranks were created.
    :param dataset: string; eval dataset.
    :param facet: string; facet for eval.
    :param split: strong; {dev, test}
    :return:
    """
    print(f'EVAL SPLIT: {split}')
    ATK = 20
    with codecs.open(os.path.join(data_path, 'queries-release.csv')) as csvfile:
        reader = csv.DictReader(csvfile)
        query_metadata = dict([('{:s}_{:s}'.format(row['pid'], row['facet']), row) for row in reader])

    perq_out_fname = os.path.join(run_path, 'test-pid2pool-{:s}-{:s}-{:s}-perq.csv'.
                                  format(dataset, method_name, facet))
    if facet == 'all':
        qpid2rankedcand_relevances = read_all_facet_relevances(data_path=data_path, run_path=run_path,
                                                               dataset=dataset, method_name=method_name,
                                                               facets=['background', 'method', 'result'])
    else:
        qpid2rankedcand_relevances = read_facet_specific_relevances(data_path=data_path, run_path=run_path,
                                                                    dataset=dataset, facet=facet,
                                                                    method_name=method_name)
    # Go over test papers and compute metrics.
    all_metrics = {}
    num_cands = 0.0
    num_queries = 0.0
    perq_file = codecs.open(perq_out_fname, 'w', 'utf-8')
    perq_csv = csv.DictWriter(perq_file, extrasaction='ignore',
                              fieldnames=['paper_id', 'title', 'recall', 'precision', 'f1', 'r_precision',
                                          'av_precision', 'reciprocal_rank', 'ndcg', 'ndcg%20', 'paper type'])
    perq_csv.writeheader()
    print('Precision and recall at rank: {:d}'.format(ATK))
    for qpid_facet, qranked_judgements in qpid2rankedcand_relevances.items():
        all_metrics[qpid_facet] = compute_metrics(qranked_judgements, pr_atk=ATK,
                                                  threshold_grade=2)
        num_cands += len(qranked_judgements)
        num_queries += 1
        metrics = all_metrics[qpid_facet]
        metrics['paper_id'] = qpid_facet
        metrics['title'] = query_metadata[qpid_facet]['title']
        metrics['paper type'] = query_metadata[qpid_facet]['paper type']
        metrics['year'] = query_metadata[qpid_facet]['year']
        perq_csv.writerow(metrics)
    aggmetrics = aggregate_metrics_crossval(query_metrics=all_metrics,
                                            facet_str=facet, split_str=split)
    print('Wrote: {:s}'.format(perq_file.name))
    perq_file.close()
    print('Total queries: {:d}; Total candidates: {:d}'.format(int(num_queries), int(num_cands)))
    print('R-Precision; Precision@{:d}; Recall@{:d}; NDCG; NDCG@20; NDCG%20'.format(ATK, ATK))
    print('{:.4f}, {:.4f}, {:.4f}, {:.4f}, {:.4f}, {:.4f}\n'.
          format(aggmetrics['r_precision'], aggmetrics['precision'], aggmetrics['recall'],
                 aggmetrics['ndcg'], aggmetrics['ndcg@20'], aggmetrics['ndcg%20']))
    

def main():
    """
    Parse command line arguments and call all the above routines.
    :return:
    """
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subcommand',
                                       help='The action to perform.')
    # Evaluate the re-ranked pools.
    evaluate_pool_ranks = subparsers.add_parser('eval_pool_ranking')
    evaluate_pool_ranks.add_argument('--gold_path', required=True,
                                     help='Path with gold data; Where the annotated files '
                                          'test-pid2anns-csfcube-{background/method/result}.json are.')
    evaluate_pool_ranks.add_argument('--ranked_path',
                                     help='Path with ranked candidates; Files named '
                                          'test-pid2pool-csfcube-{YOUR-MODEL-NAME}-{FACET}-ranked.json')
    evaluate_pool_ranks.add_argument('--experiment',
                                     help='Method name used to generate rankings.')
    evaluate_pool_ranks.add_argument('--facet',
                                     choices=['background', 'method', 'result', 'all'],
                                     help='Facet of abstract to read from. \'all\' aggregates over'
                                          'the other three facets, it does not represent a valid facet.')
    cl_args = parser.parse_args()

    if cl_args.subcommand == 'eval_pool_ranking':
        graded_eval_pool_rerank(data_path=cl_args.gold_path, method_name=cl_args.experiment,
                                facet=cl_args.facet, dataset='csfcube', run_path=cl_args.ranked_path,
                                split='dev')
        graded_eval_pool_rerank(data_path=cl_args.gold_path, method_name=cl_args.experiment,
                                facet=cl_args.facet, dataset='csfcube', run_path=cl_args.ranked_path,
                                split='test')
    else:
        sys.stderr.write("Unknown action.")


if __name__ == '__main__':
    main()
