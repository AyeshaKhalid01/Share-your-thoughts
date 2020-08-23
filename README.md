# Share-your-thoughts
Created Django, Anaconda, JavaScript and HTML

## Usage
- Install Conda package by clicking [Install Conda](https://docs.anaconda.com/anaconda/install/)
- Create conda environment with ``` conda create -n djangoenv python=3.7 ``` 
- Activate the environment with  ```conda activate djangoenv```

### Running 
- Run locally with ```python manage.py runserver localhost:8000 ```
- Run on mac1xa3.ca server with ```python manage.py runserver localhost:10055```
- Access the website by going to [https://mac1xa3.ca/e/khalia34](https://mac1xa3.ca/e/khalia34) **make sure the conda enviroment is activated**

## Objective 01 
**Description:** The purpose of this is to build signup form for new users to create an account. This done by editing the function signup_view in Project03/login/views.py to render the signup form. 

- The code below checks if the form is valid, if True it will create a UserInfo object and store the username and password.
```Python
 if form.is_valid():
          username = form.cleaned_data.get('username')
          password = form.cleaned_data.get('password1')
          models.UserInfo.objects.create_user_info(username=username,password=password)
```
Project03/login/templates/signup.djhtml is also edited to display the form. If an account is successfully created the user will be taken to the messages page.

**Exception:** If the form is called without valid arguments it redirects to login.djhtml.

## Objective 02
**Description:** This objective displays the users information  on the left side of the web page.  Project03/social/templates/social_base.djhtml is edited to display the user's data using attributes from the UserInfo class such as employment, location, birthday and interests.

**Exception:** If the user has not added information then employment and location will be "Unspecified". Birthday will be "None" and the interest section will be blank.

