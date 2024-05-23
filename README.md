# Project Title: ASGM-KG: Unveiling the Dynamics of Alluvial Gold Mining Through Knowledge Graphs


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

 
# Brief Description of the Paper
## Output of RDF

# Brief Desription of Downstream Task
- Query the knowledge graph
- Summary of the knowledge graph
- Chat with the knowledge graph
