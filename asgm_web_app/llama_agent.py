from langchain_community.document_loaders import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import CTransformers
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
import sys
from summary import create_summary

def extract_entity_relations(documents):
    results = []
    for document in documents:
        parts = document.page_content.split('\n')
        entity1 = parts[0].split(': ')[1].strip()
        relation = parts[1].split(': ')[1].strip()
        entity2 = parts[2].split(': ')[1].strip(':')
        results.append([entity1, relation, entity2])
    return results

loader = CSVLoader(file_path="data.csv",encoding="utf-8",csv_args={'delimiter':','})
data = loader.load()

# print(data)

# split the data into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=20)
text_chunks = text_splitter.split_documents(data)

# print(len(text_chunks))

# Download the sentence transformers embedding from the hugging face
embeddings = HuggingFaceEmbeddings(model_name= 'sentence-transformers/all-MiniLM-L6-v2')

#converting the text chunks into embeddings and savings the embeddings into FAISS knowledge Base
docsearch = FAISS.from_documents(text_chunks,embeddings)
docsearch.save_local('DB_FAISS_PATH/')

# query = "What is the impact of mercury?"
def ask_query(query):
    # query = input("Question:")
    docs = docsearch.similarity_search(query,k=10)
    # print("Result",docs)

    extracted_info = extract_entity_relations(docs)
    print(extracted_info)

    response = create_summary(extracted_info)
    print(f"Response: {response}")
    # response = response.split('|')[1]
    # response=response.split('\n')[1]
    response = response.replace('Summary','Answer:')
    
   
    return response

