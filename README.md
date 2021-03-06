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

**Exception: ** If the form is called without valid arguments it redirects to login.djhtml.

## Objective 02
**Description:** This objective displays the users information  on the left side of the web page.  Project03/social/templates/social_base.djhtml is edited to display the user's data using attributes from the UserInfo class such as employment, location, birthday and interests.

**Exception:** If the user has not added information then employment and location will be "Unspecified". Birthday will be "None" and the interest section will be blank.

## Objective 03
**Description:** This feature is used to update the information for the user or the user's password. Account_view function in Project03/social/views.py is edited to render the forms and Project03/social/templates/account.djhtml is used to display the form.

- After changing the password the user will be **directed to the login page** to log in with the new password. 

- The user can update their personal information aswell the user must press save after updating the information.

- **The user must press save for the current attribute they are editing before updating other attributes**. 

- All changes can be seen in the left hand column where the users current information is displayed, the page is reloaded after updating the information. 

- The interests of the user are added to the interest model and displayed as a label on the left column of the web page. The code below shows how the interest is saved and added to the UserInfo object.

```Python
if newInterest:
     userInterest = models.Interest(label=newInterest)
     userInterest.save()
     user_info.interests.add(userInterest)               
     user_info.save()
```
**Exception:** If the password change form is not filled in correctly i.e. if it lacks arguments or the wrong arguments are given, the page will reload and the user will get another chance to fill out the form again. 
