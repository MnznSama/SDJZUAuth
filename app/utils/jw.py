import json
import re
from datetime import datetime

import xlrd as xl

def SolveLesson(lesson):

    time_mapping = {
        "01": ("07:50", "08:35"),
        "02": ("08:40", "09:25"),
        "03": ("09:40", "10:25"),
        "04": ("10:30", "11:15"),
        "05": ("11:20", "12:05"),
        "06": ("13:40", "14:25"),
        "07": ("14:30", "15:15"),
        "08": ("15:30", "16:15"),
        "09": ("16:20", "17:05"),
        "10": ("18:40", "19:25"),
        "11": ("19:30", "20:15"),
        "12": ("20:20", "21:05"),
    }

    name = ''
    teacher = ''
    time = ''
    classroom = ''
    week = ''
    final_time = ''

    if lesson:
        try:
            lessons = lesson.split('|')
            if len(lessons) == 4:
                if '体育' in lessons[0]:
                    name = lessons[0] + lessons[1]
                    teacher = lessons[2]
                    time = lessons[3]
                    classroom = '体育'
                else:
                    name = lessons[0]
                    teacher = lessons[1]
                    time = lessons[2]
                    classroom = lessons[3]

                week = re.search(r"(.*?)\(\[周\]", time).group(1)
                time = re.search(r"周\]\)\[(.*?)节\]", time).group(1)

                sections = time.split('-')
                valid_sections = [s for s in sections if s in time_mapping]

                if valid_sections:
                    start_time = time_mapping[valid_sections[0]][0]  # 取第一节的开始时间
                    end_time = time_mapping[valid_sections[-1]][1]  # 取最后一节的结束时间
                    final_time = f"{start_time}-{end_time}"
                else:
                    final_time = "未找到对应时间"

                return [name, teacher, week, final_time, classroom]

        except Exception as e:
            raise RuntimeError(f"解析课程信息失败: {e}")

def SolveXLS(filedata):

    xls = xl.open_workbook(file_contents=filedata)
    table = xls.sheet_by_index(0)
    nrows = table.nrows
    ncols = table.ncols
    _data = []
    lesson = {}


    for col in range(1, ncols):
       _weekday = table.cell(2, col).value
       lesson[_weekday] = []
       for row in range(3, nrows-1):
            _time = table.cell(row, 0).value.replace('\n','|')
            _lesson = table.cell(row, col).value.strip().replace('\n','|')
            if _lesson:
                lesson1 = _lesson.split('||')
                for i in lesson1:
                    _data = SolveLesson(i)
                    if _data:
                        text = {}
                        text = {'name': _data[0],
                                'teacher': _data[1],
                                'week': _data[2],
                                'time': _data[3],
                                'classroom': _data[4]}
                        lesson[_weekday].append(text)

    return json.dumps(lesson, ensure_ascii=False)


def get_classSchedule(session):

    s = session

    semesterUrl = 'https://xjwgl.sdjzu.edu.cn/jsxsd/xskb/xskb_list.do'
    res = s.get(semesterUrl, allow_redirects=False)
    pattern = r'<option value="([^"]+)"\s+selected="selected"'
    match = re.search(pattern, res.text)
    if match:
        selected_value = match.group(1)  # 提取选中的学年学期
        xnxq = selected_value
    else:
        raise RuntimeError("没有找到当前学年学期")

    xlsUrl = f'https://xjwgl.sdjzu.edu.cn/jsxsd/xskb/xskb_print.do?xnxq01id={xnxq}'
    xls = s.get(url=xlsUrl, allow_redirects=False)

    json_schedule = SolveXLS(xls.content)

    return json_schedule



