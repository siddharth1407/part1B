
# Adobe India Hackathon 2025 - Connecting the Dots

## Project Title: [Your Project Name Here, e.g., Smart PDF Outline & Insights]

### Round 1A: Understand Your Document
This part of the solution extracts a structured outline (Title, H1, H2, H3 headings with page numbers) from PDF documents.

Approach for Round 1A:
[cite_start]Our approach for heading detection combines several heuristics to ensure robustness, as simply relying on font sizes can be insufficient.
1.  PDF Parsing: We use pdfminer.six to parse PDF files. This library allows us to extract text content along with detailed layout information, including font size, bold status, and precise (x, y) coordinates for each text block. This is crucial for understanding the visual hierarchy of the document.
2.  Feature Extraction: For each text block, we extract:
    * font_size: The size of the font used.
    * is_bold: Whether the text is rendered in bold.
    * y_position: The vertical position on the page, helping to determine vertical spacing between blocks.
    * x_position: The horizontal position, for alignment checks.
    * line_height: The height of the text line, useful for calculating vertical gaps.
3.  Heuristic-Based Heading Classification:
    * We first analyze the distribution of font sizes across the entire document to identify the most prominent sizes, which are strong candidates for H1, H2, and H3.
    * Text blocks are identified as potential headings if they are bold AND have one of the inferred heading font sizes.
    * Further checks include:
        * Vertical Spacing: Headings typically have larger vertical gaps above them compared to regular body text.
        * Positional Cues: Headings often appear at the beginning of a page or column, or are distinctly indented/aligned.
        * Title Detection: The document title is inferred as the largest, most prominent text block appearing near the top of the first page.
4.  Outline Construction: Once headings are identified and classified (H1, H2, H3), they are structured hierarchically based on their level and appearance order.

Libraries Used (Round 1A):
* pdfminer.six for PDF parsing and layout analysis.
* Standard Python libraries for text processing and JSON output.

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
docker build --platform linux/amd64 -t mysolutionname:somerandomidentifier . [cite: 64, 65]

docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none mysolutionname:somerandomidentifier [cite: 67]