import pdfplumber
import pytesseract
from PIL import Image
import pandas as pd
from markdownify import markdownify as md
import os
import argparse

# Tesseract 경로 설정 (시스템에 맞게 수정)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def ocr_image(image, lang='kor'):
    """OCR로 이미지에서 텍스트 추출"""
    return pytesseract.image_to_string(image, lang=lang)

def pdf_to_markdown(pdf_path, output_path="output.md", ocr_lang='kor'):
    with pdfplumber.open(pdf_path) as pdf:
        markdown_content = ""
        for page_num, page in enumerate(pdf.pages):
            markdown_content += f"\n\n# Page {page_num + 1}\n"
            
            # 텍스트 추출 (OCR 백업)
            text = page.extract_text()
            if not text:
                # 페이지를 이미지로 변환하여 OCR 처리
                with page.to_image(resolution=300) as img:
                    pil_image = img.original
                    text = ocr_image(pil_image, lang=ocr_lang)
            
            markdown_content += f"\n{text}\n"
            
            # 이미지 추출
            images = page.images
            for img_index, img in enumerate(images):
                # 이미지 저장
                image_path = f"image_page{page_num + 1}_{img_index + 1}.png"
                with open(image_path, "wb") as f:
                    f.write(page.images[img_index]["stream"].get_rawdata())
                # 마크다운 이미지 태그 추가
                markdown_content += f"![Image {img_index + 1}](./{image_path})\n"
            
            # 테이블 추출
            tables = page.extract_tables()
            for table_index, table in enumerate(tables):
                df = pd.DataFrame(table[1:], columns=table[0])  # 첫 번째 행은 헤더로 처리
                markdown_content += f"\n\nTable {table_index + 1}:\n\n"
                markdown_content += df.to_markdown(index=False)
        
        # 마크다운 파일로 저장
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)

def main():
    # 명령줄 인자 파서 설정
    parser = argparse.ArgumentParser(description="Convert a PDF file to a Markdown file.")
    parser.add_argument("pdf_path", help="Path to the input PDF file")
    parser.add_argument("-o", "--output", help="Path to the output Markdown file (default: output.md)", default="output.md")
    parser.add_argument("-l", "--lang", help="OCR language for text extraction (default: kor)", default="kor")
    
    args = parser.parse_args()
    
    # PDF를 마크다운으로 변환
    pdf_to_markdown(args.pdf_path, output_path=args.output, ocr_lang=args.lang)

if __name__ == "__main__":
    main()