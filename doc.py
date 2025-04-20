# Run once to extract and save Tata Code Of Conduct
from document_handler import extract_text_from_pdf, save_extracted_text
text = extract_text_from_pdf("C:/Users/aryah/Documents/Git/enterprise_chatbot/Tata Code Of Conduct.pdf")
save_extracted_text(text)
