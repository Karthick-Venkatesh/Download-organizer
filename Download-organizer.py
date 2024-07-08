from os import scandir, rename
from os.path import splitext, exists, join
from shutil import move
from time import sleep

import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# -> All source directories(Fill by yourself)
# Path should be in this format: "C:/Users/UserName/Downloads"

source_dir = ""

dest_dir_music = ""
dest_dir_video = ""
dest_dir_image = ""
dest_dir_documents = ""
dest_dir_executables = ""
dest_dir_archive = ""

# supported image types
image_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw",
                    ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]
# supported Video types
video_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg",
                    ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]
# supported Audio types
audio_extensions = [".m4a", ".flac", "mp3", ".wav", ".wma", ".aac"]

# supported Document types
document_extensions = [".doc", ".docx", ".odt",
                       ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"]

# supported Executable types
executable_extensions = [".exe", ".app", ".vb",
                       ".scr", ".bat", ".jar", ".run", ".cmd", ".bin", ".x86", ".xlm", ".sh", ".ps1",
                       ".hta", ".fap", ".esh", ".apk", ".ipa", ".msi"]

# supported Archive types
archive_extensions = [".zip", ".7z", ".sitx",
                       ".rar", ".tar", ".taz", ".tbz", ".tgz", ".tz", ".uue", ".vhd", ".vmdk"]


# This function is to deal with file repetition(Files with same names)
def make_unique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    # * IF FILE EXISTS, ADDS NUMBER TO THE END OF THE FILENAME
    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1

    return name


def move_file(dest, entry, name):
    if exists(f"{dest}/{name}"):
        unique_name = make_unique(dest, name)
        oldName = join(dest, name)
        newName = join(dest, unique_name)
        rename(oldName, newName)
    move(entry, dest)


class MoverHandler(FileSystemEventHandler):
    #  THIS FUNCTION WILL RUN WHENEVER THERE IS A CHANGE IN "source_dir"
    #  .upper is for not missing out on files with uppercase extensions
    def on_modified(self, event):
        with scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                self.check_audio_files(entry, name)
                self.check_video_files(entry, name)
                self.check_image_files(entry, name)
                self.check_document_files(entry, name)
                self.check_executable_files(entry, name)
                self.check_archive_files(entry,name)
                

    def check_audio_files(self, entry, name):  # * Checks all Audio Files
        for audio_extension in audio_extensions:
            if name.endswith(audio_extension) or name.endswith(audio_extension.upper()):
                move_file(dest_dir_music, entry, name)
                logging.info(f"Moved audio file: {name}")

    def check_video_files(self, entry, name):  # * Checks all Video Files
        for video_extension in video_extensions:
            if name.endswith(video_extension) or name.endswith(video_extension.upper()):
                move_file(dest_dir_video, entry, name)
                logging.info(f"Moved video file: {name}")

    def check_image_files(self, entry, name):  # * Checks all Image Files
        for image_extension in image_extensions:
            if name.endswith(image_extension) or name.endswith(image_extension.upper()):
                move_file(dest_dir_image, entry, name)
                logging.info(f"Moved image file: {name}")

    def check_document_files(self, entry, name):  # * Checks all Document Files
        for documents_extension in document_extensions:
            if name.endswith(documents_extension) or name.endswith(documents_extension.upper()):
                move_file(dest_dir_documents, entry, name)
                logging.info(f"Moved document file: {name}")

    def check_executable_files(self, entry, name):  # * Checks all Executable Files
        for executable_extension in executable_extensions:
            if name.endswith(executable_extension) or name.endswith(executable_extension.upper()):
                move_file(dest_dir_executables, entry, name)
                logging.info(f"Moved executable file: {name}")

    def check_archive_files(self, entry, name):  # * Checks all Archive Files
        for archive_extension in archive_extensions:
            if name.endswith(archive_extension) or name.endswith(archive_extension.upper()):
                move_file(dest_dir_archive, entry, name)
                logging.info(f"Moved archive file: {name}")


# Code for Detecting Change(No need to change)
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join() 