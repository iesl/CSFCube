Following recommended practice to report the details of the a dataset, we provide a Datasheet following prompts provided in [Bender et. al. 2018](https://www.aclweb.org/anthology/Q18-1041/) and [Gebru et. al. 2018](https://arxiv.org/abs/1803.09010).

### Motivation

Q: For what purpose was the dataset created?    
A: The dataset was created as an evaluation set for measuring information retrieval methods for a faceted Query by Example task in scientific papers. The nature of similarity judgments are meant to facilitate development of models which capture relational similarities between aspects (background, method, result) of a scientific papers, these kinds of similarities have been important for creative activities like scientific research. Our paper and `ann_guidelines.pdf` elaborate on similarity guidelines in more detail.

Q: Who created the dataset and on behalf of which entity?       
A: The dataset was created by researchers at the [Center for Intelligent Information Retrieval](https://ciir.cs.umass.edu/) and the [Information Extraction and Synthesis Laboratory](https://www.iesl.cs.umass.edu/) at the University of Massachusetts Amherst on behalf of those same entities. 

Q: Who funded the creation of the dataset?     
A: TODO.

### Composition

Q: What do the instances that comprise the dataset represent? How many instances are there in total (of each type, if appropriate)?         
A: The dataset may be viewed from a handful different perspectives: The dataset may be seen as consisting of 50 query abstracts. These are abstracts from scientific papers appearing in the NLP publication venues. Each of the 50 queries have either 250 or 100 other candidate abstracts labeled for similarity with respect to the query along one of 3 "facets". Therefore each of the query abstracts is also paired with one of 3 query facets. In all, the dataset consists of 6244 query-candidate pairs. All abstracts are also paired with the corresponding paper title and have a potential incomplete set of bibliographic (authors, publication venue and year, doi etc) information.

Q: Does the dataset contain all possible instances or is it a sample of instances from a larger set?     
A: The dataset is a sample from a larger set. The query abstracts are drawn from the ACL Anthology. The candidate abstracts are drawn from computer science papers from arXiv which were included in the [Semantic Scholar Open Research Corpus](https://github.com/allenai/s2orc) (S2ORC). 

Q: Is there a label or target associated with each instance?      
A: Each query-candidate pair is rated on a scale of 0-3 indicating the relevance of the candidate abstract to the query abstract along the query facet. The definitions of relevance are detailed in the `ann_guidelines.pdf`.

Q: Is any information missing from individual instances?        
A: Bibliographic information (`metadata` fields in the `abstracts-csfcube-preds.jsonl` file) for the abstracts was drawn from that present in the S2ORC corpus. This information may be incomplete.

Q: Are relationships between individual instances made explicit (e.g., users movie ratings, social network links)?	  
A: Individual papers (abstracts of which are in the dataset) are part of the citation network, this information is missing from this dataset but it could be obtained from the S2ORC corpus.

Q: Are there recommended data splits (e.g., training, development/validation, testing)?     
A: The dataset only represents an evaluation set for the tasks it was developed for. Therefore it only consists of development and test splits. We recommend reporting results for each of the facets in the dataset (background, method, result) separately. For each split per facet we follow a 2-fold cross validation approach where half the queries are considered dev and a the other half test, this is done 2 times. Results per query are averaged across the development splits in the 2 folds to obtain the development metric and the scores across the test splits in the two folds give the test score metric.

Q: Are there any errors, sources of noise, or redundancies in the dataset?      
A: The dataset was built from abstracts, titles, metadata, and the citation network included as part of the S2ORC corpus. Several elements of this corpus were constructed using automatic tools to obtain paper metadata, abstracts, citation span information and so on. This introduces an element of noise in our dataset, for example some candidate abstracts can be noisy (query abstracts were filtered for noise manually). Further the query and candidate abstracts sentences have a label indicating the facet for the sentence, this label was automatically predicted (using this model: [link](https://github.com/allenai/sequential_sentence_classification)) and corrected for the query abstracts but not for the candidate abstracts. Incorrect predictions persist in the dataset.

Q: Is the dataset self-contained, or does it link to or otherwise rely on external resources (e.g., websites, tweets, other datasets)?      
A: The dataset is self contained.

Q: Does the dataset contain data that might be considered confidential?      
A: No.

Q: Does the dataset contain data that, if viewed directly, might be offensive, insulting, threatening, or might otherwise cause anxiety?      
A: No.

Q: Does the dataset relate to people?      
A: The dataset relates to people in-as-much as it consists of research papers the authors of are included as part of the metadata.

Q: Does the dataset identify any subpopulations (e.g., by age, gender)?      
A: No.

Q: Is it possible to identify individuals (i.e., one or more natural per- sons), either directly or indirectly (i.e., in combination with other data) from the dataset?      
A: The authors of individual papers included in the dataset are present as part of metadata. If absent, web searches can easily reveal authors.

Q: Does the dataset contain data that might be considered sensitive in any way?    
A: No.

Q: Speaker demographic and Language Variety following [Bender et al. 2018](https://www.aclweb.org/anthology/Q18-1041/).      
A: The text of the abstracts is primarily academic writing in English.  

Q: Annotator demographics following [Bender et al. 2018](https://www.aclweb.org/anthology/Q18-1041/):       
The dataset was annotated by 4 annotators. The bucketed demographics are as follows:      
Ages- 26-30: 2, 20-25: 1, 31-35: 1      
Gender Identity- Man: 3, Woman: 1       
National Identity- Indian: 3, USA: 1       
Race- Asian: 3, White: 1       
Languages spoken, read or otherwise understood by annotators- English: 4, Hindi: 3, Arabic: 1, Tamil: 1, Telugu: 1, Malayalam: 1, Kannada: 1, Marathi: 1      

### Collection Process

Q: What mechanisms or procedures were used to collect the data (e.g., hardware apparatus or sensor, manual human curation, software program, software API)?      
A: The dataset is used as is from the S2ORC corpus. Our process for selecting query was a mix of manual curation and automatic selection. `ann_guidelines.pdf` details this process.

Q: If the dataset is a sample from a larger set, what was the sampling strategy (e.g., deterministic, probabilistic with specific sampling probabilities)?      
A: While `ann_guidelines.pdf` details the process of collecting the queries and candidate abstracts. The 800,000 computer science papers in this dataset were obtained from the S2ORC corpus as follows: 1. Papers tagged with "Computer Science" in the `mag_fos` field and with a non-null `has_arxiv_id` field in the S2ORC metadata tsv files selected to ensure computer science papers with likely full body text available. This resulted in about 140k papers. 2. For these papers all the outgoing citations which are part of the S2ORC corpus were obtained. This resulted in about 1.2 million papers. 3. For these papers any of the following filters based on sentences (nltk.tokenize.sent_tokenize) and tokens (white space split the sentence) evaluating to true excludes the paper: abstract has fewer then 3 sentences, abstract has greater then 20 sentences, any sentence is greater than 80 tokens, or all sentences have fewer than 4 tokens. This procedure results in about 800,000 abstracts based on which the remainder of the corpus is built.

Q: Who was involved in the data collection process (e.g., students, crowdworkers, contractors) and how were they compensated (e.g., how much were crowdworkers paid)?      
A: One graduate student, a post doc and 2 hired annotators (both graduate students) were involved in creation of the dataset. Both hired annotators were paid $22.5/hour for 25 hours of work for a period of 3 weeks.

Q: Over what timeframe was the data collected?      
A: Initial rounds of exploratory annotation were carried out over October 2020-December 2020. The dataset released here was annotated from January 2021-February 2021.

Q: Were any ethical review processes conducted (e.g., by an institutional review board)?      
A: The release of demographic information of annotators was reviewed by the University of Massachusetts Amherst Human Research Protection Office (HRPO) and determined as not meeting the definition of human subjects research (and hence exempt from IRB review). No other elements of the project were reviewed by research ethics compliance bodies.

Q: Did you collect the data from the individuals in question directly, or obtain it via third parties or other sources (e.g., websites)?      
A: Scientific papers were gathered from the S2ORC corpus. Relevance judgments were made directly by individual annotators.

Q: Were the individuals in question notified about the data collection?      
A: No.

Q: Did the individuals in question consent to the collection and use of their data?      
A: NA.

Q: If consent was obtained, were the consenting individuals provided with a mechanism to revoke their consent in the future or for certain uses?   
A: No.

Q: Has an analysis of the potential impact of the dataset and its use on data subjects been conducted?    
A: No.   

Q: Was any preprocessing/cleaning/labeling of the data done?    
A: Aside from the data filtering for excluding noisy data described above no other pre-processing was applied on the data.

Q: Was the "raw" data saved in addition to the preprocessed/cleaned/labeled data (e.g., to support unanticipated future uses)?     
A: NA.

Q: Is the software used to preprocess/clean/label the instances available?      
A: This will be released in future.

### Uses

Q: Has the dataset been used for any tasks already?    
A: No.

Q: Is there a repository that links to any or all papers or systems that use the dataset?      
A: No.

Q: What (other) tasks could the dataset be used for?    
A: The dataset is intended for the two formulations of the faceted Query by Example task as described in the paper accompanying the dataset. Additionally it is conceivable this could be used for evaluating methods which diversify retrieved papers along different facets (using the 16 query papers which have been rated for similarity along 2 different facets each). The dataset can also be used to evaluate a range of other methods which present methods of measuring general scientific paper similarity.

Q: Is there anything about the composition of the dataset or the way it was collected and preprocessed/cleaned/labeled that might impact future uses?    
A: None that we are aware of.

Q: Are there tasks for which the dataset should not be used?     
A: None that we can think of.

### Description

Q: Will the dataset be distributed to third parties outside of the entity (e.g., company, institution, organization) on behalf of which the dataset was created?     
A: Yes.     

Q: How will the dataset will be distributed (e.g., tarball on website, API, GitHub)?      
A: GitHub. Please use the appropriate [release](https://github.com/iesl/CSFCube/releases) to download salient releases of the dataset.      

Q: When will the dataset be distributed?     
A: The dataset has been publicly available since March 3rd 2021.

Q: Will the dataset be distributed under a copyright or other intellectual property (IP) license, and/or under applicable terms of use (ToU)?   
A: The dataset is released under the [Creative Commons Attribution-NonCommercial 4.0 International](https://creativecommons.org/licenses/by-nc/4.0/legalcode) license.

Q: Have any third parties imposed IP-based or other restrictions on the data associated with the instances?     
A: None.

Q: Do any export controls or other regulatory restrictions apply to the dataset or to individual instances?     
A: None.

### Maintenance

Q: Who is supporting/hosting/maintaining the dataset?    
A: Sheshera Mysore (smysore@cs.umass.edu)

Q: How can the owner/curator/manager of the dataset be contacted?    
A: Yes.

Q: Is there an erratum?    
A: None yet.

Q: Will the dataset be updated (e.g., to correct labeling errors, add new instances, delete instances)?    
A: If sufficiently large errors are discovered the dataset will be corrected and updated version of it will be released. We will use the "Releases" feature on Github to denote all salient releases.