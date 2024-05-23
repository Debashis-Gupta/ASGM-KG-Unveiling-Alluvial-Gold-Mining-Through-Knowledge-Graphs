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


def extract_text_from_pdf(pdf_path):
    # Open the PDF file in binary read mode
    with open(f"data/pdf/{pdf_path}", 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            # Extract text from each page and add to the text variable
            page_text = page.extract_text()
            if page_text:  # Checking if text was extracted successfully
                text += page_text
        return text

def split_document_into_chunks(document, name,max_length=3000):
    document_list = []
    document_length = len(document)
    print(f"{name} Document Length is : {document_length}")
    print(f"Chunk will be: {document_length/max_length}")
    for start in range(0, document_length, max_length):
        end = start + max_length
        # Ensure the end does not exceed the document length
        document_chunk = document[start:end]
        document_list.append(document_chunk)

    return document_list

def convert_to_df_csv(text_response,name,output_filename):
  original_text = text_response
  print(f"Original_Text: {original_text}")
  pipe_position = original_text.index("|")
  substring = original_text[pipe_position:]
  text = substring
  # Split the text into lines and remove leading/trailing whitespaces
  lines = [line.strip() for line in text.split("\n") if line.strip()]

  # Remove the line with "---"
  lines = [line for line in lines if not set(line) == {"-", "|", " "}]
  lines = [line for line in lines if "---" not in line]

  # Initialize empty lists to hold the data
  head_entity = []
  relation = []
  tail_entity = []

  # Iterate over the lines
  for line in lines[1:]:  # Skip the header
      # Split the line at the pipe characters and strip leading/trailing whitespaces
      parts = [part.strip() for part in line.split("|") if part.strip()]

      if len(parts) == 3:
          # Append the data to the respective lists
          head_entity.append(parts[0])
          relation.append(parts[1])
          tail_entity.append(parts[2])

  # Create a DataFrame from the lists
  df = pd.DataFrame({
      'Subject': head_entity,
      'Predicate': relation,
      'Object': tail_entity
  })
  if output_filename is None:
     print("No output filename is provided. Output will be created to default directory 'Output'.")
     output_filename='Output'
     os.makedirs(output_filename,exist_ok=True)
  print(f"{name} starts to convert into csv file ..")
  df.to_csv(f'{output_filename}/{name}.csv')

async def test_ask(prompt,cookies_path) -> None:
   bot = None
   try:
      mode = "Copilot" 
      cookies: list[dict] = json.loads(open(
            str(Path(str(Path.cwd()) + f"/{cookies_path}")), encoding="utf-8").read())
      bot = await Chatbot.create(cookies=cookies, mode=mode)
      response = await bot.ask(
         prompt=prompt,
         conversation_style=ConversationStyle.precise,
         simplify_response=True
      )
      return response

   except Exception as error:
      raise error
   finally:
      if bot is not None:
         await bot.close()


def Ask_Copilot(prompt,cookies_path):
  nest_asyncio.apply()

  try:
    loop = asyncio.get_running_loop()
  except RuntimeError:
    loop = asyncio.get_event_loop()

  response = loop.run_until_complete(test_ask(prompt,cookies_path))
  response = response.get('text')
  return response

def RDF_extraction(pdf_path,cookies_path=None,output_filename=None):
  name = pdf_path.split('.')[0]
  if cookies_path is None:
     raise ValueError("Please specify cookies path.")
  pdf_directory = pdf_path
  extracted_text = extract_text_from_pdf(pdf_directory)
  extracted_text = extracted_text.lower()
  #print(len(extracted_text))
  document_chunk = split_document_into_chunks(extracted_text,name)
  for id, text in enumerate(document_chunk):
    current_name = f"{name}_{id}"

    prompt = f"""
      You will now act as an expert in extracting Subject Predicate Object. Extrapolate all the available relationships from the input text named Text. You must follow the following instructions:
      1.  Every Subject must be a "noun".
      2.  Every "pronoun" (it, this, that,these, those, his,her) strictly be replaced with "noun" that is referred in the context by the "pronoun".
      3.  Every Subject and Object can be maximum four words and Predicate strictly should be not more than three words.
      4.  The Entities must be in order and the order should be maintained as the text is written.
      5.  The order of the Predicate should follow the order of the text.
      6.  The Predicate should be a "verb".
      7.  Try to extract the Subject Predicate Object in such a way that is true in your sense. Don't add any of your text in extraction.
      Input:    Text:{text}

      Output: RDF Table. The headers of the table will be as following
      |Subject|Predicate|Object|
      """
    text_response = Ask_Copilot(prompt,cookies_path)
    convert_to_df_csv(text_response,current_name,output_filename)

