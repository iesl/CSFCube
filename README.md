### Description of dataset:

**Title**: "CSFCube - A Test Collection of Computer Science Papers for Faceted Query by Example"

**Authors**: Sheshera Mysore, Tim O'Gorman, Andrew McCallum, Hamed Zamani

**Abstract**: Query by Example is a well-known information retrieval task in which a document is chosen by the user as the search query and the goal is to retrieve relevant documents from a large collection. However, a document often covers multiple aspects of a topic. To address this scenario we introduce the task of faceted Query by Example in which users can also specify a finer grained aspect in addition to the input query document. We focus on the application of this task in scientific literature search. We envision models which are able to retrieve scientific papers analogous to a query scientific paper along specifically chosen rhetorical structure elements as one solution to this problem. In this work, the rhetorical structure elements, which we refer to as facets,  indicate objectives, methods, or results of a scientific paper. We introduce and describe an expert annotated test collection to evaluate models trained to perform this task. Our test collection consists of a diverse set of 50 query documents in English, drawn from computational linguistics and machine learning venues. We carefully follow the annotation guideline used by TREC for depth-k pooling (k = 100 or 250) and the resulting data collection consists of graded relevance scores with high annotation agreement. State of the art models evaluated on our dataset show a significant gap to be closed in further work. Our dataset may be accessed here: https://github.com/iesl/CSFCube

The paper describing the dataset can be accessed here: https://openreview.net/forum?id=8Y50dBbmGU

### Dataset Release

Please use the appropriate [release](https://github.com/iesl/CSFCube/releases) to download salient releases of the dataset.


### Contents:

		├── abstracts-csfcube-preds.jsonl
		├── ann_guidelines.pdf
		├── queries-release.csv
		├── README.md
		├── LICENSE.md
		├── datasheet.md
		├── evaluation_splits.json
		├── eval_scripts
		│             ├── rank_metrics.py
		│             ├── ranking_eval.py
		│             ├── requirements.txt
		│             └── sample_ranked_pools
		│                 ├── test-pid2pool-csfcube-specter-background-ranked.json
		│                 ├── test-pid2pool-csfcube-specter-method-ranked.json
		│	              └── test-pid2pool-csfcube-specter-result-ranked.json
		├── readable_annotations
		│             ├── 10010426-method-adju.txt
		│             ├── 10014168-background-adju.txt
		│	.
		│	.
		│	.	
		│
		├── test-pid2anns-csfcube-background.json
		├── test-pid2anns-csfcube-method.json
		├── test-pid2anns-csfcube-result.json
		└── test-pid2pool-csfcube.json

`abstracts-csfcube-preds.jsonl`: `jsonl` file containing the paper-id, abstracts, titles, and metadata for the queries and candidates which are part of the test collection.

`ann_guidelines.pdf`: The annotator guidelines with relevance guidelines per facet and details about the process followed in selecting the data items to be annotated.

`queries-release.csv`: Queries which are part of the test collection and metadata (year, paper-type) associated with every query.

`readable_annotations`: Directory of 50 text files for browsing the annotations -- with one file per query-facet pair. Candidates for every query are sorted by adjudicated relevance.

`test-pid2anns-csfcube-{background/method/result}.json`: JSON file with the query paper-id, candidate paper-ids for every query paper in the test collection. Use these files in conjunction with `abstracts-csfcube-preds.jsonl` to generate files for use in model evaluation. 

`test-pid2pool-csfcube.json`: JSON file query paper-id, candidate paper-ids and the methods which caused the candidate to be included in the pool. The methods are one among `{abs_tfidf, abs_cbow200, abs_tfidfcbow200, title_tfidf, title_cbow200, title_tfidfcbow200, specter, cited}`. This file is included to facilitate further analysis of the dataset.

`evaluation_splits.json`: Paper-ids for the splits to use in reporting evaluation numbers. `eval_scripts` implements the evaluation protocol and computes evaluation metrics. Please see the paper and `datasheet.md` for descriptions of the experimental protocol we recommend to report numbers. 

`eval_scripts`: Python scripts to compute evaluation metrics, example output files of a ranked pool which the scripts consume to generate the metrics, and a `requirements.txt` file.

`datasheet.md`: Following recommended practice to report the details of the a dataset, we provide a Datasheet following prompts provided in [Bender et. al. 2018](https://www.aclweb.org/anthology/Q18-1041/) and [Gebru et. al. 2018](https://arxiv.org/abs/1803.09010).

`LICENSE.md`: The dataset is released under the [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) license. 

`abstracts-preds.zip`: The roughly 800k abstracts from which the candidate pools for the dataset were built. Hosted externally here: https://figshare.com/articles/dataset/abstracts-preds_zip/14796339 

### Usage instructions:

1. To generate rankings per query the following files will be necessary: `test-pid2anns-csfcube-{background/method/result}.json` and `abstracts-csfcube-preds.jsonl`. The `test-pid2anns-*` files contain the rated pool of documents per query which your methods will need to re-rank and `abstracts-csfcube-preds` contains the actual title and abstract text for the documents. In generating ranked outputs the evaluation scripts consume json files of a specific format. Below is some example code for reading in data, generating rankings, and writing out an apt json file for evaluation of the `background` facet with an toy model called `my_model`:

	```
	# Read in paper text data.
	with codecs.open('abstracts-csfcube-preds.jsonl', 'r', 'utf-8') as absfile:
        for line in absfile:
            injson = json.loads(line.strip())
            pid2abstract[injson['paper_id']] = injson

	# Read in pools for the queries per facet.
	with codecs.open(test-pid2anns-csfcube-background.json, 'r', 'utf-8') as fp:
        qpid2pool = json.load(fp)
	
	# Rank the candidates per query.
	qpid2pool_ranked = {}
	for qpid in qpid2pool.keys():
		# Get the paper-ids for candidates.
        cand_pids = qpid2pool[qpid]['cands']
        # Compute the distance between a query and candidate.
        query_cand_distance = []
        for cpid in cand_pids:
        	dist = my_model(pid2abstract[qpid], pid2abstract[cpid])
			query_cand_distance.append((cpid, dist))
		# Sort the candidates in predicted rank order - smallest to largest distances.
		ranked_pool = list(sorted(query_cand_distance, key=lambda cd: cd[1]))
		qpid2pool_ranked[qpid] = ranked_pool

	# Write out the ranked pool in a format consumed by the eval script.
	with codecs.open('test-pid2pool-csfcube-my_model-background-ranked.json', 'w', 'utf-8') as fp:
        json.dump(query2rankedcands, fp)
	```

2. Once an appropriate json file with the ranked files is generated use the `eval_scripts/ranking_eval.py` (its only dependency is numpy) to generate evaluation metrics. The eval script consumes a json file with a ranked pool of candidates structured as: `{query-paper-id: [[candidate-pid-1, distance], [candidate-pid-2, distance] ...], ...}`. These are expected to be named as `test-pid2pool-csfcube-{YOUR-MODEL-NAME}-{background/method/result}-ranked.json`. Aptly structured example files for the [SPECTER](https://aclanthology.org/2020.acl-main.207/) baseline are included in `eval_scripts/sample_ranked_pools`. Below is an example run of the script for the included example files. The script will print results to stdout and write a csv file with per-query performance metrics to the directory passed with `ranked_path`:

	```
	python3 eval_scripts/ranking_eval.py eval_pool_ranking --gold_path ./ --ranked_path eval_scripts/sample_ranked_pools --experiment specter --facet background

	python3 eval_scripts/ranking_eval.py eval_pool_ranking --gold_path ./ --ranked_path eval_scripts/sample_ranked_pools --experiment specter --facet method

	python3 eval_scripts/ranking_eval.py eval_pool_ranking --gold_path ./ --ranked_path eval_scripts/sample_ranked_pools --experiment specter --facet result

	python3 eval_scripts/ranking_eval.py eval_pool_ranking --gold_path ./ --ranked_path eval_scripts/sample_ranked_pools --experiment specter --facet all
	```


### Acknowledgments: 

This dataset was built using the [Semantic Scholar Open Research Corpus](https://github.com/allenai/s2orc)(S2ORC). This dataset also uses the pre-trained models of [sequential_sentence_classification](https://github.com/allenai/sequential_sentence_classification) and [SPECTER](https://github.com/allenai/specter).


### Citation:

Cite the paper as:
```
@inproceedings{mysore2021csfcube,
	title={{CSFC}ube - A Test Collection of Computer Science Research Articles for Faceted Query by Example},
	author={Sheshera Mysore and Tim O'Gorman and Andrew McCallum and Hamed Zamani},
	booktitle={Thirty-fifth Conference on Neural Information Processing Systems Datasets and Benchmarks Track (Round 2)},
	year={2021},
	url={https://openreview.net/forum?id=8Y50dBbmGU}
}
```