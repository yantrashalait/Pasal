# Pasal
This is a Django peojct that is used to obtain RESTful APIs for the Pasal(now Bhumija) app.

## Setup
### 1. Clone the repo:
`git clone git@github.com:yantrashalait/Pasal.git`

### 2. Create a virtualenvironment in your machine specifying the python version. You can use virtualenv for this.
`virtualenv <path_to_virtual_environment> -p python3`

### 3. Install the requirements:
Activate the virtual environment `activate <path_to_virtual_environment>/bin/activate`.

Install all the requirements listed in **requirements.txt** as:
`pip install -r requirements.txt`

### 4. Manage settings:
Copy the **local_settings_sample.py** file to **local_settings.py** in the same location. Make proper changes to the **local_settings.py** file as:

a. ALLOWED_HOSTS

b. DATABASES

c. STATIC FILES

Make sure you follow the instructions given the in the **local_settings_sample.py** file to edit the **local_settings.py** file.
