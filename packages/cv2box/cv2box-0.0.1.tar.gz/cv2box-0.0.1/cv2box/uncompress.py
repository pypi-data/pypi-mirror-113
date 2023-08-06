import os


def get_shell(shell_type, file_path):
    if shell_type == 'compress':
        os.system('cp ./shell_scripts/uncompress.sh {}'.format(file_path))
