# RAG First Project
# Human Nutrition Chatbot - RAG Based Project
## Overview

This project is a Retrieval-Augmented Generation (RAG)-based chatbot built to answer questions related to Human Nutrition.
It combines document understanding, semantic search, and language generation to provide meaningful, accurate answers from a nutrition knowledge base.

## Objective

The main goal of this project is to build an intelligent system that can:

Read and understand nutrition-related PDFs.

Split the content into manageable chunks.

Convert those chunks into embeddings for semantic understanding.

Retrieve the most relevant context when a user asks a question.

Generate clear and informative answers using a language model.

## Project Workflow

The project follows a simple but powerful RAG pipeline:


1) PDF to Text Extraction

The system begins by reading a Human Nutrition PDF and extracting the raw text. This text acts as the foundation of our knowledge base.

2️) Text Cleaning

Unnecessary symbols, line breaks, and extra spaces are removed.
This ensures the content is clean and consistent for further processing.

3️) Document Splitting

The cleaned text is divided into smaller chunks (for example, 800–1000 characters each).
Chunking helps the model handle large documents efficiently and improves retrieval accuracy.

4️) Embedding Generation

Each chunk is transformed into a vector representation — a numerical format that captures the semantic meaning of the text.
These embeddings allow the model to find related information even when different words are used.

5️) Vector Database Creation

All embeddings are stored in a FAISS vector database, enabling fast and efficient similarity searches.
This means that whenever a user asks a question, the system can quickly locate the most relevant sections of the document.

6️) Retriever Setup

A retriever is configured to search through the vector database and return the top-matching text chunks based on similarity.
These chunks serve as the context for answering the user’s question.

7️) Answer Generation

The selected text chunks are passed to a language model (LLM), which generates a natural-language answer by combining retrieved knowledge and reasoning.

8️) Interactive Chat Interface

A simple FastAPI backend connects with a modern web frontend, allowing users to ask questions in real time.
The interface displays both the user’s question and the model’s response dynamically, just like a ChatGPT-style chat window.

## Example Use Case

A user can ask questions like:

1) What is the Vitamin P6?

<img width="1446" height="714" alt="Screenshot 2025-11-05 145514" src="https://github.com/user-attachments/assets/f5c23d56-3ed6-4793-b9c4-be02ad241f1f" />

2) What is the Diabetes?

   <img width="1277" height="738" alt="Screenshot 2025-11-05 145920" src="https://github.com/user-attachments/assets/925fdbd5-4a22-4065-b6ce-c7a7b947248c" />


The chatbot will retrieve the relevant portions of the nutrition document and generate clear, concise answers.

## Key Concepts Used

RAG (Retrieval-Augmented Generation) - combines retrieval and generation for factual accuracy.

Chunks - converting chunk using RecursiveCharacterTextSplitter

Embeddings - convert text into numerical vectors for semantic search.

FAISS - a fast vector database used for storing and searching embeddings.

LLM (Large Language Model) - responsible for generating final, natural-language answers.

FastAPI - backend framework for API and chatbot integration.

HTML/CSS/JavaScript - used to create an interactive, modern front-end chat interface.

## Outcome

This project demonstrates how AI can be used to turn static educational PDFs into interactive, intelligent learning systems.
It can be expanded to other domains like medical studies, finance, or research-based education simply by changing the source PDF.
