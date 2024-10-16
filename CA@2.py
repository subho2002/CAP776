import csv
import re
import requests

csv_file = 'RegNo.csv'
NASA_API_KEY = 'NuRGzcrLL95ZATFTjSOYvN1J0jhhq2yZDPWyEudY'



def read_user():
    users = {}
    try:
        with open(csv_file, mode='r', newline='') as file:
            f = csv.DictReader(file)
            for row in f:
                if 'Email' in row and 'Password' in row and 'Favorite Question' in row and 'User Name' in row:
                    users[row['Email']] = {
                        'User Name': row['User Name'],
                        'Password': row['Password'],
                        'security_question': row['Favorite Question']
                    }
                else:
                    print("Warning: Missing fields in CSV row.")
    except FileNotFoundError:
        print("User data file not found.")
    return users



def login(users):
    attempts = 1
    while attempts < 6:
        email = input("Enter your registered email id: ")
        password = input("Enter your password: ")

        if email in users and users[email]['Password'] == password:
            print("Login successful!")
            return True
        else:
            print("Invalid email or password.")
            attempts += 1
    
    print("Too many failed attempts. Please try again later.")
    return False


def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_valid_password(password):
    return (len(password) >= 8 and
            any(char in '!@#$%^&*()_+' for char in password))


def register():
    userName = input("Enter User Name: ")
    email = input("Enter the Email address: ")
    if not is_valid_email(email):
        print("Invalid email format.")
        return
    password = input("Enter the Password: ")
    if not is_valid_password(password):
        print("Password must be at least 8 characters long and contain a special character.")
        return
    favQ = input("Where Are You From?: ")

    regNo = [userName, email, password, favQ]

    with open(csv_file, mode='a', newline='') as file:
        f = csv.writer(file)

        if file.tell() == 0:
            f.writerow(['User Name', 'Email', 'Password', 'Favorite Question'])

        f.writerow(regNo)

    print("\nSuccessfully Registered.\n")



def reset_password(users):
    email = input("Enter your registered email: ")
    if email in users:
        print(f"Security question: Where are you from?")
        answer = input("Answer the security question: ")
        
        new_password = input("Enter your new password: ")
        if new_password:  
            users[email]['Password'] = new_password
            print("Password updated successfully.")
            
            update_csv(users)
        else:
            print("Password does not meet requirements.")
    else:
        print("Email not found.")



def update_csv(users):
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['User Name', 'Email', 'Password', 'Favorite Question'])
        for email, data in users.items():
            writer.writerow([data['User Name'], email, data['Password'], data['security_question']])



def fetch_nasa_data():
    response = requests.get(f"https://api.nasa.gov/neo/rest/v1/feed?api_key={NASA_API_KEY}")
    if response.status_code == 200:
        data = response.json()
        for date, neos in data['near_earth_objects'].items():
            for neo in neos:
                print(f"Name: {neo['name']}")
                print(f"Close Approach Date: {neo['close_approach_data'][0]['close_approach_date']}")
                print(f"Estimated Diameter: {neo['estimated_diameter']['meters']['estimated_diameter_max']} m")
                print(f"Velocity: {neo['close_approach_data'][0]['relative_velocity']['kilometers_per_hour']} km/h")
                print(f"Miss Distance: {neo['close_approach_data'][0]['miss_distance']['kilometers']} km")
                print(f"Hazardous: {neo['is_potentially_hazardous_asteroid']}")
                print("-" * 40)
    else:
        print("Error fetching data from NASA API.")





print("NASA Data Console Screen with Login and API Integration\n")
users = read_user()  

while True:
    print(f'''Please Select Option:
    1) Login
    2) Register
    3) Forgot Password
    4) Exit\n''')
    value = int(input("Enter the option: "))
    
    match value:
        case 1:
            login(users)
            fetch_nasa_data()
        case 2:
            register()
            users = read_user()  
        case 3:
            reset_password(users)
        case 4:
            break
        case _:
            print("\nPlease choose a valid option!\n")