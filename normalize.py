import sys
from pathlib import Path
JPEG_IMAGES = []
JPG_IMAGES = []
PNG_IMAGES = []
SVG_IMAGES = []
MOV_VIDEO = []
AVI_VIDEO = []
MP4_VIDEO = []
MKV_VIDEO = []
DOC_DOKUMENT = []
DOCX_DOKUMENT = []
TXT_DOKUMENT = []
PDF_DOKUMENT = []
XLSX_DOKUMENT = []
PPTX_DOKUMENT = []
MP3_AUDIO = []
OGG_AUDIO = []
WAV_AUDIO = []
AMR_AUDIO = []
MY_OTHER = []
GZ_ARCHIVE = []
TAR_ARCHIVE = []
ZIP_ARCHIVE = []
REGISTER_EXTENSIONS = {
    'JPEG': JPEG_IMAGES,
    'PNG': PNG_IMAGES,
    'JPG': JPG_IMAGES,
    'SVG': SVG_IMAGES,
    'MOV': MOV_VIDEO,
    'AVI': AVI_VIDEO,
    'MP4': MP4_VIDEO,
    'MKV': MKV_VIDEO,
    'MP3': MP3_AUDIO,
    'OGG': OGG_AUDIO,
    'WAV': WAV_AUDIO,
    'AMR': AMR_AUDIO,
    'DOC': DOC_DOKUMENT,
    'DOCX': DOCX_DOKUMENT,
    'TXT': TXT_DOKUMENT,
    'PDF': PDF_DOKUMENT,
    'XLSX': XLSX_DOKUMENT,
    'PPTX': PPTX_DOKUMENT,
    'ZIP': ZIP_ARCHIVES,
    'TAR': TAR_ARCHIVES,
    'GZ': GZ_ARCHIVES
}
FOLDERS = []
EXTENSIONS = set()
UNKNOWN = set()
def get_extension(filename: str) -> str:
    return Path(filename).suffix[1:].upper()

def scan(folder: Path) -> None:
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in ('archives', 'video', 'audio', 'documents', 'images', 'MY_OTHER'):
                FOLDERS.append(item)
                scan(item)
            continue
        ext = get_extension(item.name)
        fullname = folder / item.name
        if not ext:
            MY_OTHER.append(fullname)
        else:
            try:
                container = REGISTER_EXTENSIONS[ext]
                EXTENSIONS.add(ext)
                container.append(fullname)
            except KeyError:
                UNKNOWN.add(ext)
                MY_OTHER.append(fullname)
if __name__ == '__main__':
    folder_for_scan = sys.argv[1]
    print(f'Start in folder {folder_for_scan}')
    scan(Path(folder_for_scan))
    print(f'Images jpeg: {JPEG_IMAGES}')
    print(f'Images jpg: {JPG_IMAGES}')
    print(f'Images svg: {SVG_IMAGES}')
    print(f'Images png: {PNG_IMAGES}')
    print(f'Audio mp3: {MP3_AUDIO}')
    print(f'Audio ogg: {OGG_AUDIO}')
    print(f'Audio wav: {WAV_AUDIO}')
    print(f'Audio amr: {AMR_AUDIO}')
    print(f'Video mov: {MOV_VIDEO}')
    print(f'Video avi: {AVI_VIDEO}')
    print(f'Video mp4: {MP4_VIDEO}')
    print(f'Video mkv: {MKV_VIDEO}')
    print(f'Document doc: {DOC_DOKUMENT}')
    print(f'Document docx: {DOCX_DOKUMENT}')
    print(f'Document txt: {TXT_DOKUMENT}')
    print(f'Document pdf: {PDF_DOKUMENT}')
    print(f'Document xlsx: {XLSX_DOKUMENT}')
    print(f'Document pptx: {PPTX_DOKUMENT}')
    print(f'Archives: {ARCHIVES}')
    print(f'Types of files in folder: {EXTENSIONS}')
    print(f'Unknown files of types: {UNKNOWN}')
    print(FOLDERS[::-1])
