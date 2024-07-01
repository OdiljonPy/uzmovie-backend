class A:
    name: str
    age: int
    surname: str


a = A()
a.surname = 'Valiyev'
a.name = 'Ali'
a.age = 40

answer = input('pls input the name of field: ')
# print(a.__dict__)
print(getattr(a, answer))
# print(setattr(a, answer))
setattr(a, 'univer', 'JHY')

print(a.__dict__)
