# Currency Converter
This is a simple implementation of an online currency exchanger.
The application exposes two main endpoints:
    1. get_currencies [GET] : Takes no parameters and returns a list of currencies available
    2. exchange[POST] : Takes a custom exchange object and returns a
 

 ### Running the application
- Make sure that you have Python 3 + and an environment key for the APILayer api
- Clone the repository using the `git clone` command
- Navigate into the project directory
- Activate your virtual environment using the `pipenv shell` command 
- Install the appropriate packages using the `pipenv install` command
- Run the application using the `uvicorn main:app --reload` command
- Navigate to http://127.0.0.1:8000/docs to use the OPENAPI documentation to interact with the endpoints
- Note: The api uses authentication . To login use the username: `johndoe` and the password: `secret2`


### Technologies Used
- Python (FastAPI)
- Other APIs used [APILayer](https://apilayer.com/marketplace/exchangerates_data-api#documentation-tab)

### Areas for further improvements
- Use actual password hashing 
- Use a database to store authentication information

