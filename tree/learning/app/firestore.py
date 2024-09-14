from firebase import auth, db
username = 'abcdefg'
email = 'royal@abcd.in'
password = 'abcdefgh'
user_ref = db.collection('users')
query = user_ref.where('email' ,'==', email).stream()
user = None
for user in query:
    print(f'User Data: {user.to_dict()}')
if user:
    print("User already exists")
else:
    print("Enter the data")