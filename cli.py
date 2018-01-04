import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import auth
import click

# Fetch the service account key JSON file contents
cred = credentials.Certificate("resources/movey-6713a-firebase-adminsdk-gyujr-e3ff0b1397.json")

# Initialize the app with a service account, granting admin privileges
default_app = firebase_admin.initialize_app(cred, {'databaseURL': 'https://movey-6713a.firebaseio.com/'})
# As an admin, the app has access to read and write all data, regradless of Security Rules
users_db_ref = db.reference('social/users')


@click.command()
def list():
    all_users = users_db_ref.get()
    for uid in all_users:
        if all_users[uid]:
            print(all_users[uid]['email'], uid)

@click.command()
@click.option('--uid', help='by uid')
@click.option('--email', help='by email')
def remove(uid,email):
    if uid: 
        print("Deleting user by uid: ", uid)
        auth.delete_user(uid)
        return
    if email:
        print("Deleting user by email: ", email)
        return


@click.command()
@click.option('--email',prompt="Enter email", help='set email')
@click.option('--name',prompt="Enter full name", help='set full name')
@click.option('--photo',default="none",prompt="Enter profile image link", help='set profile image')
@click.option('--password',prompt="Enter password", help='set password',hide_input=True)
def create(email,name,photo,password):

    if(photo == "none"):
        photo = "https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&cad=rja&uact=8&ved=0ahUKEwi-qp3G677YAhWGYVAKHa3pAVQQjRwIBw&url=https%3A%2F%2Fwww.pexels.com%2Fsearch%2Flove%2F&psig=AOvVaw0v1shBRwjmW00MDnEeqL0O&ust=1515173571706027"
        
    user = auth.create_user(
    email=email,
    email_verified=False,
    password=password,
    display_name=name,
    photo_url=photo,
    disabled=False)
    print ('Sucessfully created new user')

@click.group()
def user():
    pass

user.add_command(list)
user.add_command(remove)
user.add_command(create)


@click.group()
def main():
    pass

main.add_command(user)

if __name__ == '__main__':
    main()










