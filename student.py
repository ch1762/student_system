import os
import re
import time


# 保存学生信息
filename = 'student.txt'

# 显示菜单
def menu():
    print('''
    ╔———————学生信息管理系统————————╗
    │                                              │
    │   =============== 功能菜单 ===============   │
    │                                              │
    │   1 录入学生信息                             │
    │   2 查找学生信息                             │
    │   3 删除学生信息                             │
    │   4 修改学生信息                             │
    │   5 排序                                     │
    │   6 统计学生总人数                           │
    │   7 显示所有学生信息                         │
    │   0 退出系统                                 │
    │  ==========================================  │
    │  说明：通过数字或↑↓方向键选择菜单          │
    ╚———————————————————————╝
    ''')


# 增
def insert():
    studentList = []
    mark = True#是否继续增加

    while mark:
        id = input('请输入ID：')
        if not id:
            print('ID不能为空！')
            break
        name = input('请输入名字：')
        if not name:
            print('名字不能为空！')
            break
        try:
            english = int(input('请输入英语成绩：'))
            math = int(input('请输入数学成绩：'))
            python = int(input('请输入python成绩：'))
        except:
            print('输入无效，请重新输入！')
            continue

        student = {'id':id,'name':name,'english':english,'python':python,'math':math}
        studentList.append(student)
        inputMark = input('是否继续添加?(y/n)')
        if inputMark == 'y':
            mark = True
        else:
            mark = False
    save(studentList)
    print('学生信息录入完毕！')

def save(student):
    try:
        student_txt = open(filename,'a')
    except Exception as e:
        student_txt = open(filename,'w')#文件不存在，创建文件
    for info in student:
        student_txt.write(str(info)+'\n')#按行存储
    student_txt.close()

# 删
def delete():
    mark = True
    while mark:
        studentId = input('请输入要删除学生的学号：')
        answer = input('是否确认删除？（y/n）')
        if answer == 'n':
            continue
        if studentId is not '':
            if os.path.exists(filename):
                with open(filename,'r') as rf:
                    studentinfo = rf.readlines()
            else:
                studentinfo = []
            ifdel = False
            if studentinfo:
                with open(filename,'w') as wf:
                    d = {}
                    for list in studentinfo:
                        d = dict(eval(list))
                        if d['id'] != studentId:
                            wf.write(str(d)+'\n')
                        else:
                            ifdel = True
                    if ifdel:
                        print('ID为 %s 的学生已经被删除'%studentId)
                    else:
                        print('没有找到ID为 %s 的学生 '%studentId)
            else:
                print('无学生信息')
                break
            inputMark = input('是否继续删除？（y/n）')
            if inputMark == 'y':
                mark = True
            else:
                mark = False

# 改
def change():
    show()
    mark = True
    if os.path.exists(filename):
        with open(filename,'r') as rf:
            studentinfo = rf.readlines()
    else:
        return
    studentId = input('请输入要修改学生的ID：')
    with open(filename,'w') as wf:
        for student in studentinfo:
            d = dict(eval(student))#字符串转字典
            if d['id'] == studentId:
                while True:
                    try:
                        d['name'] = input('请输入名字：')
                        d['english'] = int(input('请输入英语成绩：'))
                        d['math'] = int(input('请输入数学成绩：'))
                        d['python'] = int(input('请输入python成绩：'))
                    except:
                        print('输入有误，请重新输入')
                    else:
                        break
                student = str(d)
                wf.write(student + '\n')
                print('修改成功!')
            else:
                wf.write(student)
        inputMark = input('是否继续修改？（y/n）')
        if inputMark == 'y':
            change()

# 排序
def sort():
    show()
    if os.path.exists(filename):
        with open(filename,'r') as rf:
            studentinfo = rf.readlines()
            studentsort = []
        for list in studentinfo:
            d = dict(eval(list))
            studentsort.append(d)
    else:
        return
    ascORdesc = input('1升序 或者 降序2？')
    if ascORdesc == '1':
        ascORdescBool = False
    elif ascORdesc == '2':
        ascORdescBool = True
    else:
        print('输入有误，请重新输入')
        sort()
    mode = input('请选择排序方式（1 按英语成绩 2 按数学成绩 3 按python成绩 4 按总成绩）')
    if mode == '1':
        studentsort.sort(key=lambda x:x['english'],reverse=ascORdescBool)
    elif mode == '2':
        studentsort.sort(key=lambda x:x['math'],reverse=ascORdescBool)
    elif mode == '3':
        studentsort.sort(key=lambda x:x['python'],reverse=ascORdescBool)
    elif mode == '4':
        studentsort.sort(key=lambda x:(x['english']+x['math']+x['python']),reverse=ascORdescBool)
    else:
        print('输入有误，请重新输入')
        sort()
    show_student(studentsort)

# 查
def search():
    mark = True
    student_query = []
    while mark:
        id = ''
        name = ''
        if os.path.exists(filename):
            mode = input('按ID查询输入1，按名字查询输入2')
            if mode == '1':
                id = input('请输入ID：')
            elif mode == '2':
                name = input('请输入名字：')
            else:
                print('输入有误，请重新输入！')
                search()
            with open(filename,'r') as f:
                student = f.readlines()
                for stu in student:
                    d = dict(eval(stu))
                    if id is not '':
                        if d['id'] == id:
                            student_query.append(d)
                    elif name is not '':
                        if d['name'] == name:
                            student_query.append(d)
                show_student(student_query)
                student_query.clear()
                inputMark = input('是否继续查找？（y/n）')
                if inputMark == 'y':
                    mark = True
                else:
                    mark = False
        else:
            print('未保存数据。。。')
            return

# 将保存在列表中的学生信息显示出来
def show_student(studentList):
    if not studentList:
        print('无数据信息')
        return
    format_title = "{:^6}{:^12}\t{:^8}\t{:^10}\t{:^10}\t{:^10}"
    print(format_title.format("ID", "名字", "英语成绩", "数学成绩", "python成绩", "总成绩"))
    format_data = "{:^6}{:^12}\t{:^12}\t{:^12}\t{:^12}\t{:^12}"
    for info in studentList:
        print(format_data.format(info.get("id"), info.get("name"),
                                 str(info.get("english")), str(info.get("python")),str(info.get("math")),
                                 str(info.get("english") + info.get("python") + info.get("math")).center(12)))
    time.sleep(1)

# 显示学生总数
def total():
    if os.path.exists(filename):
        with open(filename,'r') as rf:
            studentinfo = rf.readlines()
            if studentinfo:
                print('一共有 %d 名学生！'%len(studentinfo))
                time.sleep(1)
            else:
                print('暂时没有学生信息')
    else:
        print('暂时没有数据信息')

# 显示所有学生信息
def show():
    student_new = []
    if os.path.exists(filename):
        with open(filename,'r') as rf:
            studentinfo = rf.readlines()
        for student in studentinfo:
            student_new.append(eval(student))#将学生信息添加进student_new中
        if student_new:
            show_student(student_new)#打印学生信息
    else:
        print('暂未保存数据信息')

    time.sleep(1)

def main():
    ctrl = True  # 标记是否退出系统
    while ctrl:
        menu()
        option = input('请选择：')
        option_str = re.sub("\D", "", option)
        if option_str in ['0', '1', '2', '3', '4', '5', '6', '7']:
            option_int = int(option_str)
            if option_int == 0:
                print('您已退出本系统！')
                ctrl = False
            elif option_int == 1:
                insert()
            elif option_int == 2:
                search()
            elif option_int == 3:
                delete()
            elif option_int == 4:
                change()
            elif option_int == 5:
                sort()
            elif option_int == 6:
                total()
            elif option_int == 7:
                show()
        else:
            print('请输入有效的数字！')


if __name__ == '__main__':
    main()
