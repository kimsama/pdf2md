import pdfplumber
import pytesseract
from PIL import Image
import pandas as pd
from markdownify import markdownify as md
import os
import argparse
<<<<<<< Updated upstream
=======
import io
import fitz  # PyMuPDF
>>>>>>> Stashed changes

# Tesseract 경로 설정 (시스템에 맞게 수정)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def ocr_image(image, lang='kor'):
    """OCR로 이미지에서 텍스트 추출"""
    return pytesseract.image_to_string(image, lang=lang)

<<<<<<< Updated upstream
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
=======
def save_image(image_obj, output_path):
    """이미지 객체를 파일로 저장하고 포맷 검증"""
    try:
        # 이미지 데이터 추출
        image_data = image_obj["stream"].get_data()
        
        # 이미지 포맷 확인
        fmt = image_obj.get("format", "").lower()
        if fmt not in ["jpg", "jpeg", "png"]:
            fmt = "png"  # 기본값으로 PNG 사용
        
        # PIL을 사용하여 이미지 데이터 검증 및 변환
        try:
            img = Image.open(io.BytesIO(image_data))
            # 이미지 모드가 RGBA가 아닌 경우 변환
            if img.mode not in ['RGB', 'RGBA']:
                img = img.convert('RGB')
            img.save(output_path, format=fmt)
            print(f"이미지 저장 성공: {output_path}")
            return True
        except Exception as e:
            print(f"이미지 변환 중 오류: {e}")
            
            # 직접 바이너리 데이터 저장 시도 (��체 방법)
            try:
                with open(output_path, "wb") as f:
                    f.write(image_data)
                return True
            except Exception as e2:
                print(f"직접 저장 시도 중 오류: {e2}")
                return False
                
    except Exception as e:
        print(f"이미지 처리 중 오류 발생: {e}")
        return False

def extract_images_from_pdf(pdf_path, image_dir):
    """PyMuPDF를 사용하여 PDF에서 이미지 추출"""
    image_paths = []
    
    # PDF 문서 열기
    doc = fitz.open(pdf_path)
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        image_list = page.get_images()
        
        for img_index, img in enumerate(image_list):
            # 이미지 데이터 가져오기
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_data = base_image["image"]
            
            # 이미지 포맷 확인
            image_format = base_image["ext"]
            image_filename = f"image_page{page_num + 1}_{img_index + 1}.{image_format}"
            image_path = os.path.join(image_dir, image_filename)
            
            try:
                # 이미지 데이터를 PIL Image로 변환
                image = Image.open(io.BytesIO(image_data))
                image.save(image_path)
                print(f"이미지 저장 성공: {image_path}")
                image_paths.append((page_num + 1, image_path))
            except Exception as e:
                print(f"이미지 저장 실패 (Page {page_num + 1}, Image {img_index + 1}): {e}")
    
    doc.close()
    return image_paths

def pdf_to_markdown(pdf_path, output_path="output.md", ocr_lang='kor'):
    image_dir = "extracted_images"
    os.makedirs(image_dir, exist_ok=True)
    
    # PyMuPDF로 이미지 추출
    image_paths = extract_images_from_pdf(pdf_path, image_dir)
    
    # pdfplumber로 텍스트 추출
    with pdfplumber.open(pdf_path) as pdf:
        markdown_content = ""
        current_page = 1
        
        for page_num, page in enumerate(pdf.pages):
            markdown_content += f"\n\n# Page {page_num + 1}\n"
            
            # 텍스트 추출 (기존 코드와 동일)
            text = page.extract_text()
            if text:
                markdown_content += text + "\n"
            
            # 현재 페이지의 이미지 삽입
            page_images = [img for img in image_paths if img[0] == page_num + 1]
            for _, img_path in page_images:
                rel_path = os.path.relpath(img_path, os.path.dirname(output_path))
                markdown_content += f"\n![Image]({rel_path})\n"

    # 마크다운 파일 저장 (기존 코드와 동일)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)
    
    return output_path
>>>>>>> Stashed changes

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