import PyPDF2
import re
import json

def extract_technical_terms_from_pdf(pdf_path):
    technical_terms = set()
    with open(pdf_path, "rb") as f:
        pdf_reader = PyPDF2.PdfReader(f)
        num_pages = len(pdf_reader.pages)
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            terms = re.findall(
                r'\b(?:Mathematics|Pure Mathematics|Applied Mathematics|Statistics|Actuarial Science|Financial Mathematics|Physics|Astrophysics|Quantum Mechanics|Thermodynamics|Biophysics|Chemistry|Organic Chemistry|Inorganic Chemistry|Analytical Chemistry|Physical Chemistry|Biochemistry|Polymer Chemistry|Earth Sciences|Geology|Geophysics|Meteorology|Oceanography|Environmental Science|Ecology|Conservation Biology|Wildlife Biology|Forestry|Climatology|Astronomy|Astrophysics|Cosmology|Planetary Science|Space Exploration|Computer Science|Artificial Intelligence|Machine Learning|Data Science|Cybersecurity|Software Engineering|Information Technology|Networking|Database Management|Web Development|Human-Computer Interaction|Engineering|Civil Engineering|Mechanical Engineering|Electrical Engineering|Aerospace Engineering|Chemical Engineering|Biomedical Engineering|Materials Science|Medicine|General Medicine|Surgery|Pediatrics|Obstetrics and Gynecology|Psychiatry|Radiology|Nursing|Registered Nursing|Nurse Practitioner|Nurse Anesthetist|Nurse Midwifery|Pharmacology|Clinical Pharmacology|Toxicology|Psychopharmacology|Pharmacy|Psychology|Clinical Psychology|Counseling Psychology|Developmental Psychology|Cognitive Psychology|Social Psychology|Industrial-Organizational Psychology|Sociology|Criminology|Demography|Social Work|Family Studies|Anthropology|Cultural Anthropology|Physical Anthropology|Archaeology|Historical Archaeology|Forensic Anthropology|Political Science|International Relations|Comparative Politics|Public Administration|Economics|Microeconomics|Macroeconomics|Development Economics|Econometrics|Business Administration|Management Information Systems|Operations Management|Entrepreneurship|Marketing|Finance|Accounting|Management|Human Resources|Organizational Behavior|Leadership Studies|Education|Early Childhood Education|Elementary Education|Secondary Education|Special Education|Educational Leadership|Curriculum and Instruction|Adult Education|Linguistics|Phonetics|Syntax|Semantics|Sociolinguistics|Literature|English Literature|World Literature|Comparative Literature|Creative Writing|Poetry|Drama|History|Ancient History|Medieval History|Modern History|Military History|Archaeology|Classical Archaeology|Historical Archaeology|Public History|Philosophy|Ethics|Metaphysics|Epistemology|Logic|Aesthetics|Religious Studies|Comparative Religion|Theology|Eastern Religions|Western Religions|Art History|Renaissance Art|Baroque Art|Modern Art|Contemporary Art|Fine Arts|Painting|Sculpture|Printmaking|Drawing|Photography|Ceramics|Performing Arts|Theater Studies|Acting|Directing|Playwriting|Dance|Ballet|Contemporary Dance|Choreography|Music|Music Theory|Music History|Composition|Music Performance|Ethnomusicology|Film Studies|Film Production|Film Theory|Cinematography|Screenwriting|Animation|Communication Studies|Mass Communication|Journalism|Broadcast Journalism|Print Journalism|Digital Journalism|Media Studies|New Media|Media Production|Media Ethics|Public Relations|Advertising|Corporate Communications|Crisis Communication|Law|Criminal Justice|Forensic Science|Homeland Security|Emergency Management|Social Work|Community Social Work|Clinical Social Work|Macro Social Work|Counseling|Mental Health Counseling|Marriage and Family Therapy|School Counseling|Substance Abuse Counseling|Rehabilitation Counseling|Library and Information Science|Archives Management|Digital Libraries|Information Architecture|Urban Planning|City and Regional Planning|Transportation Planning|Environmental Planning|Architecture|Landscape Architecture|Interior Architecture|Urban Design|Fashion Design|Fashion Merchandising|Textile Design|Costume Design|Sustainable Design|Interior Design|Residential Design|Commercial Design|Hospitality Design|Healthcare Design)\b', text, flags=re.IGNORECASE)
            technical_terms.update(term.lower().replace(" ", "") for term in terms)
    return list(technical_terms)

pdf_path = "mateenshahcv.pdf"
technical_terms = extract_technical_terms_from_pdf(pdf_path)

existing_terms = set()
with open("technical_terms.json", 'r', encoding='utf-8') as f:
    existing_terms = set(json.load(f))

existing_terms.update(technical_terms)
print(existing_terms)

with open("technical_terms.json", 'w', encoding='utf-8') as f:
    json.dump(list(existing_terms), f, indent=4)

print("Technical terms appended to and deduplicated in technical_terms.json")
