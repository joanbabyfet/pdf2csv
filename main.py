import pdfplumber
import time
import pandas as pd

# pdf文件
pdf_file = 'example.pdf' 

def get_pdf_content(filename):
    page_list = [] # 所有页内容
    
    pdf = pdfplumber.open(filename, password='')
    for page in pdf.pages: # 每页提取
        temp = []
        text = page.extract_text()
        
        for line in text.split('\n'): # 每行提取
            temp.append(line)
        page_list.append(temp)
    pdf.close()
    return page_list

def main():
    try:
        keywords = {
            '登記日期：': 14,
            '原因發生日期：': 12,
            '登記原因：': 2,
            '地    目：': 1,
            '面    積：': 16,
            '使用分區：': 4,
            '使用地類別：': 4,
            '公告土地現值：': 15,
            '地上建物建號：': 19,
            '所有權人：': 4,
            '住    址：': 8,
            '管 理 者：': 7,
            '權利範圍：': 25,
        }
        data = get_pdf_content(pdf_file)

        match_list = []
        for index, page in enumerate(data): # 几页循环几次
            list_temp = []
            dict_temp = {} # 开始每页提取时清空
            for line in page:   # 第n页逐行提取
                for k, v in keywords.items(): # 每行匹配关键词
                    word_index = line.find(k) # 返回该字符串第1次出现下标
                    if word_index != -1:
                        word_len = len(k)
                        dict_temp[k] = line[word_index + word_len: word_index + word_len + v].strip()
            list_temp.append(dict_temp)
            match_list.append(list_temp)

        headers  = list(keywords.keys())
        export_data = {} # 组装数据, 类型为字典
        for k in range(len(headers)):
            values = []
            for index in range(len(match_list)):
                if headers[k] in match_list[index][0]:
                    values.append(match_list[index][0][headers[k]])
                else:
                    values.append('')
            export_data[headers[k].replace('：', '')] = values

        df = pd.DataFrame(export_data)
        filename = 'land_' + time.strftime("%Y%m%d%H%M%S", time.localtime()) + '.csv' # 导出文件名
        df.to_csv(filename, index=False, header=True, encoding='utf-8-sig') # utf-8-sig 解决csv乱码
        print('导出csv成功')
    except:
        print('导出csv失败')

if __name__ == '__main__': # 主入口
    main()