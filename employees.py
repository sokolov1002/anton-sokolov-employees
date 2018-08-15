import sys
from datetime import datetime
from collections import namedtuple
from collections import defaultdict
import operator

with open(sys.argv[1], 'r') as file:
    data = [entry.replace(',', '').split() for entry in file]

    employees = {}

    for i in range(len(data)+1):
        for item in data:
            employees.update({item[0]: {k: v for k, v in zip(['ProjectID', 'DateFrom', 'DateTo'], item[1:])}})

    emp_common_projects = defaultdict(list)
    for k, v in employees.items():
        emp_common_projects[v['ProjectID']].append(k)

    overlap_dict = {}

    for k, v in emp_common_projects.items():
        if len(v) == 1:
            print("Employee {} has been working alone on project {}.".format(v, k))
        else:
            Range = namedtuple('Range', ['start', 'end'])
            date_format = '%Y-%m-%d'

            date_from1 = datetime.strptime(employees[v[0]]['DateFrom'], date_format)
            if employees[v[0]]['DateTo'] == 'NULL':
                date_to1 = datetime.today()
            else:
                date_to1 = datetime.strptime(employees[v[0]]['DateTo'], date_format)
            r1 = Range(start=date_from1, end=date_to1)

            date_from2 = datetime.strptime(employees[v[1]]['DateFrom'], date_format)
            if employees[v[1]]['DateTo'] == 'NULL':
                date_to2 = datetime.today()
            else:
                date_to2 = datetime.strptime(employees[v[1]]['DateTo'], date_format)
            r2 = Range(start=date_from2, end=date_to2)

            latest_start = max(r1.start, r2.start)
            earliest_end = min(r1.end, r2.end)
            delta = (earliest_end - latest_start).days + 1
            overlap = max(0, delta)
            overlap_dict.update({(v[0], v[1]): overlap})
            if overlap != 0:
                print("Employees {} have been working together on project {} for {} days.".format(v, k, overlap))

    print("Employees {} have been working most time together.".format(max(overlap_dict.items(), key=operator.itemgetter(1))[0]))
