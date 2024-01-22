# написати функцію на будь-якій мові програмування, яка приймає два об'єкта 
# та перевіряє чи вони однакові (всі властивості є однаковими).
# завдання з зірочкою - функція може рекурсивно перевірити вкладені об'єкти.


obj_1 = {
    'users': [
        {'name': 'John', 'age': 30, 'addresses': {'home': '123 Main St', 'work': '456 Business Ave'}},
        {'name': 'Alice', 'age': 25, 'addresses': {'home': '789 Residential Rd', 'work': '101 Corporate Blvd'}}
    ],
    'departments': {
        'engineering': {'head': 'Bob', 'team': ['Alex', 'Charlie', 'Eva']},
        'marketing': {'head': 'David', 'team': ['Frank', 'Grace', 'Helen']}
    },
    'projects': [
        {'name': 'Project_A', 'status': 'in-progress', 'team': ['John', 'Alice']},
        {'name': 'Project_B', 'status': 'completed', 'team': ['Bob', 'Charlie']}
    ]
}

obj_2 = {
    'departments': {
        'engineering': {'head': 'Bob', 'team': ['Alex', 'Charlie', 'Eva']},
        'marketing': {'head': 'David', 'team': ['Frank', 'Grace', 'Helen']}
    },
    'users': [
        {'name': 'John', 'age': 30, 'addresses': {'home': '123 Main St', 'work': '456 Business Ave'}},
        {'name': 'Alice', 'age': 25, 'addresses': {'home': '789 Residential Rd', 'work': '101 Corporate Blvd'}}
    ],
    'projects': [
        {'name': 'Project_B', 'status': 'completed', 'team': ['Bob', 'Charlie']},
        {'name': 'Project_A', 'status': 'in-progress', 'team': ['John', 'Alice']}
    ]
}

obj_3 = {
    'companies': {
        'company_A': {'location': 'City_X', 'employees': ['John', 'Alice', 'Bob']},
        'company_B': {'location': 'City_Y', 'employees': ['Charlie', 'David', 'Eva']}
    },
    'events': [
        {'name': 'Event_X', 'date': '2023-05-15', 'participants': ['Grace', 'Helen']},
        {'name': 'Event_Y', 'date': '2023-06-20', 'participants': ['Frank', 'Eva']}
    ],
    'data_centers': {
        'DC_1': {'location': 'City_Z', 'servers': {'main': 100, 'backup': 50}},
        'DC_2': {'location': 'City_W', 'servers': {'main': 80, 'backup': 40}}
    }
}


def main():
    ...


if __name__ == '__main__':
    main()