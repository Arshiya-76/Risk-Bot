# reformatter.py

import re

def _find_section(text: str, keywords: list, next_keywords: list) -> str:
    start_pattern = r"(?i)\b(" + "|".join(keywords) + r")\b"
    end_pattern = r"(?i)\b(" + "|".join(next_keywords) + r")\b"
    start_match = re.search(start_pattern, text)
    if not start_match:
        return ""
    end_match = re.search(end_pattern, text[start_match.end():])
    if end_match:
        return text[start_match.start() : start_match.end() + end_match.start()].strip()
    else:
        return text[start_match.start():].strip()

def reformat_contract_as_template(text: str, template_type: str, language: str = 'en'):
    body_clauses = re.findall(r"(\n\s*\d+\..+)", text, re.DOTALL)
    body_text = "".join(body_clauses).strip() if body_clauses else "[COULD NOT AUTOMATICALLY EXTRACT NUMBERED CLAUSES]"
    all_headings = ["term", "effective date", "confidentiality", "governing law", "jurisdiction", "dispute resolution", "arbitration"]
    reformatted_text = f"""
## {template_type.upper()}
**This Agreement** is made and entered into on this ______ day of __________, 20__
**BY AND BETWEEN:**
{_find_section(text, ["parties", "between"], all_headings) or "[PARTIES SECTION NOT FOUND - PLEASE INSERT MANUALLY]"}
**WHEREAS:**
(A) [Insert Recital A]
(B) [Insert Recital B]
**NOW, THEREFORE, IN CONSIDERATION OF THE MUTUAL COVENANTS CONTAINED HEREIN, THE PARTIES AGREE AS FOLLOWS:**
---
### NUMBERED CLAUSES
---
{body_text}
---
### STANDARD CLAUSES
---
**GOVERNING LAW AND JURISDICTION**
{_find_section(text, ["governing law", "jurisdiction"], ["dispute resolution", "arbitration"]) or "This Agreement shall be governed by and construed in accordance with the laws of India. The Parties agree to submit to the exclusive jurisdiction of the courts in [Specify City, e.g., Mumbai]."}
**DISPUTE RESOLUTION**
{_find_section(text, ["dispute resolution", "arbitration"], []) or "Any dispute arising out of or in connection with this Agreement shall be referred to and finally resolved by arbitration in accordance with the Arbitration and Conciliation Act, 1996. The seat of the arbitration shall be [Specify City, e.g., New Delhi]."}
**IN WITNESS WHEREOF,** the Parties have executed this Agreement as of the date first above written.
**For [PARTY 1 NAME]:**
_________________________
Name:
Title:
**For [PARTY 2 NAME]:**
_________________________
Name:
Title:
"""
    return reformatted_text.strip()