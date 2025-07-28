import os
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def calculate_relevance(text, query):
    if not text or not text.strip(): return 0.0
    try:
        vectorizer = TfidfVectorizer().fit([query, text])
        vectors = vectorizer.transform([query, text])
        return float(cosine_similarity(vectors[0:1], vectors[1:2])[0][0])
    except: return 0.0

def refine_text(text, query, num_sentences=8):
    sentences = [s.strip() for s in text.split('.') if len(s.strip()) > 15]
    if not sentences: return text[:600] + "..." if text else ""
    scores = [calculate_relevance(s, query) for s in sentences]
    top_indices = sorted(np.argsort(scores)[-num_sentences:][::-1])
    return ". ".join([sentences[i] for i in top_indices]) + "."

def process_document_collection(challenge_input, get_sections_func, pdfs_dir):
    persona = challenge_input['persona']['role']
    job = challenge_input['job_to_be_done']['task']
    query = f"{persona} {job} activities nightlife entertainment beach coast budget friends fun party"
    
    all_sections = []
    for doc in challenge_input['documents']:
        pdf_path = os.path.join(pdfs_dir, doc.get('filename'))
        if os.path.exists(pdf_path):
            for section in get_sections_func(pdf_path):
                section['document'] = doc.get('filename')
                all_sections.append(section)
                
    for section in all_sections:
        section['score'] = calculate_relevance(f"{section['section_title']} {section['text'][:500]}", query)
    all_sections.sort(key=lambda x: x['score'], reverse=True)
    
    return {
        "metadata": {
            "input_documents": [d['filename'] for d in challenge_input['documents']],
            "persona": persona, "job_to_be_done": job, "processing_timestamp": datetime.now().isoformat()
        },
        "extracted_sections": [{"document": s['document'], "section_title": s['section_title'], "importance_rank": i + 1, "page_number": s['page_number']} for i, s in enumerate(all_sections[:5])],
        "subsection_analysis": [{"document": s['document'], "refined_text": refine_text(s['text'], query), "page_number": s['page_number']} for s in all_sections[:5] if s.get('text')]
    }