import pandas as pd
import PyPDF2
import time
import os
import re
from pathlib import Path
import numpy as np
import asyncio
import json
import time
from pathlib import Path

from re_edge_gpt import Chatbot
from re_edge_gpt import ConversationStyle
import nest_asyncio

import requests
from bs4 import BeautifulSoup
import re
from logging import exception
import pandas as pd
import re
import time
from tqdm import tqdm
import time
import pandas as pd
import os
from io import StringIO
import re
from duckduckgo_search import DDGS, AsyncDDGS
from rdf_extraction import Ask_Copilot
api = None #You will need API key from https://www.domcop.com/openpagerank/what-is-openpagerank
headers = {'API-OPR':api}

def clean_text(text):
    # Regex to remove citations and unwanted markers
    cleaned_text = re.sub(r'\[\^[^\]]*\]', '', text)  # Remove citations like [^1^]
    cleaned_text = re.sub(r'\b(nan\b)', '', cleaned_text)  # Remove 'nan'
    cleaned_text = re.sub(r'[\r\n]+', '\n', cleaned_text)  # Remove extra new lines
    cleaned_text = re.sub(r'[-]+\n', '', cleaned_text)  # Remove lines with dashes
    cleaned_text = re.sub(r'---', '', cleaned_text)  # Remove lines with ---
    return cleaned_text.strip()

def create_rdf_dataset(directory_path=None):
    if directory_path is None:
       print("Directory path is not assigned so the default is 'Output'")
       directory_path='Output'
       os.makedirs(directory_path,exist_ok=True)
    # List to store dataframes
    dataframes = []

    # Iterate through each file in the directory
    for file in os.listdir(directory_path):
        # Check if the file is a CSV
        if file.endswith('.csv'):
            # Construct full file path
            file_path = os.path.join(directory_path, file)
            # Read the CSV file and append to list
            df = pd.read_csv(file_path)
            dataframes.append(df)

    # Concatenate all dataframes along the columns
    merged_df = pd.concat(dataframes, axis=0, ignore_index=True)

    # Save the merged dataframe to a new CSV file
    output_file_path = os.path.join(directory_path, 'rdf_dataset.csv')
    merged_df.to_csv(output_file_path, index=False)
    print(f"RDF dataset Has been created successfully at {directory_path}")
    return merged_df

def url_content_extraction(url, printType=False, timeout_seconds=60):
    try:
        # Fetch the content from the URL with a timeout
        response = requests.get(url, timeout=timeout_seconds)

        # Check if the request was successful
        response.raise_for_status()

        # Use BeautifulSoup to parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract text from the <body> tag
        body_text = soup.body.get_text(separator=' ', strip=True)

        # Clean the extracted text
        cleaned_text = re.sub(r"[^a-zA-Z0-9\s.?!]", "", body_text)
        cleaned_words = [str(word) for word in cleaned_text.split(" ")]
        cleaned_text = " ".join(cleaned_words)

        return cleaned_text

    except requests.exceptions.Timeout as e:
        # Handle timeout specifically
        #print(f"Request timed out: {e}")
        return None

    except requests.exceptions.RequestException as e:
        # Handle errors during the request to the URL
        #print(f"Error fetching the URL: {e}")
        return None

    except Exception as e:
        # Handle any other exceptions that may occur
        #print(f"An error occurred: {e}")
        return None
def DAS_Page_Rank(results):
  #### Getting only the weblinks ####
  urls = []
  text_body = []
  for url in results:
  # Working with full body content
  # print(f"Url : {url['href']}")
    try:
      urls.append(url['href'])
      query = url['href']
      #print(query)
      #print(type(query))
      # print(f"After Replacing : {query}")
      # quoted_url = '"' + query + '"'
      # print(f"Quated URL: {quoted_url}")
      # 403 Forbidden
      content = url_content_extraction(query)
      if "403 Forbidden" in content:
        urls.pop()
        continue
      elif "Request blocked" in content:
        urls.pop()
        continue
      content = url['body'] + content
      #print(content)
      text_body.append(content)
      time.sleep(1.5)

    except Exception as e:
      #print(f"Problem url : {url['href']}")
      #print(e)
      urls.pop()

    # Working with short body text
    # urls.append(url['href'])
    # text_body.append(url['body'])


  #### Getting weblinks that can be ranked ####
  simple_urls=[]

  pattern = r"https?:\/\/([^\/]+)"

  for url in urls:
    match = re.search(pattern, url)
    if match:
        simple_urls.append(match.group(1))


  #### Getting rank response from open_page_rank ####
  rank_responses = []
  for url in simple_urls:
    domain = url
    url = 'https://openpagerank.com/api/v1.0/getPageRank?domains%5B0%5D=' + domain
    request = requests.get(url, headers=headers)
    rank_response = request.json()
    #print(rank_response)
    rank_responses.append(rank_response)

  #### Extracting data from rank responses ####
  page_rank_integer = []
  page_rank_decimal = []
  rank = []

  # Function to extract the details
  for item in rank_responses:
      response = item.get('response', [])
      for resp_item in response:
          page_rank_integer.append(resp_item.get('page_rank_integer'))
          page_rank_decimal.append(resp_item.get('page_rank_decimal'))
          rank.append(resp_item.get('rank'))

  df = pd.DataFrame(urls, columns=['Urls'])
  df['Domains'] = simple_urls
  df["Page_Rank_int"] = page_rank_integer
  df["Page_Rank_decimal"] = page_rank_decimal
  df["Rank"] = rank
  df['Text'] = text_body

  #sorted_df = df.sort_values(by=['Rank','Page_Rank_decimal'], ascending=[True, False])
  sorted_df = df.sort_values(by=['Page_Rank_decimal'], ascending=[False]) #works good
  sorted_df = sorted_df.reset_index(drop=True)
  return sorted_df

def DAS_Validation(entity1, relation, entity2,cookies_path=None):
  if cookies_path is None:
     raise ValueError("Please provide a cookies_path")
  text = entity1 + " " + relation + " " + entity2
  #print(text)
  query = text
  query = query.replace('"', '')
  #### Using DAS_Page_Rank ####
  results = DDGS().text(query, max_results=25)
  page_rank_df = DAS_Page_Rank(results).copy()
  column_names = ['Subject', 'Predicate', 'Object', 'Is_The_Triple_Valid', 'Reason'] #Short_Reason

  # Create an empty DataFrame with these columns
  empty_df = pd.DataFrame(columns=column_names)

  text_body_for_val = page_rank_df.Text.values.tolist()[0:3]
  for text in tqdm(text_body_for_val,desc="Processing"):

    if len(text)>20000:
      text = text[20000]

    max_retries = 5
    retry_count = 0

    while retry_count < max_retries:
      try:
            # Attempt to access the 'Text' column
          prompt_for_validation = f"""
      Assume you are an expert researcher. Given the input text body called 'Text' followed by a number please find if the triple is valid or not for each text.
      Approach this with a mindset that allows for exploratory analysis and the recognition of uncertainty or multiple valid perspectives.
      If the triple(Subject, Predicate, Object) is valid you have to response with Yes, if the triple is invalid response with No. You should give a detailed reason for why you decided that. Use your vast knowledge of reasoning behind your reason of output for the "Reference".
      Just give output in a table format with headers like shown in the "Output". Is_The_Triple_Valid can only be Yes or No. Please don't write anything outside the table in the beginning or in the end. You have to give "Yes" or "No" reply
      for "Reference" body.

      Input:
      Subject : {entity1}
      Predicate : {relation}
      Object : {entity2}
      Reference : {text}



      Output:I expect one row of having values for the headers below. You don't need to print anything else.
      |Subject|Predicate|Object|Is_The_Triple_Valid|Reason|
      """
          # Assuming Ask_Copilot is a callable function that takes the prompt and returns a structured response
          #print(text)
          response = Ask_Copilot(prompt_for_validation,cookies_path)
          #print(response)
          # Extracting the table part of the text
          table_text = response.split('|Subject|', 1)[1]
          table_text = '|Subject|' + table_text  # Adding the header
            # Converting the table text into a DataFrame
          dataframe_for_response = pd.read_csv(StringIO(table_text), sep="|", skipinitialspace=True)
           # Removing the empty columns generated due to extra separators
          dataframe_for_response = dataframe_for_response.dropna(axis=1, how='all')

          # Remove rows where all columns contain dashes '---'
          dataframe_for_response = dataframe_for_response[~dataframe_for_response.apply(lambda x: all(x == '---'), axis=1)]
          dataframe_for_response = dataframe_for_response.reset_index(drop=True)
          empty_df = pd.concat([empty_df, dataframe_for_response], ignore_index=True)
          #print(empty_df)
          break

      except Exception as e:
        print(f"Attempt {retry_count + 1}: Error processing item {entity1} {relation} {entity2} :: {e}")
        retry_count += 1
        if retry_count >= max_retries:
            print("Maximum retry attempts reached. Please check the error and try again later.")
            break
  triple_validation_list = empty_df.Is_The_Triple_Valid.values.tolist()
    #print(triple_validation_list)
  yes_count=0
  no_count=0

  triple_validation_list = [str(item) for item in triple_validation_list]

  triple_validation_list = [item for item in triple_validation_list if item == 'Yes' or item == 'No']
  print(triple_validation_list, type(triple_validation_list))

  for item in triple_validation_list:
    if item == "Yes":
      yes_count = yes_count + 1
    elif item == "No":
      no_count = no_count + 1


  if yes_count>= no_count:
    triple_val = "Yes"
  else:
    triple_val = "No"

  #print(triple_val)
  # Before joining, convert all items to strings to avoid the TypeError
  short_reasons = empty_df.Reason.values.tolist()
  short_reasons = [clean_text(str(reason)) for reason in short_reasons]  # Convert each item to a string

  short_reasons = "\n".join(short_reasons)

  web_ref = page_rank_df['Urls'][0:3].tolist()
  web_ref = "\n".join(web_ref)
  #print(web_ref)
  #max_page_rank = 0.0
  page_rank_decimal = page_rank_df['Page_Rank_decimal'][0:3].tolist()

  # for values in page_rank_decimal:
  #   if values > max_page_rank:
  #     max_page_rank = values

  #print(max_page_rank)
  new_row_df = pd.DataFrame([{'Subject': entity1, 'Predicate': relation, 'Object': entity2, 'Is_The_Triple_Valid': triple_val,'Sequence of Validation':triple_validation_list, 'Reason': short_reasons, 'Web_Ref': web_ref, 'Highest_Page_Rank': page_rank_decimal}])
  return new_row_df