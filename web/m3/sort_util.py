from pathlib import Path
import sys
import os
import shutil
from threading import Thread, Semaphore
import logging
from time import time


def normilise(line):
    cyrilic_symbols = "àáâãäå¸æçèéêëìíîïðñòóôõö÷øùúûüýþÿº³¿´"
    latin_symbols = (
     "a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
     "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
    punctuation = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~¹ """
    translate_dict = {}
    for cyr, lat in zip(cyrilic_symbols, latin_symbols):
        translate_dict[ord(cyr)] = lat
        translate_dict[ord(cyr.upper())] = lat.upper()
    latin_line = line.translate(translate_dict)
    for char in latin_line:
        if char in punctuation:
            latin_line = latin_line.replace(char, '_')
    return latin_line


known_suffix = {'images': ['.JPEG', '.PNG', '.JPG', '.SVG'],
                    'video': ['.AVI', '.MP4', '.MOV', '.MKV'],
                    'documents': ['.DOC', '.DOCX', '.TXT', '.PDF', '.XLSX', '.PPTX'],
                    'audio': ['.MP3', '.OGG', '.WAV', '.AMR'],
                    'archives': ['.ZIP', '.GZ', '.TAR']
                    }

def sort_in_dir(dir_path:Path, condition):
    with condition:
        timer = time()

        local_path_dir = dir_path

        for file in local_path_dir.iterdir():  # iterating under each file into directory

            file_path = Path.joinpath(local_path_dir, file.name)  # make a path to file or dir

            if file.suffix.upper() in known_suffix['images']:
                images_dir_path = Path.joinpath(local_path_dir, 'images')  # create a path to a new dir
                images_dir_path.mkdir(parents=True, exist_ok=True)  # make a new dir based on path to this dir

                file_path_in_new_dir = Path.joinpath(images_dir_path,
                                                     file.name)  # create a file path into a new dir
                os.replace(file_path, file_path_in_new_dir)  # replace file to a new dir

                rename_file = normilise(file.name.replace(file.suffix, '')) + file.suffix  # make a new file name
                renamed_file_path_in_new_dir = Path.joinpath(images_dir_path,
                                                             rename_file)   # create a path to renamed file
                os.rename(file_path_in_new_dir, renamed_file_path_in_new_dir)  # rename file into new dir


            elif file.suffix.upper() in known_suffix['video']:
                video_dir_path = Path.joinpath(local_path_dir, 'video')
                video_dir_path.mkdir(parents=True, exist_ok=True)

                file_path_in_new_dir = Path.joinpath(video_dir_path, file.name)
                os.replace(file_path, file_path_in_new_dir)

                rename_file = normilise(file.name.replace(file.suffix, '')) + file.suffix
                renamed_file_path_in_new_dir = Path.joinpath(video_dir_path, rename_file)
                os.rename(file_path_in_new_dir, renamed_file_path_in_new_dir)  # rename file into new dir


            elif file.suffix.upper() in known_suffix['documents']:
                document_dir_path = Path.joinpath(local_path_dir, 'documents')  # create a path to a new dir
                document_dir_path.mkdir(parents=True, exist_ok=True)  # make a new dir based on path to this dir

                file_path_in_new_dir = Path.joinpath(document_dir_path,
                                                     file.name)  # create a file path into a new dir
                os.replace(file_path, file_path_in_new_dir)  # replace file to a new dir

                rename_file = normilise(file.name.replace(file.suffix, '')) + file.suffix  # make a new file name
                renamed_file_path_in_new_dir = Path.joinpath(document_dir_path,
                                                             rename_file)  # create a path to renamed file
                os.rename(file_path_in_new_dir, renamed_file_path_in_new_dir)


            elif file.suffix.upper() in known_suffix['audio']:
                audio_dir_path = Path.joinpath(local_path_dir, 'audio')
                audio_dir_path.mkdir(parents=True, exist_ok=True)

                file_path_in_new_dir = Path.joinpath(audio_dir_path, file.name)
                os.replace(file_path, file_path_in_new_dir)

                rename_file = normilise(file.name.replace(file.suffix, '')) + file.suffix  # make a new file name
                renamed_file_path_in_new_dir = Path.joinpath(audio_dir_path,
                                                             rename_file)  # create a path to renamed file
                os.rename(file_path_in_new_dir, renamed_file_path_in_new_dir)



            elif file.suffix.upper() in known_suffix['archives']:
                archive_dir_path = Path.joinpath(local_path_dir, 'archives')
                archive_dir_path.mkdir(parents=True, exist_ok=True)
                sub_archive_dir_path = Path.joinpath(archive_dir_path, file.name.replace(file.suffix, ''))
                Path(sub_archive_dir_path).mkdir(parents=True, exist_ok=True)
                new_file_path = Path.joinpath(archive_dir_path, file.name)
                os.replace(file_path, new_file_path)
                shutil.unpack_archive(new_file_path, sub_archive_dir_path)

            else:
                pass


        new_dir_name = normilise(dir_path.name)
        if not Path.joinpath(dir_path.parent, new_dir_name).exists():
            new_dir_name_path = Path.joinpath(dir_path.parent, new_dir_name)
            os.rename(dir_path, new_dir_name_path)

        logging.debug(f'Done {time()-timer}')


folders = []


def folder_tree(base_path: Path):
    for file in base_path.iterdir():
        if file.is_dir() and (file.name not in known_suffix):
            folders.append(file)
            folder_tree(file) #recursion


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format="%(threadName)s %(message)s")
    logging.debug('Start program')

    if len(sys.argv) < 2:
        print('Please provide correct path')
        exit()
    base_folder = Path(sys.argv[1])
    if not (os.path.exists(base_folder) and Path(base_folder).is_dir()):
        print('inputed path is not existed or it\'s not a dir')
        exit()

    new_base_folder_name = normilise(base_folder.name)
    base_folder_new_path = Path.joinpath(base_folder.parent, new_base_folder_name)
    base_folder.rename(base_folder_new_path)

    folders.append(base_folder_new_path)
    folder_tree(base_folder_new_path)
    print(f'List of folders under sorting')
    [print(i, folders[i]) for i in range(len(folders))]

    threads = []
    pool = Semaphore(50)
    for folder in folders:
        thread = Thread(target=sort_in_dir, args=(folder, pool))
        thread.start()
        threads.append(thread)

    [el.join() for el in threads]
    logging.debug('End program')