# my_fintech_tools

## Description

This is a Django shell application that helps to collect funds from a user and monitor transaction completion using the MTN MoMo API. This project uses two publicly available utilities that are build on top of the MTN MoMo API.

- The mtnmomo library to make HTTP calls to the MoMo API
- The mtnmomo command line tool to help with generation of keys. This tool abstracts a lot of the pain involved in getting keys straight from the MoMo API.
  Both these utilities are available on [PyLib](https://pypi.org/project/mtnmomo/) and are open on [github](https://github.com/sparkplug/momoapi-python)

## Setting up the code

- Clone the source code on github
- Install the project dependencies using pip - `pip install -r requirements.txt`
- Install `redis` on your host system. This is not a python package and will have to be installed separately.
- I would advice you create a virtual environment for this project so you do not interfere with your local python setup. For more on virtual environments, check [this](https://virtualenv.pypa.io/en/latest/) out.

## Setting up to use the MOMO API

- This tools assumes that you have an MTN MoMo developer account have subscribed to the Collections product and gotten a Primary and Secondary Key.
- Use your Primary Key to generate your `User ID` and `API Secret` which you'll use to make requests to the MoMo API. Generate these values using this command on your terminal - `mtmmomo --provider <your-app-domain> --key <your-primary-key>`. This command line tool will output a JSON string which contains your `User ID` and `API Secret`. We are now ready to interact with the MoMo API sandbox.
- Export 3 key variables to the virtual environment (if you are using one) - `COLLECTION_USER_ID`, `COLLECTION_API_SECRET` and `COLLECTION_PRIMARY_KEY`. The values of these variables have been mentioned in the previous points.
- Lastly we need to start two processes in two terminals (with the virtual env activated, if you are using one):

  - The celery worker to handle asynchronous tasks - `celery -A my_fintech_tools worker -l info`
  - The celery beat process to handle periodic tasks(to check on the status of transactions) - `celery -A my_fintech_tools beat -l info`

  Both these commands should be run in the project folder. On both terminals, remember to export the 3 environment variables as well.

## How to use it

- Open another terminal (with the virtual env activated, if you are using one) and enter `python manage.py shell`. This will open a Python interactive shell.
- On the shell, import the model using this import statement `from my_momo_app.models import MomoRequest`
- You can then create your new request e.g `mr = MomoRequest(mobile_no="256772123456", amount="1000", external_id="123456789", payee_note="OK", payee_message="Purchase of python library", currency="EUR")`. Please note that the MTN Sandbox which we'd be using in this case currently only accepts Euros(EUR) as currency.
- Finally, save your request - `mr.save()`
- And that's it! The rest happens in the background. You can check your SQLite DB for the status of your request.
