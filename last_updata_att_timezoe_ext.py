from urllib import response
import pyodbc
from xmlrpc import client as xmlrpclib
from datetime import datetime, timedelta
# import time
limit=datetime.now()- timedelta(days=31)
# limit=(timezone(timedelta(seconds=-time.timezone)))-timedelta(days=31)
# print('')


limitstr=str(limit.month)+"/"+str(limit.day)+"/"+str(limit.year)

conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Program Files (x86)\Limton Innovative Systems\Suprema_Standard_Setup\Database\SupremaPollingManager.mdb;')
cursor = conn.cursor()
# print("hello world")
stmt="SELECT Attendance.PinNumber, Attendance.AttendanceDateTime from Attendance where Attendance.AttendanceDateTime > #"+limitstr+"# ;"
# stmt="SELECT TOP 5 * from Attendance;"
cursor.execute(stmt)
attendaces=cursor.fetchall()
print(attendaces)
stmt="SELECT Employee.EmpID,Employee.EmployeeName  FROM Employee;"
cursor.execute(stmt)
employees=cursor.fetchall()
# print(employees)



# # odoo server connection
url = 'http://209.58.178.202:8069'
db = 'ubw_primary'
username = 'admin'
password = 'admin'

common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))

uid = common.login(db, username, password)

# var = common.version()

# models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))

# # uid = common.authenticate(db, username, password, {})
# # print('UID',uid)

odoo_employeeIds=models.execute_kw(db, uid, password,
    'hr.employee', 'search',
    [[]])
odoo_employee = models.execute_kw(db, uid, password,
    'hr.employee', 'read',[odoo_employeeIds],{'fields':['name','id','pin']})
odoo_employee_pins=[a['pin'] for a in odoo_employee]


for emp in employees:
        empname=emp[0]
        if empname not in odoo_employee_pins:
                data={ 
                                            'pin': emp[0],
                                            'name':emp[1],
                                            
                                            }
                print("processing Entry: "+str(data))
                response = models.execute_kw(db, uid, password,
                            'hr.employee', 'create',
                                    [data])



                
def groupattendaces(listofAttendances):
        groupDict={}
        temp=[]
        for attendance in listofAttendances:
                key=(attendance[0],attendance[1].date())
                #print(key)
                if key not in temp:
                        groupDict[key]=[]
                        temp.append(key)
                groupDict[key].append(attendance)
        for key in groupDict.keys():
                groupDict[key].sort(key=lambda x : x[1])
        return groupDict

groupedAttendances=groupattendaces(attendaces)

# print(groupedAttendances)

for key in groupedAttendances.keys():
        groupedAttendance=groupedAttendances[key]

        ## for odoo,checkin and checkout must be present at same moment. If there are less then 2 entries of a person in a day. that means this entry canot be process. so we skipped it . 
        if len(groupedAttendance)<2:
                checkInTime=groupedAttendance[0][1]
                checkoutTime=groupedAttendance[0][1]
        else:
                ## pick first entry as checkin
                checkInTime=groupedAttendance[0][1]
                ## pick last entry as checkout
                checkoutTime=groupedAttendance[-1][1]
        checkInTime=checkInTime-timedelta(hours=5)
        checkoutTime=checkoutTime-timedelta(hours=5)

        #we need employee id present in odoo for this person
        emp=models.execute_kw(db, uid, password,
                'hr.employee', 'search',
                [[['pin','=',int(key[0])]]])
        if len(emp)<1:
                print("No emp with pin : " +str(int(key[0])))
                continue
        empid=emp[0]
        
        ##check and bring any attendance for this day and employee if any
        checkin_already_exist= models.execute_kw(db, uid, password,
                'hr.attendance', 'search',
                [[['employee_id','=',empid],['check_in','=',checkInTime]]])
        attendance_already_exist=models.execute_kw(db, uid, password,
                'hr.attendance', 'search',
                [[['employee_id','=',empid],['check_in','=',checkInTime],['check_out','=',checkoutTime]]])
        
        if attendance_already_exist:
                continue
        #prepare attendance entry
        data={
                'employee_id':empid,
                'check_in': str(checkInTime),
                'check_out': str(checkoutTime),
                }
        
        if not checkin_already_exist:
                print(" creating entry : "+str(data))
                createdobj= models.execute_kw(db, uid, password,
                'hr.attendance', 'create',[data])

        else:
                print(" overwriting entry : "+str(data))
                writtenobj=models.execute_kw(db, uid, password,
                'hr.attendance', 'write',[[checkin_already_exist[0]],data])
        


conn.close()