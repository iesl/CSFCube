### Description of dataset:
This dataset accompanies a paper under review at the [SIGIR 2021 Resource Track](http://sigir.org/sigir2021/call-for-resource-papers/index.html).

**Title**: "CSFCube -- A Test Collection of Computer Science Papers for Faceted Query by Example"

**Authors**: Sheshera Mysore, Tim O'Gorman, Andrew McCallum, Hamed Zamani

**Abstract**: Query by example is a well-known information retrieval task in which a document is chosen by the user as the search query and the goal is to retrieve relevan documents from a large collection. However, a document often covers multipl aspects of a topic. In this paper, we introduce the task offaceted query by example in which users can also provide a facet in addition to the input document. We focuses on the application of this task in scientific literature search. We envision models which are able to retrieve scientific papers analogous to a query scientific paper along specifically chosen rhetorical structure elements as one solution to this problem. In this work, the rhetorical structure elements, which we refer to as facets,  indicate background, method, or results aspects of a scientific paper. In this work we introduce and describe an expert annotated test collection to evaluate models trained to perform this task. Our test collection consists of a diverse set of 50 query documents, drawn from computational linguistics and machine learning venues. We carefully followed the annotation guideline used by TREC for depth-k pooling (k = 100 or 250) and the resulting data collection consists of graded relevance scores with high annotation agreement. The data is freely available for research purposes.

### Contents:

		├── abstracts-csfcube-preds.jsonl
		├── ann_guidelines.pdf
		├── queries-release.csv
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

### Forthcoming:
1. Datasheet.
2. Script to generate test and development scripts for the dataset. 
3. License for dataset.

