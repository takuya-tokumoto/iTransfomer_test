import pathlib
import glob
import os
import shutil

def tree(path, layer=0, is_last=True, indent_current='　', show_files=True):
    '''
        指定したディレクトリの配下構造を可視化
    '''
    
    if not pathlib.Path(path).is_absolute():
        path = str(pathlib.Path(path).resolve())

    # カレントディレクトリの表示
    current = path.split('/')[::-1][0]
    if layer == 0:
        print('<' + current + '>')
    else:
        branch = '└' if is_last else '├'
        print('{indent}{branch}<{dirname}>'.format(indent=indent_current, branch=branch, dirname=current))

    # 下の階層のパスを取得
    paths = [p for p in glob.glob(path + '/*') if os.path.isdir(p) or (show_files and os.path.isfile(p))]
    def is_last_path(i):
        return i == len(paths) - 1

    # 再帰的に表示
    for i, p in enumerate(paths):
        indent_lower = indent_current
        if layer != 0:
            indent_lower += '　　' if is_last else '│　'

        if os.path.isfile(p) and show_files:
            branch = '└' if is_last_path(i) else '├'
            print('{indent}{branch}{filename}'.format(indent=indent_lower, branch=branch, filename=p.split('/')[::-1][0]))
        elif os.path.isdir(p):
            tree(p, layer=layer + 1, is_last=is_last_path(i), indent_current=indent_lower, show_files=show_files)



def copy_images(src_dir, dst_dir, extension=None, prefix=''):
    # dst_dir が存在しない場合は作成する
    os.makedirs(dst_dir, exist_ok=True)

    # # dst_dir にファイルが既に存在する場合は実行しない
    # if os.listdir(dst_dir):
    #     print(f'Files already exist in {dst_dir}. Aborting operation.')
    #     return

    if extension:
        pattern = os.path.join(src_dir, '**', f'*.{extension}')
        files_to_copy = glob.glob(pattern, recursive=True)
    else:
        files_to_copy = glob.glob(os.path.join(src_dir, '**', '*'), recursive=True)

    for file in files_to_copy:
        filename = os.path.basename(file)
        destination = os.path.join(dst_dir, prefix + filename)
        shutil.copy(file, destination)
        print(f'Copied: {file} to {destination}')
        # shutil.copy(file, dst_dir)
        # print(f'Copied: {file} to {dst_dir}')