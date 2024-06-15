# CollabNext_alpha

## Refer to below for steps to build the app

https://techcommunity.microsoft.com/t5/apps-on-azure-blog/deploying-react-spa-and-python-backend-together-on-the-same/ba-p/4095567


## Building React.js/Flask application locally:

1. Python setup<br>
`python3 -m venv .venv`<br>
`source .venv/bin/activate`<br>
`pip install -r requirements.txt`<br>

2. React build
`npm run build`

    The build folder is ready to be deployed.
    You may serve it with a static server:

    `npm install -g serve`<br>
    `serve -s build`
 
3. Run locally 
 To run the Flask application locally, you need to execute the Python script containing your Flask application 

   `python app.py`



