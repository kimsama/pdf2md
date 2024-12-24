# PDF to Markdown Converter with OCR Support

## 개요

이 도구는 PDF 파일을 마크다운 형식으로 변환하는 파이썬 스크립트입니다. 주요 기능:

- OCR을 통한 한글 텍스트 인식
- PDF 내 이미지 추출 및 저장
- 테이블 변환 지원
- 명령줄 인터페이스

## 설치

1. 필수 패키지 설치:
```bash
pip install -r requirements.txt
```

2. PyMuPDF 설치:
```bash
pip install PyMuPDF
```

3. Tesseract OCR 설치:
   - Windows: [Tesseract-OCR 다운로드](https://github.com/UB-Mannheim/tesseract/wiki)
   - Linux: `sudo apt install tesseract-ocr`

4. Korean 언어 패키지 설치:
   - Windows: Tesseract 설치 시 Korean 선택
   - Linux: `sudo apt install tesseract-ocr-kor`

### 이미지 처리

PDF 내 이미지 추출 및 처리를 위해 PyMuPDF (fitz) 라이브러리를 사용합니다:

- 이미지 자동 감지 및 적절한 확장자로 저장
- 원본 이미지 데이터 직접 추출로 품질 유지
- 페이지별 이미지 추출 및 마크다운 링크 생성
- 상대 경로를 사용한 이미지 참조
- 안정적인 이미지 저장 방식 구현
- 텍스트와 이미지의 페이지별 정렬 유지

## 사용방법

### 기본 사용
```bash
python app.py 입력파일.pdf
```

### 출력 파일명 지정
```bash
python app.py 입력파일.pdf -o 출력파일.md
```

### OCR 언어 변경
```bash
python app.py 입력파일.pdf -l eng
```

### 옵션
- `-o`, `--output`: 출력 파일 경로 (기본값: output.md)
- `-l`, `--lang`: OCR 언어 설정 (기본값: kor)
