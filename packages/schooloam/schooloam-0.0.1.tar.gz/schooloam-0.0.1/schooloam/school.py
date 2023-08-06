#school

class Student:
    def __init__(self,name,lastname):
        self.name = name
        self.lastname = lastname
        self.exp = 0  # EXP
        self.lesson = 0
        self.vehicle = 'Bus'
    @property
    def fullname(self):
        return '{} {}'.format(self.name,self.lastname)

    def Coding(self):
        '''คลาสเรียนวิชาเขียนโปรแกรม'''
        self.AddExp()
        print('{} is Codinggg...'.format(self.fullname))

    def ShowExp(self):
        return '{} has {} exp เรีนนไป {} ครั้ง'.format(self.name,self.exp,self.lesson)

    def AddExp(self):
        self.exp += 10
        self.lesson += 1

    def __str__(self):
        return self.fullname
    def __repr__(self):
        return self.fullname # Name
    def __add__(self, other):
        return self.exp + other.exp

class Tesla:
    def __init__(self):
        self.model = 'Model S'

    def SelfDriving(self,st):
        print('Autopilot Mode... by {}'.format(st.name))

    def __str__(self):
        return self.model

class SpecialStudent(Student):
    def __init__(self,name,lastname,father):
        super().__init__(name,lastname)

        self.father = father
        self.vehicle = Tesla()
        print('รู้มั้ยฉันคือใคร   พ่อฉันคือออ {}'.format(self.father))

    def AddExp(self):
        self.exp += 30
        self.lesson += 2
class Teacher:
    def __init__(self,fullname):
        self.fullname = fullname
        self.students = []

    def CheckStudent(self):
        print('<<<Teacher: {}>>>'.format(self.fullname))
        for i,st in enumerate(self.students):
            print('{}-->{} [{}exp][{}lesson ]'.format(i+1,st.fullname,st.exp,st.lesson))
    def AddStudent(self,st):
        self.students.append(st)
print('FILE:',__name__)
if __name__ == '__main__':
    print(__name__)

    allstudent = []

    teacher1 = Teacher('ADA Lovelace')
    teacher2 = Teacher('Isaac Newton')
    print(teacher1.students)

    print('-----Day1-----')
    st1= Student('JoJo',"Jostar")
    allstudent.append(st1) # register append list
    teacher2.AddStudent(st1)
    print(st1.fullname)

    print('-----Day2-----')
    st2 = Student('Jonathan','Jostar')
    allstudent.append(st2)
    teacher2.AddStudent(st2)
    print(st2.fullname)

    print('-----Day3-----')
    st2.Coding()
    for i in range(3):
        st1.Coding()
    # print('{} has {} exp'.format(st1.name,st1.exp))
    print(st1.ShowExp())
    print(st2.ShowExp())

    print('-----Day4-----')
    stp1 = SpecialStudent('Thomas','Edison','Robert')
    allstudent.append(stp1)
    teacher1.AddStudent(stp1)
    print(stp1.fullname)
    print('คุณครูครับ ขอคะแนนฟรั 20 ได้ไหม')
    stp1.exp = 20
    stp1.Coding()
    stp1.ShowExp()

    print('-----Day5-----')
    print('Go Home')
    print(allstudent)
    for st in allstudent:
        print('{} go home by {}'.format(st.fullname,st.vehicle))
        print(isinstance(st,SpecialStudent))
        if isinstance(st,SpecialStudent):
            st.vehicle.SelfDriving(st)

    print('-----Day6-----')
    teacher1.CheckStudent()
    teacher2.CheckStudent()

    print('Sum',st1+st2)