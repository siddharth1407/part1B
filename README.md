
# Adobe India Hackathon 2025 - Connecting the Dots

## Project Title: [Your Project Name Here, e.g., Smart PDF Outline & Insights]

### Round 1B: Persona-Driven Document Intelligence
[cite_start]This part of the solution acts as an intelligent document analyst, extracting and prioritizing relevant sections from a collection of documents based on a specific persona and a given "job-to-be-done." [cite: 109]

Approach for Round 1B:
1.  Structured Document Representation: We leverage the output of Round 1A (or integrate its core logic) to create a structured representation of each PDF, identifying sections and sub-sections based on detected headings. This allows us to work with meaningful chunks of text.
2.  Semantic Relevance Scoring:
    * The persona (role, expertise) and job_to_be_done (concrete task) are combined into a query text.
    * For each section and sub-section in the document collection, we calculate a semantic similarity score against this combined query.
    * Methodology:
        * [cite_start](Option 1: Sentence Embeddings - Preferred if within 1GB model size constraint): We intend to use a pre-trained, compact sentence embedding model (e.g., from the sentence-transformers library, specifically a small model like all-MiniLM-L6-v2 if it fits the $\le 1$GB limit [cite: 152]). This model would encode the query and each document section into vector representations. Cosine similarity between these vectors would then determine the relevance. [cite_start]The model files will be bundled within the Docker image to ensure offline operation[cite: 155].
        * (Option 2: TF-IDF Cosine Similarity - Fallback): If an embedding model cannot be used due to size constraints or performance, we will fall back to TF-IDF vectorization and cosine similarity. While less semantically rich, it is highly efficient and robust for keyword overlap.
3.  [cite_start]Section Ranking: Sections are then ranked based on their calculated relevance scores, with the most relevant sections receiving a higher importance rank[cite: 144].
4.  [cite_start]Sub-Section Refinement (Extractive Summarization): For relevant sections, we identify and extract key sentences from their sub-sections to create a "refined text"[cite: 148]. This is done by calculating the similarity of individual sentences within the sub-section to the persona and job-to-be-done, and then selecting the top N most similar sentences.

Libraries Used (Round 1B):
* scikit-learn for TF-IDF vectorization and cosine similarity.
* numpy for numerical operations.
* (Potentially) sentence-transformers and torch (or tensorflow) if using sentence embedding models.

### Docker Build and Run Instructions

Docker Requirements:
* [cite_start]The Dockerfile is compatible with linux/amd64 architecture. [cite: 56]
* [cite_start]No GPU dependencies are used. [cite: 58]
* [cite_start]All dependencies are installed within the container. [cite: 86]
* [cite_start]The solution works completely offline, with no internet access or API calls during execution. 
* [cite_start]Model size (if used) is $\le 200$MB for Round 1A and $\le 1$GB for Round 1B. 
* [cite_start]Runtime is on a system with 8 CPUs and 16 GB RAM configurations. [cite: 79, 80]

How to Build the Docker Image:
Navigate to the root directory of this project (where Dockerfile is located) and run:
```bash
docker build --platform linux/amd64 -t mysolutionname:somerandomidentifier .

docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none mysolutionname:somerandomidentifier 
