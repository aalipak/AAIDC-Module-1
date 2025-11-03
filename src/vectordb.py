import os
import chromadb
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer


class VectorDB:
    """
    A simple vector database wrapper using ChromaDB with HuggingFace embeddings.
    """

    def __init__(self, collection_name: str = None, embedding_model: str = None):
        """
        Initialize the vector database.

        Args:
            collection_name: Name of the ChromaDB collection
            embedding_model: HuggingFace model name for embeddings
        """
        self.collection_name = collection_name or os.getenv(
            "CHROMA_COLLECTION_NAME", "rag_documents"
        )
        self.embedding_model_name = embedding_model or os.getenv(
            "EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
        )

        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(path="./chroma_db")

        # Load embedding model
        print(f"Loading embedding model: {self.embedding_model_name}")
        self.embedding_model = SentenceTransformer(self.embedding_model_name)

        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"description": "RAG document collection"},
        )

        print(f"Vector database initialized with collection: {self.collection_name}")

    def chunk_text(self, text: str, chunk_size: int = 500) -> List[str]:
        """
        Split text into smaller chunks using LangChain's RecursiveCharacterTextSplitter.
        This method respects sentence boundaries and maintains context better than simple splitting.

        Args:
            text: Input text to chunk
            chunk_size: Approximate number of characters per chunk

        Returns:
            List of text chunks
        """
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        
        # Initialize the text splitter with appropriate parameters
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=50,  # Overlap between chunks to maintain context
            length_function=len,
            separators=["\n\n", "\n", ". ", ", ", " ", ""]  # Order from most to least preferred split points
        )
        
        try:
            # Split the text into chunks
            chunks = text_splitter.split_text(text)
            print(f"Text split into {len(chunks)} chunks")
            return chunks
        except Exception as e:
            print(f"Error during text chunking: {str(e)}")
            # Return single chunk if splitting fails
            return [text]

    def add_documents(self, documents: List[Dict[str, Any]]) -> None:
        """
        Add documents to the vector database.

        Args:
            documents: List of documents, each with 'content' and 'metadata' keys
        """
        print(f"Processing {len(documents)} documents...")
        
        all_chunks = []
        all_metadatas = []
        all_ids = []
        
        # Process each document
        for doc_idx, doc in enumerate(documents):
            try:
                # Extract content and metadata
                content = doc.get('content', '')
                metadata = doc.get('metadata', {})
                
                if not content:
                    print(f"Warning: Empty content in document {doc_idx}")
                    continue
                
                # Split document into chunks
                chunks = self.chunk_text(content)
                print(f"Document {doc_idx}: Split into {len(chunks)} chunks")
                
                # Process each chunk
                for chunk_idx, chunk in enumerate(chunks):
                    # Create unique ID for the chunk
                    chunk_id = f"doc_{doc_idx}_chunk_{chunk_idx}"
                    
                    # Add chunk-specific metadata
                    chunk_metadata = metadata.copy()
                    chunk_metadata.update({
                        'chunk_id': chunk_id,
                        'chunk_index': chunk_idx,
                        'total_chunks': len(chunks),
                        'document_id': doc_idx
                    })
                    
                    # Add to lists for batch processing
                    all_chunks.append(chunk)
                    all_metadatas.append(chunk_metadata)
                    all_ids.append(chunk_id)
                    
            except Exception as e:
                print(f"Error processing document {doc_idx}: {str(e)}")
                continue
        
        if not all_chunks:
            print("No valid chunks to add to the database")
            return
            
        try:
            # Generate embeddings for all chunks in one batch
            print("Generating embeddings for all chunks...")
            embeddings = self.embedding_model.encode(all_chunks)
            
            # Add everything to ChromaDB
            print("Adding chunks to vector database...")
            self.collection.add(
                embeddings=embeddings.tolist(),
                documents=all_chunks,
                metadatas=all_metadatas,
                ids=all_ids
            )
            
            print(f"Successfully added {len(all_chunks)} chunks to vector database")
            
        except Exception as e:
            print(f"Error adding chunks to database: {str(e)}")

    def search(self, query: str, n_results: int = 5) -> Dict[str, Any]:
        """
        Search for similar documents in the vector database.

        Args:
            query: Search query
            n_results: Number of results to return

        Returns:
            Dictionary containing search results with keys: 'documents', 'metadatas', 'distances', 'ids'
        """
        try:
            # Check if collection is empty
            if self.collection.count() == 0:
                print("Warning: Vector database is empty")
                return {
                    "documents": [],
                    "metadatas": [],
                    "distances": [],
                    "ids": []
                }

            # Generate embedding for the query
            print("Generating query embedding...")
            query_embedding = self.embedding_model.encode([query])[0]

            # Perform the similarity search
            print(f"Searching for top {n_results} relevant chunks...")
            results = self.collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=n_results,
                include=["documents", "metadatas", "distances"]
            )

            # Extract and format results
            documents = results.get("documents", [[]])[0]  # Get first query's results
            metadatas = results.get("metadatas", [[]])[0]
            distances = results.get("distances", [[]])[0]
            ids = results.get("ids", [[]])[0]

            # Sort results by distance (similarity score)
            sorted_results = sorted(
                zip(documents, metadatas, distances, ids),
                key=lambda x: x[2]  # Sort by distance
            )

            # Unzip sorted results
            sorted_docs, sorted_metas, sorted_dists, sorted_ids = zip(*sorted_results) if sorted_results else ([], [], [], [])

            print(f"Found {len(sorted_docs)} relevant chunks")
            
            return {
                "documents": list(sorted_docs),
                "metadatas": list(sorted_metas),
                "distances": list(sorted_dists),
                "ids": list(sorted_ids)
            }

        except Exception as e:
            print(f"Error during similarity search: {str(e)}")
            return {
                "documents": [],
                "metadatas": [],
                "distances": [],
                "ids": []
            }
