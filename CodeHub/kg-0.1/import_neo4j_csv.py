import csv
import hashlib


# md5加密成唯一id
def get_md5(string):
    """Get md5 according to the string
    """
    byte_string = string.encode("utf-8")
    md5 = hashlib.md5()
    md5.update(byte_string)
    result = md5.hexdigest()
    return result


# 输入的文件信息，输出Person实体的csv信息文件
# input 输入的文件路径名
# output 输出的文件路径名
# Person实体暂时先只设置姓名，其他信息tushare中需要额外积分
def built_Person(input = 'data1.csv', output='Person.csv'):
    with open(input, 'r', encoding='utf-8') as file_prep, \
            open(output, 'w', encoding='utf-8') as file_output:

        file_prep_csv = csv.reader(file_prep, delimiter=',')
        file_output_csv = csv.writer(file_output, delimiter=',')

        headers = ['person_id:ID', 'name', ':LABEL']
        file_output_csv.writerow(headers)
        for i, row in enumerate(file_prep_csv):

            # 第一行跳过
            if i == 0:
                continue

            for name in row[2:5]:
                info=[name]
                info_id = get_md5('{}'.format(name))
                info.insert(0,info_id)
                info.append('Person')
                file_output_csv.writerow(info)

        file_prep.close()
        file_output.close()
    print("done")


# 输入的文件信息，输出Stock实体的csv信息文件
# input 输入的文件路径名
# output 输出的文件路径名
# Person实体暂时先只设置姓名，其他信息tushare中需要额外积分
def build_Stock(input = 'data2.csv', output='Stock.csv'):

    with open(input, 'r', encoding='utf-8') as file_prep, \
            open(output, 'w', encoding='utf-8') as file_output:

        file_prep_csv = csv.reader(file_prep, delimiter=',')
        file_output_csv = csv.writer(file_output, delimiter=',')

        headers = ['stock_id:ID', 'code', 'name','industry', ' market',':LABEL']
        file_output_csv.writerow(headers)

        for i, row in enumerate(file_prep_csv):

            # 第一行跳过
            if i == 0:
                continue

            info = [row[1], row[2],row[3],row[4]]
            info_id = row[1].split('.')[0] # 以股票代码为图谱中id标识
            info.insert(0, info_id)
            info.append('Stock')
            file_output_csv.writerow(info)

        file_prep.close()
        file_output.close()
    print("done")

# data1中既有Person和Stock信息
def build_Person_Stock(input = 'data1.csv', output='Person_Stock.csv'):
    """Create an 'executive_stock' file in csv format that can be imported into Neo4j.
    format -> :START_ID,title,:END_ID,:TYPE
               person          stock
    type -> chairman    manager     secretary
    """
    with open(input, 'r', encoding='utf-8') as file_prep, \
        open(output, 'w', encoding='utf-8') as file_output:

        file_prep_csv = csv.reader(file_prep, delimiter=',')
        file_output_csv = csv.writer(file_output, delimiter=',')

        headers = [':START_ID', 'jobs', ':END_ID', ':TYPE']
        Jobs = ['chairman_of','manager_of','secretary_of'] # 关系实体employ_of分类

        file_output_csv.writerow(headers)

        for i, row in enumerate(file_prep_csv):
            if i == 0:
                continue

            end_id = row[1].split('.')[0]  # code
            k = 2
            while(k<5):
                start_id = get_md5(row[k])
                relation = [start_id, Jobs[k-2], end_id, 'employ_of']
                k = k+1
                file_output_csv.writerow(relation)
        file_prep.close()
        file_output.close()

if __name__ == '__main__':
    built_Person()
    build_Stock()
    build_Person_Stock()

