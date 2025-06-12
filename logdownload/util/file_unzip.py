import zlib, base64

def unzip(file_text):
    '''
    unzip函数，用于对文件进行解压缩操作。
    ### 参数：
    - file_text: str类型，待解压的文件内容
    ### 返回值：
    - text_data: 解压后的文本数据
    - type: str类型，文本类型

'''
    
    zip_text = base64.b64decode(file_text)  # 先解一遍base64
    
    b_text = zlib.decompress(zip_text[1:], -15)  # 跳过\x00并忽略头部

    text_data = b_text.decode('gbk', errors='ignore')  # 自动识别并去除BOM

    return text_data

if __name__ == '__main__':

    file_text = "AGWPvY4CMQyEeyTeYaRtuGYfgIoGiYKOe4HcZrQbyetEcRaOt8cgfnQ62ZU183mm w6mEGYesvJbcbL3qfHFMSsMPx6SadMQltQkdQiWGPM/Ut/Jhn172h0LyEAScQxKE GCvNHFaWWrJRroi0NCojWnaaCIcGc0x/531PNP4z25QXiVCeWT0Wgn0QYWiL/1uM 1fpnqr02F3qqvyQUv4p3w4a/Ww97puyCNO291dd6dZ8bvlv4nw=="
    
    text = unzip(file_text)

    print(text)
