"""
RAG Service - Handles document loading, embeddings, and question answering.
Uses singleton pattern to ensure chain is built only once.
"""
import os
import re
import logging
from typing import Optional

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama

from app.core.config import settings

logger = logging.getLogger(__name__)


class RAGService:
    """
    Singleton RAG Service for handling nutrition-related questions.
    Initializes the LangChain pipeline once and reuses it for all queries.
    """
    
    _instance: Optional["RAGService"] = None
    _qa_chain = None
    
    def __new__(cls) -> "RAGService":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self) -> None:
        """Initialize the RAG pipeline."""
        logger.info("Initializing RAG Service...")
        
        # Determine PDF path (handle both old and new structure)
        pdf_path = settings.PDF_PATH
        if not os.path.exists(pdf_path):
            # Fallback to old location
            pdf_path = "HumanNutrition.pdf"
        
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF not found at {pdf_path}")
        
        logger.info(f"Loading PDF from: {pdf_path}")
        
        # Load and process PDF
        loader = PyPDFLoader(pdf_path)
        docs = loader.load()
        logger.info(f"Loaded {len(docs)} pages")
        
        # Clean text
        for doc in docs:
            doc.page_content = self._clean_text(doc.page_content)
        
        # Split into chunks
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP
        )
        chunks = splitter.split_documents(docs)
        logger.info(f"Created {len(chunks)} chunks")
        
        # Create embeddings and vector store
        logger.info(f"Loading embedding model: {settings.EMBEDDING_MODEL}")
        embeddings = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL
        )
        
        logger.info("Building FAISS vector store...")
        db = FAISS.from_documents(chunks, embeddings)
        
        retriever = db.as_retriever(
            search_type="similarity",
            search_kwargs={"k": settings.RETRIEVER_K}
        )
        
        # Initialize LLM
        logger.info(f"Loading LLM: {settings.LLM_MODEL}")
        llm = Ollama(model=settings.LLM_MODEL)
        
        # Build QA chain
        self._qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            return_source_documents=False
        )
        
        logger.info("RAG Service initialized successfully!")
    
    @staticmethod
    def _clean_text(text: str) -> str:
        """Clean and normalize text content."""
        text = text.replace("\n", " ")
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"(\w+)-\s+(\w+)", r"\1\2", text)
        return text.strip()
    
    def ask(self, query: str) -> str:
        """
        Ask a question and get an answer from the RAG pipeline.
        
        Args:
            query: The question to ask
            
        Returns:
            The generated answer
        """
        if self._qa_chain is None:
            raise RuntimeError("RAG Service not initialized")
        
        result = self._qa_chain.invoke({"query": query})
        return result["result"]


# Singleton instance getter
def get_rag_service() -> RAGService:
    """Get the RAG service singleton instance."""
    return RAGService()
