from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar

def extract_text_and_properties_from_pdf(pdf_path):
    """
    Extracts text blocks with their properties (font size, bold, page number, position)
    from a PDF document.
    """
    text_blocks_with_properties = []
    
    for page_num, page_layout in enumerate(extract_pages(pdf_path)):
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                for text_line in element:
                    line_text = text_line.get_text().strip()
                    if not line_text:
                        continue

                    font_size = None
                    is_bold = False
                    if hasattr(text_line, '_objs') and text_line._objs and isinstance(text_line._objs[0], LTChar):
                        font_size = round(text_line._objs[0].size, 2)
                        if "bold" in text_line._objs[0].fontname.lower():
                            is_bold = True
                    
                    text_blocks_with_properties.append({
                        "text": line_text,
                        "page": page_num,
                        "x0": round(text_line.x0, 2),
                        "y0": round(text_line.y0, 2),
                        "font_size": font_size,
                        "is_bold": is_bold,
                    })
    
    text_blocks_with_properties.sort(key=lambda x: (x['page'], -x['y0']))
    return text_blocks_with_properties

def get_document_title(text_blocks):
    """
    Attempts to identify the document title.
    """
    if not text_blocks:
        return ""

    first_page_blocks = sorted(
        [b for b in text_blocks if b['page'] == 0], 
        key=lambda x: (x.get('font_size') or 0, x.get('y0')), 
        reverse=True
    )
    
    return first_page_blocks[0]['text'].strip() if first_page_blocks else ""