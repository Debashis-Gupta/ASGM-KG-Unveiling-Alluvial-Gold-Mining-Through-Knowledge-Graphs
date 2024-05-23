import os
import pandas as pd
from rdf_extraction import RDF_extraction
from DAS_validation import DAS_Validation,create_rdf_dataset
from tqdm import tqdm

def find_pdf_files(directory):
    pdf_files = []
    # Walk through all files and folders in the specified directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check if the file ends with .pdf
            if file.endswith(".pdf"):
                # Append the full path of the file to the list
                pdf_files.append(file)
    return pdf_files

def main():
    pdf_directory = "data/pdf/"
    data_dir = "Output/"
    cookies_path= None # please include your cookies - check the code/README.md
    pdf_files = find_pdf_files(pdf_directory)
    for file in pdf_files:
        RDF_extraction(pdf_path=file,cookies_path=cookies_path,output_filename=None)
    
    dataframe = pd.DataFrame()
    dataframe = create_rdf_dataset(directory_path=data_dir)
    dataframe = dataframe.reset_index(drop=True)
    column_names = ['Subject', 'Predicate', 'Object', 'Is_The_Triple_Valid', 'Sequence of Validation', 'Reason', 'Web_Ref', 'Highest_Page_Rank']

    # Create an empty DataFrame with these columns
    final_data = pd.DataFrame(columns=column_names)
    garbage_data = pd.DataFrame(columns=column_names)
    output_directory =None
    if output_directory is None:
        print("Please specify a directory to save the KNOWLEDG GRAPH AFTER VALIDATION. Default is 'Output'.")
        output_directory ='Output'
        os.makedirs(output_directory,exist_ok=True)
        
    for i in tqdm(range(len(dataframe)), desc="Walking"):
        try:
            entity1 = dataframe['Subject'][i]
            relation = dataframe['Predicate'][i]
            entity2 = dataframe['Object'][i]
            new_row_df = pd.DataFrame()
            new_row_df = DAS_Validation(entity1, relation, entity2,cookies_path=cookies_path).copy()
            final_data = pd.concat([final_data, new_row_df], ignore_index=True)
            output_file_path = os.path.join(f'{output_directory}', 'DAS_validated_KG.csv')
            final_data.to_csv(output_file_path, index=False)

        except Exception as e:
            print(f"An error occurred at iteration {i}: {e}")
            final_data = pd.concat([final_data, garbage_data], ignore_index=True)
            output_file_path = os.path.join(f'{output_directory}', 'DAS_validated_KG.csv')
            final_data.to_csv(output_file_path, index=False)
            continue  
    
    
if __name__ == "__main__":
    main()