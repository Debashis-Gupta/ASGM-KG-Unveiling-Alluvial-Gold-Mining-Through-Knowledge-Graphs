from typing import List, Optional

from langchain.callbacks import get_openai_callback
from langchain_openai import ChatOpenAI

from kor.extraction import create_extraction_chain
from kor.nodes import Object, Text, Number

import pandas as pd
from pydantic import BaseModel, Field, validator
from kor import extract_from_documents, from_pydantic, create_extraction_chain


from langchain.schema import Document
# from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_text_splitters import TokenTextSplitter

from llama_index.core import SimpleDirectoryReader


from logging import exception
from bs4 import BeautifulSoup

from tqdm import tqdm
from io import StringIO
from pathlib import Path
# import pandas as pd
import re
import os
import time
import requests
import warnings
import asyncio
import streamlit as st
import nest_asyncio

async def extract_documents(chain, text):
    with get_openai_callback() as cb:
        document_extraction_results = await extract_from_documents(
            chain, text, max_concurrency=1, use_uid=False, return_exceptions=True
        )
    # You can now use document_extraction_results within or outside this function
    return document_extraction_results

async def SummarizationOSLLM(text_list, llm):
    class Summary(BaseModel):
        Summary: str = Field(
            description="Explain the given list in the most logical and meaningful way. Make it as long as possible.",
        )

    schema, extraction_validator = from_pydantic(
        Summary,
        description="Summarize the following content",
        examples=[
            (
                """Content: amazon region found in mining expansion. amazon region lost millions hectares forest. amazon region is in mercury. amazon region exists in gold mining. amazon region conducted in research. amazon region is in gold production project. amazon region found in mercury. amazon region used in mercury. amazon region is legalizing mining activities. amazon region operate in dissident groups. amazon region is ecological treasure. amazon region source of food. amazon region source of water. amazon region contains biodiversity.""",
                {"Summary": "The Amazon region, an ecological treasure known for its vast biodiversity, is facing significant environmental and social challenges due to the expansion of mining activities. The area has lost millions of hectares of forest, largely attributable to gold mining operations that not only clear vast lands but also utilize harmful substances like mercury in the extraction process. This use of mercury has resulted in widespread contamination, posing severe risks to the regions sources of food and water. Additionally, the Amazon is embroiled in complex socio-political issues, with the legalization of mining activities and the presence of dissident groups further complicating the situation. Despite these challenges, the region remains a vital source of natural resources and is the focus of ongoing research aimed at balancing development with ecological preservation"}
            ),
            # (
            #     """Entity1: 'mercury'  Relation: 'is a' Entity2: 'planet'
            #         Content: Mercury is a chemical element. It has symbol Hg and atomic number 80. It is also known as quicksilver and was formerly named hydrargyrum from the Greek words hydor (water) and argyros (silver).A heavy, silvery d-block element, mercury is the only metallic element that is known to be liquid at standard temperature and pressure.
            #         """,
            #     {"Is_The_Triple_Valid": "No", "Reason": "In the given context mercury is not a planet."}
            # ),
        ],
        
        many=False,
    )

    chain = create_extraction_chain(
        llm,
        schema,
        encoder_or_encoder_class="csv",
        # validator=extraction_validator,
        input_formatter="triple_quotes",
    )

    text = "Content: "
    text += ". ".join([" ".join(sublist) for sublist in text_list]) + "."
    doc = Document(page_content=text)
    split_docs = RecursiveCharacterTextSplitter(chunk_size=50000,).split_documents([doc])

    document_extraction_results = await extract_documents(chain, split_docs)
    print(document_extraction_results[0]['raw'])
    return document_extraction_results[0]['raw']
# async def SummarizationOSLLM(text_list, llm):
#     class Summary(BaseModel):
#         Summary: str = Field(
#             description="Explain the given list in the most logical and meaningful way. Make it as long as possible.",  
#         )
        
    
#     schema, extraction_validator = from_pydantic(
#         Summary,
#         description="Explain the following content in detail.",
#         # examples=[
#         #        (
#         #         """
#         #         amazon region found in mining expansion. amazon region lost millions hectares forest. amazon region is in mercury. amazon region exists in gold mining. amazon region conducted in research. amazon region is in gold production project. amazon region found in mercury. amazon region used in mercury. amazon region is legalizing mining activities. amazon region operate in dissident groups. amazon region is ecological treasure. amazon region source of food. amazon region source of water. amazon region contains biodiversity.
#         #         """,
#         #         {
#         #          """
#         #          The Amazon region, an ecological treasure known for its vast biodiversity, is facing significant environmental and social challenges due to the expansion of mining activities. The area has lost millions of hectares of forest, largely attributable to gold mining operations that not only clear vast lands but also utilize harmful substances like mercury in the extraction process. This use of mercury has resulted in widespread contamination, posing severe risks to the regions sources of food and water. Additionally, the Amazon is embroiled in complex socio-political issues, with the legalization of mining activities and the presence of dissident groups further complicating the situation. Despite these challenges, the region remains a vital source of natural resources and is the focus of ongoing research aimed at balancing development with ecological preservation
#         #          """
#         #         }
#         #         ),
#         #     ],
#         # many=False,
#     )

#     chain = create_extraction_chain(
#         llm,
#         schema,
#         encoder_or_encoder_class="csv",
#         # validator=extraction_validator,
#         input_formatter="triple_quotes",
#     )


#     text = ". ".join([" ".join(sublist) for sublist in text_list]) + "."
#     doc = Document(page_content=text)
#     split_docs = RecursiveCharacterTextSplitter(chunk_size=50000,).split_documents([doc])
#     print(f"Split Content\n :{split_docs}")
#     document_extraction_results = await extract_documents(chain, split_docs)
    
#     return document_extraction_results[0]['raw']

async def make_sum(dataframe):
    llm = ChatOpenAI(
    base_url="https://api.together.xyz/v1",
    model="META-LLAMA/LLAMA-3-70B-CHAT-HF", api_key='bc3592e8f5f99f9a6a63a9bdda8021337b858bf913ee82c32c8ed758d02bff35',
    temperature=0.0,
    )
    # text_list = dataframe.values.tolist()
    if isinstance(dataframe, list):
        text_list = dataframe
    else:
        text_list = dataframe.values.tolist()
    result = await SummarizationOSLLM(text_list, llm)
    return result


def create_summary(dataframe):
  nest_asyncio.apply()

  try:
    loop = asyncio.get_running_loop()
  except RuntimeError:
    loop = asyncio.get_event_loop()

  response = loop.run_until_complete(make_sum(dataframe))
#   response = response.get('text')
#   response = response.split("|")[1]
  return response