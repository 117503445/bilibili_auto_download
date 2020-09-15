# version 2020.0504.2200
# author 117503445
# email t117503445@gmail.com

import os


def read_all_text(path: str):
    with open(path, 'r', encoding='utf-8')as f:
        lines = f.readlines()
        text = ''.join(lines)
        return text


def read_all_lines(path: str):
    with open(path, 'r', encoding='utf-8')as f:
        lines = f.readlines()
        for i in range(len(lines)):
            lines[i] = lines[i].replace('\n', '')
            lines[i] = lines[i].replace('\r', '')
        return lines


def write_all_text(path: str, content: str):
    content = str(content)
    create_dir_if_not_exist(os.path.dirname(path))
    with open(path, 'w', encoding='utf-8')as f:
        f.write(content)


def write_all_lines(path: str, content: list):
    if not isinstance(content, list):
        print('file_util write_all_lines() Warning ! content is not list.')
    create_dir_if_not_exist(os.path.dirname(path))
    with open(path, 'w', encoding='utf-8')as f:
        text = '\n'.join(content)
        f.write(text)


def append_all_text(path: str, content: str):
    content=str(content)
    with open(path, 'a', encoding='utf-8')as f:
        f.write(content)


def append_all_texts(path: str, content: list):
    if not isinstance(content, list):
        print('file_util write_all_lines() Warning ! content is not list.')
    with open(path, 'a', encoding='utf-8')as f:
        text = '\n'.    join(content)
        f.write(text)


def create_dir_if_not_exist(path: str):
    if path == '':
        return
    if not os.path.exists(path):
        os.makedirs(path)


def read_csv(path: str):
    lines = read_all_lines(path)
    rows = []
    for line in lines:
        rows.append(line.split(','))
    return rows


def write_csv(path: str, rows: list):
    lines = []
    for row in rows:
        for i in range(len(row)):
            row[i] = str(row[i])
        line = ','.join(row)
        lines.append(line)
    write_all_lines(path, lines)


if __name__ == "__main__":
    write_csv('1.csv', [[1, 2], [2, 3]])
    print(read_csv('1.csv'))
