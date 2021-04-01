### Description of dataset:
This dataset accompanies the following paper under review at the [SIGIR 2021 Resource Track](http://sigir.org/sigir2021/call-for-resource-papers/index.html):

**Title**: "CSFCube -- A Test Collection of Computer Science Papers for Faceted Query by Example"

**Authors**: Sheshera Mysore, Tim O'Gorman, Andrew McCallum, Hamed Zamani

**Abstract**: Query by example is a well-known information retrieval task in which a document is chosen by the user as the search query and the goal is to retrieve relevant documents from a large collection. However, a document often covers multiple aspects of a topic. In this paper, we introduce the task of faceted query by example in which users can also provide a facet in addition to the input document. We focuses on the application of this task in scientific literature search. We envision models which are able to retrieve scientific papers analogous to a query scientific paper along specifically chosen rhetorical structure elements as one solution to this problem. In this work, the rhetorical structure elements, which we refer to as facets,  indicate background, method, or results aspects of a scientific paper. In this work we introduce and describe an expert annotated test collection to evaluate models trained to perform this task. Our test collection consists of a diverse set of 50 query documents, drawn from computational linguistics and machine learning venues. We carefully followed the annotation guideline used by TREC for depth-k pooling (k = 100 or 250) and the resulting data collection consists of graded relevance scores with high annotation agreement. The data is freely available for research purposes.

The paper describing the dataset can be accessed here: https://arxiv.org/abs/2103.12906   

### Usage

Please use the appropriate [release](https://github.com/iesl/CSFCube/releases) to download salient releases of the dataset.


### Contents:

		├── abstracts-csfcube-preds.jsonl
		├── ann_guidelines.pdf
		├── queries-release.csv
		├── README.md
		├── LICENSE.md
		├── datasheet.md
		├── evaluation_splits.json
		├── readable_annotations
		│   ├── 10010426-method-adju.txt
		│   ├── 10014168-background-adju.txt
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

`readable-annotations`: Directory of 50 text files for browsing the annotations -- with one file per query-facet pair. Candidates for every query are sorted by adjudicated relevance.

`test-pid2anns-csfcube-{background/method/result}.json`: JSON file with the query paper-id, candidate paper-ids for every query paper in the test collection. Use these files in conjunction with `abstracts-csfcube-preds.jsonl` to generate files for use in model development/evaluation. 

`test-pid2pool-csfcube.json`: JSON file query paper-id, candidate paper-ids and the methods which caused the candidate to be included in the pool. The methods are one among `{abs_tfidf, abs_cbow200, abs_tfidfcbow200, title_tfidf, title_cbow200, title_tfidfcbow200, specter, cited}`. This file is included to facilitate further analysis of the dataset.

`evaluation_splits.json`: Paper-ids for the splits to use in reporting evaluation numbers. Please see the paper and `datasheet.md` for the experimental protocol we recommend to report numbers.   

`datasheet.md`: Following recommended practice to report the details of the a dataset, we provide a Datasheet following prompts provided in [Bender et. al. 2018](https://www.aclweb.org/anthology/Q18-1041/) and [Gebru et. al. 2018](https://arxiv.org/abs/1803.09010).

`LICENSE.md`: The dataset is released under the [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) license. 

### Acknowledgments: 

This dataset was built using the [Semantic Scholar Open Research Corpus](https://github.com/allenai/s2orc)(S2ORC). This dataset also uses the pre-trained models of [sequential_sentence_classification](https://github.com/allenai/sequential_sentence_classification) and [SPECTER](https://github.com/allenai/specter).
