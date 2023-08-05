
# 创建一个写入的文件对象
from Document_processing.english_pkg.Separate_words import Separate_english

# 创建对象
port = Separate_english()

#打开文件
port.open(url='./英语E、F开头单词 音标.docx')

port.document_write.add_heading(u'将单词按词性分类', 0)

port.count_of_type()
port.write()

#将程序写入缓存的内容，写入文件，参数为最终文件的文件名

port.save("实例文件.doc")
print(port.cixing)
print("end")


