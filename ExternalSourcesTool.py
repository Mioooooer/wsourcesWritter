from xml.etree import ElementTree  # 导入ElementTree模块
import os


def recursionFindAll(orcas, keyString, resultList):
    if len(orcas) != 0:
        for orca in orcas:
            #if recursionFindAll(orca) here shall include case like cues in cue
            if orca.get(keyString) != None:
                resultList.append(orca)
            else:
                recursionFindAll(orca, keyString, resultList)#this shall ignore case like cues in another cue

def recursionFind(orcas, keyString):
    for orca in orcas:
        if orca.get(keyString) != None:
            return orca
        else:
            temp = recursionFind(orca, keyString)
            if temp != False:
                return temp
    return False

def pretty_xml(element, indent, newline, level=0):  # elemnt为传进来的Elment类，参数indent用于缩进，newline用于换行
    if element:  # 判断element是否有子元素    
        if (element.text is None) or element.text.isspace():  # 如果element的text没有内容
            element.text = newline + indent * (level + 1)
        else:
            element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)
            # else:  # 此处两行如果把注释去掉，Element的text也会另起一行
            # element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * level
    temp = list(element)  # 将element转成list
    for subelement in temp:
        if temp.index(subelement) < (len(temp) - 1):  # 如果不是list的最后一个元素，说明下一个行是同级别元素的起始，缩进应一致
            subelement.tail = newline + indent * (level + 1)
        else:  # 如果是list的最后一个元素， 说明下一行是母元素的结束，缩进应该少一个    
            subelement.tail = newline + indent * level
        pretty_xml(subelement, indent, newline, level=level + 1)  # 对子元素进行递归操作

def convertFileToXml(XMLInput, iterpath, wavrootpath):
    for root , dirs, files in os.walk(iterpath):
        for name in files:
            if name.endswith(".wav") or name.endswith(".WAV"):
                tempElement = ElementTree.Element('Source', {"Path": os.path.join(wavrootpath, root[2:], name), "Destination": os.path.join(root[2:], name[:-4]+".wem")})
                XMLInput.append(tempElement)
                print(name + "written")




#outpath = input("output path")
#filepath = './'
##for path , dirs, files in os.walk("./"):
        ##for name in files:
            ##if name.endswith(".wsources"):
                ##tree = ElementTree.parse(os.path.join(path, name))
                ##root = tree.getroot()  # 得到根元素，Element类
                #elementList = []
root = ElementTree.Element('ExternalSourcesList', {'SchemaVersion': '1', 'Root': '.\\'})
convertFileToXml(root, "./", ".\\"+os.path.split(os.getcwd())[-1])
pretty_xml(root, '\t', '\n')  # 执行美化方法
tree = ElementTree.ElementTree(root)
tree.write('ExternalSourcesList.wsources', encoding='utf-8', xml_declaration=True)
                ##break
#pretty_xml(root, '\t', '\n')  # 执行美化方法
#tree.write('ExternalSourcesList.wsources', encoding='utf-8', xml_declaration=True)
