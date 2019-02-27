#!/usr/bin/env python3

import base64
import re
import sys
import textwrap

import filetype
import win32clipboard


def pic2base64(src_pic):
    '''
    图片转为base64
    :param file: 文件
    :return: str
    '''

    with open(src_pic, 'rb') as f:
        pic_base64 = base64.b64encode(f.read())
    return pic_base64


def parse2mdsyntax(src_pic):
    '''
    生成md语句
    :param src_pic: 文件
    :return: str
    '''
    pic_type = filetype.guess(src_pic)
    pic_base64 = bytes.decode(pic2base64(src_pic))
    pic_name = re.split(r'[\\\/]', src_pic)[-1]
    if pic_type:
        deststr = textwrap.dedent("""
        ![{}][{}]

        [{}]:data:{};base64,{}
        """.format(pic_name, pic_name, pic_name, pic_type.mime, pic_base64))
    else:
        deststr = pic_base64
    return deststr


if __name__ == '__main__':
    src_pic = sys.argv[1]
    deststr = parse2mdsyntax(src_pic)

    # 将最终语句粘贴到剪切板
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(deststr)
    win32clipboard.CloseClipboard()
