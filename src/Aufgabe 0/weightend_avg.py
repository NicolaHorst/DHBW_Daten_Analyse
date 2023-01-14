gpa = 0
all_ects = 0
while True:
    cont = input("contnue:")
    if cont == "n":
        break
    grade = float(input("grade:"))
    ects = float(input("ects:"))

    gpa += grade * ects
    all_ects += ects

print(f" GPA = {gpa / all_ects}")
print(f" ects = {all_ects}")