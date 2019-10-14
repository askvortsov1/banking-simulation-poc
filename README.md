# banking-simulation-poc

CMPSC 132 Assignment to explore OOP principles via a simulated banking environment in the United States.

Implemented as Flask-powered Restful API.

API Documentation can be found at <https://app.swaggerhub.com/apis-docs/askvortsov1/Banking-Simulation-PoC/1.0.0>


## Running Instructions

### With Docker

`docker-compose up` to start the container

`docker exec -it banking flask create-superuser FIRSTNAME LASTNAME` to create a superuser

### Without Docker

If running without docker, please consider using a virtualenv.

`pip install -r requirements.txt`
`cd src`
`flask db upgrade`
`flask run --host=0.0.0.0`


## Tests

A number of tests have been created in. These tests can be run with the following steps.

1. Make sure all requirements in requirements.txt are installed (use of a virtualenv is recommended).
2. `sh test.sh`

Support for running tests with the docker configuration may be added later.
Unfortunately, I was unable to figure out how to refresh the database between test sessions, so all tests are contained in one pytest test case. I recognize that this is very bad practice, but due to the impending assignment deadline, I'm forced to leave it like this for now. This is a theoretical proof of concept, which isn't used anywhere, so there's no security ramification to this.

## Inaccuracies

I used this project to explore RESTful APIs with Flask. However, it is still a graded assignment with a deadline, so in the interests of time and GPA, the following simplifications were excused. This is also a future to-do list if I want to explore this project further.

- [x] ~~Automated tests should be added~~.

- [ ] API Endpoints should be secured and properly authenticated.

- [ ] Multi-user accounts lack support

- [ ] Loans, debit cards, and credit cards lack support

- [ ] Record Ids should not be sequential

- [x] ~~Getting record information should return a whitelisted subset of attribute and property values~~

- [ ] Lookup options by name should be implemented

- [ ] Basic GIS support for bank branches should be considered

- [ ] Further research should be done into U.S. Banking Law

- [ ] User credit score should be considered in account approval, loan approval, and interest calculations

- [ ] A token-based authentication system should be implemented

- [ ] A validator system for model attributes should be added.
