user_database = [
    {'name': 'A', 'age': 30, 'hobbies': ['reading', 'tennis']},
    {'name': 'B', 'age': 15, 'hobbies': ['coding', 'sleeping']},
    {'name': 'C', 'age': 25, 'hobbies': ['swimming', 'skip_hobby', 'golf']}, 
    {'name': 'D', 'age': 45, 'hobbies': ['football', 'music']}, 
    {'name': 'E', 'age': 20, 'hobbies': ['painting', 'dancing']}
]

print("A and C will be processed. B will be skipped. D will trigger break. E won't be processed.")

def process_data(data_list, age_limits_tuple):

    min_age, max_age = age_limits_tuple
    
    valid_users_list = []
    user_hobby_dict = {}

    print(f"Age Limits: {min_age} - {max_age}")

    for user in data_list:
        user_name = user['name']
        user_age = user['age']
        
        if user_age < min_age:
            print(f"skip: {user_name} (age {user_age} < {min_age})")
            continue
        
        elif user_age > max_age:
            print(f"stop: {user_name} (age {user_age} > {max_age})")
            break
        
        else:
            print(f"process: {user_name} (age {user_age})")
            valid_users_list.append(user_name)
            current_hobbies = []

            for hobby in user['hobbies']:
                if hobby == 'skip_hobby':
                    print(f"skip_hobby")
                    continue
                current_hobbies.append(hobby)
            user_hobby_dict[user_name] = current_hobbies

    return (valid_users_list, user_hobby_dict)

age_tuple = (18, 40)
processed_list, processed_dict = process_data(user_database, age_tuple)
print("Processed Users")
print(processed_list)
print("Processed Hobbies")
print(processed_dict)
