# Project Title: ASGM-KG: Unveiling the Dynamics of Alluvial Gold Mining Through Knowledge Graphs


# Brief Description of the Paper

<div style="text-align: justify">

This paper, **"ASGM-KG: Unveiling the Dynamics of Alluvial Gold Mining Through Knowledge Graphs,"** represents the inaugural effort to systematically apply a Knowledge Graph (KG) to the study of artisanal and small-scale gold mining (ASGM). This research addresses a significant gap by constructing the first known dataset and knowledge graph dedicated to ASGM, highlighting its environmental and health impacts, particularly mercury pollution in tropical forests. This pioneering work is crucial, as ASGM is a major contributor to environmental degradation yet has been understudied in this structured and accessible format.

**Resource Description Framework (RDF):** At the core of ASGM-KG is the Resource Description Framework (RDF), a standard model for data interchange on the Web. RDF uses a triple-based structure to link data points, making it an essential tool for developing knowledge graphs. This framework facilitates the integration of diverse data sources into a unified, queryable structure, enabling complex relationships and dependencies within the ASGM domain to be mapped and analyzed systematically.

Our **contribution** through ASGM-KG is pivotal, as it introduces the first dataset that encapsulates validated and structured information about ASGM impacts, which can guide policymakers and researchers. The methodology leverages advanced Natural Language Processing powered by large language models for RDF triple extraction from varied texts, followed by a meticulous validation via our novel **Data Assessment Semantics (DAS) framework**. Experimentally, ASGM-KG has proven effective, aligning with verified data sources and enabling robust querying and data interpretation. The significance of our work lies in its application to environmental monitoring and policy-making, potentially serving as a blueprint for addressing similar challenges in other sectors.

</div>


## Instructions for Reproducing The Result
<div style="text-align: justify">

The code has been written in python programming language and put into the **code** directory. Before running the code, please install the requirements.txt file using the following command

</div>

`
pip install -r requirements.txt
`

<div style="text-align: justify">

After installing all the required packages, ensure that the following configurations -
1. Take the session of co-pilot GPT-4 (*pro if you have*) and create a **cookies.json** file in the **code** directory.
2. Get API-key of page rank from [open-page-rank](https://www.domcop.com/openpagerank/what-is-openpagerank) website.
3. If you want to extract the information from the PDFs itself, please see the TABLE-2 of the paper and the corresponding listed urls and download the pdfs and save them in the **data/pdf** directory.

In the **code** folder, the ***rdf_extraction.py*** (as shown by Figure 2 in the paper) file contains the code of extracting the RDF format from the PDF and save the extracted information in csv format to the specified folder by the user (if not provided, the default directory is **Output**).

The **RDF_extraction** function takes three arguments - pdf_path, cookies_path, and output_filename. **pdf_path, and cookies_path** are required however if **output_filename** is not provided the default output_filename will be assigned to **Output**.

The **DAS_validation.py** is responsible for validating the extracted RDF in realtime as shown in Figure 3 in the paper using **DAS_validation** which takes four arguments, entity1, relation, entity2 and cookies_path. Here entity1,relation, and entity2 refer to the Subject, Predicate and Object properties of the RDF. 

You need to run only the **main.py** file in the code directory to regenerate the experimental results using the following command 

`python3 code/main.py`

In the main function, we are doing the following things -
1. Getting the pdfs from the **data/pdf** directory.
2. Setting up the file path of cookies.json file.
3. Extracting the pdfs using RDF_extraction function.
4. creating the main dataframe of extracted information from step 3 using **create_rdf_dataset** function.
5. Finally, we are validating each of the extracted RDF triples using our DAS Validation framework by calling the **DAS_Validation** function.

</div>



## Sample Output Discussion

### RDF extracted from RDF_extraction

<div style="text-align: justify">

A sample output from the RDF extraction looks like below:

| Subject                  | Predicate  | Object            |
|--------------------------|------------|-------------------|
| amazon region                  | contains   | biodiversity   |
| amazon region | source of | water |
|amazon region| source of | food |
|gold mining | source of | livelihoods |
|gold mining | source of | income |
|mercury| released in| water |
|mercury| contaminates|plants|
|mercury| contaminates| animals |

This is an example of extraction from the following text -

**"The Amazon region is a unique environmental icon.
Spanning more than a third of the South American continent, it
contains the greatest share of biodiversity in the world. Further,
it is home to more than 34 million human inhabitants, including
some 3 million indigenous peoples. It is an invaluable source of
water, food, shelter, medicines, and culture to these people of
diverse origins, stretching back thousands of years.
However, today the Amazon is under threat. Artisanal and small-
scale gold mining is a prominent source of livelihoods and income
in the region. These informal, unregulated operations make
heavy use of mercury in the gold purification process, which is
then released into the water and air. This mercury is carried far
from the mines, irreversibly contaminating plants and animals
throughout the region."**

### Constructing Knowledge Graph ASGM using DAS Validation Framework

A sample output of our **DAS Validation** framework is following:

| **Subject**              | **Predicate** | **Object**        | **Factual Validation** | **Logical Reasoning**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | **Web Reference** | **Page Rank**                                                  |
|--------------------------|---------------|-------------------|------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------|------------------|
| mercury                  | found in      | amazonian soils   | Yes                    | Research indicates that mercury is indeed found in Amazonian soils. The soils of the Amazon rainforest, including the lowland Amazon, are known to be rich in mercury. This mercury accumulation can be attributed to natural processes such as geologic weathering, erosion from deforestation, and atmospheric deposition. Therefore, the triple (mercury, found in, amazonian soils) is valid. The reference text mentions that a study was conducted on the soil of the Amazon rainforest, specifically in the Tapajos National Forest in Brazil. The study analyzed 11 soil profiles at depths of 0-40 cm and determined the contents of major oxides and mercury ($\mu$g kg$^{-1}$) in the soil and rock. The mercury content in the soil averaged 240 $\mu$g kg$^{-1}$. Therefore, the statement that mercury is found in Amazonian soils is valid. The reference text mentions that the total mercury ($\mu$g kg$^{-1}$) ranged from 21.5 to 208 $\mu$g kg$^{-1}$ in the studied Amazon soils. This indicates that mercury is indeed found in Amazonian soils. | 1.http://www.nature.com/articles/s41467-022-27997-3 <br>2.http://link.springer.com/article/10.1007/s12665-018-7471-x<br>3.http://pubmed.ncbi.nlm.nih.gov/36063907/ | 9.5, 8.0,7.5|
| brazil national databank | introduced    | conama resolution | No                     | Based on the information available, there is no evidence to suggest that the brazil national databank introduced the conama resolution. The CONAMA resolution is established by the National Council for the Environment (Conselho Nacional do Meio Ambiente), or CONAMA, part of the Ministry of Environment (Ministério do Meio Ambiente) in Brazil. There is no mention of a brazil national databank being involved in the introduction of the CONAMA resolution.Based on the information available, there is no evidence to suggest that the brazil national databank introduced the conama resolution. The conama resolution is a set of environmental regulations established by the National Council for the Environment (Conselho Nacional do Meio Ambiente), or CONAMA, part of the Ministry of Environment (Ministério do Meio Ambiente) in Brazil. There is no mention of the brazil national databank being involved in the introduction of these regulations. Based on the information available, there is no evidence to suggest that the brazil national databank introduced the conama resolution. The conama resolution is a set of environmental regulations established by the National Council for the Environment (Conselho Nacional do Meio Ambiente), or CONAMA, part of the Ministry of Environment (Ministério do Meio Ambiente) in Brazil. There is no mention of the `brazil national databank' in relation to the introduction of these resolutions. | 1.https://www.nature.com/articles/s41597-024-03068-8<br>2. https://www.academia.edu/40765924/Aspects\_that\_should\_be\_considered\_in\_a\_possible\_revision\_of\_the\_Brazilian\_Guideline\_Conama\_Resolution\_357\_05 <br>3. https://braziliannr.com/brazilian-environmental-legislation/conama-resolution-39307/  | 9.0,8.5,7.5|


As shown in the table, the output of DAS framework contains the RDF triplet (Subject, Predicate and Object), followed by the Factual Validation based on the Logical Reasoning of LLM model applied to the top K most web references according to the Page-Rank's relevancy and coherence score sorted. For demonstration purposes and limited resource, we took the top most reference and context K as 3 which can be increased according to the available resources. Our final resultant knowledge graph on ASGM (ASGM-KG) is validated by this approach and only the factually correct information is mostly considered to be included in the graph.


### Performance of DAS Validation AGAINST CoDEx-S Dataset
As mentioned in the paper, DAS validation framework has been applied to the *CoDEx: A Comprehensive Knowledge Graph Completion Benchmark* small dataset (CODEX-S) that contains 1838 positive and negative triplet based on Wikidata and Wikipedia data. While applying the DAS validation framework, this framework not only outperforms the existing model on classifying the triplet mentioned in the CoDEx paper, but it also successfully indentifies the mislabeled triplet. The following table shows the results of DAS validation framework on CoDEx-S dataset -

| **Subject**         | **Predicate**                        | **Object** | **Logical Reasoning**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | **Web Reference**                                                                                                                                                                                                                       | **GT** | **PR** | **AGT** |
|---------------------|-------------------------------------|-------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|--------|---------|
| Michail Sholokhov   | ethnic group                        | Russians    | Michail Sholokhov was a Russian novelist. His father was a Russian. Therefore, it is valid to say that his ethnic group is Russian. The text mentions that Michail Sholokhov is a Russian writer, which implies that his ethnic group is Russians. The text mentions Mikhail Sholokhov and discusses his work in the context of Russian literature and history, implying that he is part of the Russian ethnic group.                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | [Link1](https://en.wikipedia.org/wiki/Mikhail_Sholokhov) <br> [Link2](https://en.wikipedia.org/wiki/And_Quiet_Flows_the_Don) <br> [Link3](https://link.springer.com/chapter/10.1007/978-3-030-62982-3_33)                                 | Yes    | Yes    | Yes     |
| Moldova             | continent                            | Asia        | Moldova is located in Europe, not Asia. Moldova is described as a landlocked country in Eastern Europe on the northeastern corner of the Balkans in the provided text. It is not located in Asia. Moldova is mentioned as a country in Europe in the provided text. Therefore, it's not in Asia.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | [Link1](https://en.wikipedia.org/wiki/Moldova) <br> [Link2](https://en.wikipedia.org/wiki/Portal:Moldova) <br> [Link3](https://www.bbc.com/news/world-europe-17601580)                                                                     | No     | No     | No      |
| Laurie Anderson     | place of birth                       | Chicago     | Laurie Anderson was born in Glen Ellyn, Illinois, not in Chicago. Laurie Anderson was born in Wayne, Illinois, not Chicago. The reference text indicates that Laurie Anderson was born in Wayne, Illinois, not Chicago.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | [Link1](https://en.wikipedia.org/wiki/Laurie_Anderson) <br> [Link2](https://www.npr.org/sections/deceptivecadence/2021/04/13/978134291/catching-up-with-laurie-anderson-an-artist-always-ahead-of-her-time) <br> [Link3](https://www.britannica.com/biography/Laurie-Anderson) | Yes    | No     | Yes     |
| Mark Twain          | languages spoken, written, or signed | Italian     | Mark Twain, the renowned author, had an interest in the Italian language. He wrote a short story titled "Italian Without a Master" while he was in Florence, Italy. In this story, he humorously interprets the Italian language. This indicates that he had some understanding of Italian, even if he wasn't fluent. Therefore, it can be inferred that Mark Twain could at least partially understand and interpret Italian. The reference text mentions that Mark Twain was fond of the Italian dialect and it was his favorite method of learning Italian. This suggests that he had some knowledge of the Italian language. The reference text indicates that while Mark Twain was living in Italy, he did not speak Italian fluently. He communicated in English and used an Italian word when he had one, but he did not understand the language fully. Therefore, it would be incorrect to say that he spoke, wrote, or signed Italian. | [Link1](https://en.wikipedia.org/wiki/Mark_Twain) <br> [Link2](http://www.twainquotes.com/interviews/critic1904.html) <br> [Link3](https://www.classicshorts.com/stories/ItalianMaster.html)                                                  | No     | Yes    | No      |



This Table shows a summary of our framework while applying on the Codex-S test dataset describing the result of the triples from positive and negative triples indicated by ground truth (GT) column, the prediction (PR) refers the output of the framework and actual ground truth (AGT) actual label of the ground truth by cross-checking the open-source knowledge and expert opinion. The Web Reference and Logical Reasoning columns show the context of the top 3 Web references and the explanation behind the prediction of the framework respectively. Whenever the `GT = AGT` and `PR = GT` then it implies that our framework correctly labels the triple and if `PR ≠ GT` but `PR = AGT` this implies the ground truth (GT) is wrong labeled.


</div>

# Brief Desription of Downstream Task
- Query the knowledge graph
- Summary of the knowledge graph
- Chat with the knowledge graph



### Corresponding Author
Debashis Gupta <br>
Email: guptd23@wfu.edu
### License and Copyright
This project is developed and copyright reserved by the computer scientist and biologist expert of Wake Forest’s Intelligent Remote Sensing in Conservation & Discovery Group [(IRSC Lab)](https://irsc-wfu.github.io/). Please contact Prof. Dr. Paul Pauca or Dr. Sarra Alqahtani for further information. 
<div style="display: flex; justify-content: flex-start;">
  <div style="margin-right: 50px;">
    <strong>V. Paúl Pauca</strong><br>
    Professor<br>
    Department of Computer Science<br>
    Wake Forest University
  </div>
  <div>
    <strong>Sarra Alqahtani</strong><br>
    Assistant Professor<br>
    Department of Computer Science<br>
    Wake Forest University
  </div>
</div>
