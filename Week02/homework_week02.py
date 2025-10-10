# Homework Week02
print("1. List learning")

uni = ["Tokyo", "Kyoto", "Waseda", "Keio"]
print(uni)

uni.append("Osaka")
print(uni)

uni.insert(2, "Tohoku")
print(uni)

removed_item = uni.pop()
print(uni)

sorted_uni = sorted(uni)
print(sorted_uni)

uni.sort(reverse=True)
print(uni)

uni_copy = uni[:]
uni_copy[0] = "ok"
print(uni_copy)


print("2. Tuple learning")

Japan_city = ("Tokyo", "Osaka", "Kyoto", "Kobe")
print(Japan_city)
print(type(Japan_city))

print("Tuple is immutable")

city = Japan_city + ("Beijing", "Shanghai")
print(city)


print("3. Nesting learning")

student = ("Zixuan", 37, ["power", "energy", "system"])
print(student)

student[2].append("EV")
print(student)

score = [(90, 99), (80, 88), (70, 77)]
print(score)

score[0] = (60, 66)
print(score)


print("4. Intentionally causing an error")

tuple_error = (1, 2, 3)
tuple_error[1] = 4