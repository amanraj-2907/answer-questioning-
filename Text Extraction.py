import fitz  

def extract_text_debug(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""

    for page_num in range(len(doc)):
        page = doc[page_num]
        print(f"\n🔹 Page {page_num + 1}")

      
        text = page.get_text("text")  
        lines = text.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            print(f"  📝 Line {line_num}: {line}")
            words = line.split()
            for word in words:
                print(f"     🔸 Word: {word}")
            
            full_text += line + "\n"

    return full_text


pdf_path = "C:/Users/Asus/OneDrive/ドキュメント/India is a South Asian country with its capital in New Delhi.pdf"
extract_text_debug(pdf_path)
