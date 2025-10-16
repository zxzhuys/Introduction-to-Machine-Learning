original = {
    'name': 'ZZX',
    'id': '000000',
    'courses': {
        'machine learning': {
            'schedule': 'Thursday',
            'grades': [80, 90, 100]
        },
        'energy system': {
            'schedule': 'Friday',
            'grades': [85, 95, 100]
        }
    }
}

# Shallow Copy
copy = original.copy()

print("--- Original Grades ---")
print("Original Machine Learning Grades:", original['courses']['machine learning']['grades'])
print("Copy Machine Learning Grades:", copy['courses']['machine learning']['grades'])
print("\n")

print("--- Add a new grade '99' ---")
copy['courses']['machine learning']['grades'].append(99)
print("\n")

# Results
print("--- Results ---")
print("Original Machine Learning Grades:", original['courses']['machine learning']['grades'])
print("Copy Machine Learning Grades:", copy['courses']['machine learning']['grades'])
