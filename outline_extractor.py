import re
from pdf_parser import extract_text_and_properties_from_pdf, get_document_title

# detect_headings is identical to part_1A's version
def detect_headings(text_blocks):
    if not text_blocks: return []
    font_sizes = [b['font_size'] for b in text_blocks if b['font_size']]
    if not font_sizes: return []
    most_common_size = max(set(font_sizes), key=font_sizes.count)
    heading_styles = sorted({s for s in font_sizes if s > most_common_size}, reverse=True)
    level_map = {size: f"H{i+1}" for i, size in enumerate(heading_styles)}
    headings = []
    for block in text_blocks:
        is_heading, level = False, None
        num_match = re.match(r'^((\d+(\.\d+)*)|(Appendix\s+[A-Z]))\s+', block['text'])
        if num_match:
            is_heading, level_text = True, num_match.group(1)
            level = 'H2' if 'Appendix' in level_text else f"H{level_text.count('.') + 1}"
        elif block['font_size'] in level_map and block['is_bold']:
            is_heading, level = True, level_map[block['font_size']]
        if is_heading:
            headings.append({"level": level, "text": block['text'], "page": block['page'] + 1, "_page_num": block['page'], "y0": block['y0']})
    return headings

def get_document_sections_from_outline(pdf_path):
    text_blocks = extract_text_and_properties_from_pdf(pdf_path)
    title = get_document_title(text_blocks)
    headings = detect_headings(text_blocks)
    headings.sort(key=lambda h: (h['_page_num'], -h['y0']))
    if not headings:
        return [{"section_title": title, "text": " ".join(b['text'] for b in text_blocks), "page_number": 1}]
    sections = []
    for i, heading in enumerate(headings):
        start_page, start_y = heading['_page_num'], heading['y0']
        end_page, end_y = (float('inf'), -1)
        if i + 1 < len(headings): end_page, end_y = headings[i+1]['_page_num'], headings[i+1]['y0']
        section_text = " ".join([b['text'] for b in text_blocks if ((b['page'] == start_page and b['y0'] < start_y) or b['page'] > start_page) and ((b['page'] == end_page and b['y0'] > end_y) or b['page'] < end_page)])
        sections.append({"section_title": heading['text'], "text": section_text, "page_number": heading['page']})
    return sections