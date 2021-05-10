# imagipy

Imagipy is a Flask app for an image repository system 
that allows users to make private or public uploads which are 
securely stored in a sqlite database.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the dependencies.

```bash
pip install flask 
pip install flask-sqlalchemy 
pip install flask-login
pip install sqlalchemy
```

## Running the App

Run this command on your terminal

```python
python -m flask run
```

the app is now running on http://localhost:5000/

## How does the Imagipy App work?

1. **Login Page**:

![login page](https://i.imgur.com/yr7VXPF.png)

- click on "Register Here" to create a new user

2. **Register Page**:

![register page](https://i.imgur.com/yPHpuns.png)

- fill in your email and password and click submit. 
- You will be redirected to the login page after the user is registered

3. **Login User**:

![login_user](https://i.imgur.com/RSRstgc.png)

- enter your login details and click submit and now you'll be redirected to the home page

4. **Home page**:

![Home](https://i.imgur.com/PxcPob8.png)

- Here you'll be able to choose image(s) to upload

5. **Select Images**:

![Select](https://i.imgur.com/0pNqjyd.png)

- Select the images you want to upload

6. **Upload Images**:

![Upload](https://i.imgur.com/Zn47uEz.png)

- By default the uploads are public, but you have the option to make private uploads.
- If you select the private option the image(s) will only be visible to the user that is making the upload.
- To see the image(s) click Show Pictures

7. **Image Gallery**:

![Gallery](https://i.imgur.com/H1uPdda.png)

- Here you can view all public uploads by any user, but only your private uploads. Private uploads by other users won't be visible
- To delete any of your uploads click the Delete image button on the top right corner.

8. **Delete Image**:

![Delete](https://i.imgur.com/3hqPY2R.png)

- In the delete images tab you'll only be able see and delete your uploads. This is to ensure access control. 
- To delete any image click the delete button directly below the image.
- To delete all of your uploads at once click the red Delete All button on the top.


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)