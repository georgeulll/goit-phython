from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import time
import shutil


EXTENSIONS_DICT = {
    'images': ('.jpeg', '.png', '.jpg', '.svg', '.dng', '.bmp'),
    'video': ('.avi', '.mp4', '.mov', '.mkv'),
    'documents': ('.doc', '.docx', '.txt', '.pdf', '.xls', '.xlsx', '.pptx', '.djvu', '.rtf', '.pub'),
    'audio': ('.mp3', '.ogg', '.wav', '.amr'),
    'archives': ('.zip', '.gz', '.tar'),
    'photoshop': ('.xmp', '.nef'),
    'books': ('.epub', '.fb2')
}

CYRILLIC_SYMBOLS = "àáâãäå¸æçèéêëìíîïðñòóôõö÷øùúûüýþÿº³¿´"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
trans = {}


def sort_files(path):
    '''Launches file sorting.'''
    global main_folder

    current_folder = Path(path)

    if (not current_folder.exists()) or (not current_folder.is_dir()):
        return f'Wrong path. Try again.'

    main_folder = current_folder

    to_translate()
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.submit(sort, current_folder)

    return f"Well done!"


def sort(iter_dirs: Path):
    '''Iterates files and folders.'''
    for file in iter_dirs.iterdir():

        if file.name not in EXTENSIONS_DICT.keys() and file.is_dir():
            sort(file)

        elif file.is_file():
            change(file)

        if file.name not in EXTENSIONS_DICT.keys():
            try:
                if not any(file.iterdir()):
                    file.rmdir()

            finally:
                continue


def change(founded_file: Path):
    '''Strips files apart.'''
    f_suffix = founded_file.suffix.lower()
    f_name = founded_file.stem

    for key, value in EXTENSIONS_DICT.items():

        if f_suffix in value:

            new_f_name = normalize(f_name)
            final_name = new_f_name + f_suffix
            end_folder = main_folder.joinpath(key)
            end_folder.mkdir(exist_ok=True)
            new_file_path = end_folder.joinpath(final_name)

            try:
                founded_file.rename(new_file_path)

            except FileExistsError:

                time_stamp = time.time()
                new_file_path = end_folder.joinpath(
                    new_f_name + '_' + str(time_stamp) + f_suffix)
                founded_file.rename(new_file_path)

            except FileNotFoundError:
                continue

            if key == 'archives':

                base_archive_dir = end_folder.joinpath(new_f_name)
                base_archive_dir.mkdir(exist_ok=False)
                shutil.unpack_archive(new_file_path, base_archive_dir)


def normalize(correct_name: str) -> str:
    '''Replaces different symbols to '_' except letters.'''
    new_main_name = correct_name.translate(trans)

    for i in new_main_name:
        if i.isdigit() or i.isalpha() or i == '_':
            continue
        else:
            new_main_name = new_main_name.replace(i, '_')

    return new_main_name


def to_translate():
    '''Changes Cyrillic letters to Latin letters.'''
    for cyril, latin in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        trans[ord(cyril)] = latin
        trans[ord(cyril.upper())] = latin.upper()