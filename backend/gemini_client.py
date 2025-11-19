import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")

genai.configure(api_key=GOOGLE_API_KEY)

class GeminiClient:
    def __init__(self):
        self.model_name = "gemini-1.5-flash" # Or gemini-1.5-pro
        self.model = genai.GenerativeModel(self.model_name)

    def upload_file(self, file_path: str, mime_type: str = None):
        """Uploads a file to Gemini File API."""
        print(f"Uploading file: {file_path}")
        file = genai.upload_file(file_path, mime_type=mime_type)
        print(f"Uploaded file: {file.name}")
        return file

    def list_files(self):
        """Lists files uploaded to Gemini."""
        return list(genai.list_files())

    def delete_file(self, file_name: str):
        """Deletes a file from Gemini."""
        genai.delete_file(file_name)

    def chat_with_files(self, query: str, file_uris: list[str]):
        """
        Sends a query to Gemini using the uploaded files as context.
        Note: In a real production scenario with many files, you would use 
        File Search (Vector Store) instead of passing all file URIs directly 
        if the context window is exceeded. For this MVP with File Search API,
        we will assume we are using the 'tools' approach or direct context 
        depending on the specific Gemini API version capabilities for 'File Search'.
        
        For the 'File Search' specific feature (Knowledge Retrieval), we need to 
        create a corpus/cache.
        """
        # This is a simplified implementation using direct file context for now.
        # For true "File Search" with large scale, we'd use the retrieval tools.
        
        # Construct the prompt with file context
        # In 1.5 Flash/Pro, we can pass file objects directly to generate_content
        
        # Fetch file objects (simplified, assuming we have the names/URIs)
        # In SDK, we might need to pass the file object returned from upload, 
        # or retrieve it by name.
        
        # For this implementation, let's assume we are using the standard generate_content
        # with the file objects.
        
        # NOTE: To properly use "File Search" (Semantic Retrieval), we should use
        # the `tools=[{'google_search_retrieval': ...}]` or similar if available,
        # but for *uploaded user files*, we typically pass them in the history or request.
        
        # Let's try the direct approach first which is robust for < 1M tokens.
        
        # We need to get the file objects first.
        files = []
        for uri in file_uris:
             # We can't easily get the file object back from just URI in the standard SDK 
             # without re-fetching or keeping track. 
             # Let's assume the caller passes the file names (files/...)
             try:
                 file = genai.get_file(uri)
                 files.append(file)
             except Exception as e:
                 print(f"Error getting file {uri}: {e}")

        response = self.model.generate_content(
            [query] + files
        )
        return response.text

gemini_client = GeminiClient()
