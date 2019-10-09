# banking-simulation-poc

CMPSC 132 to explore OOP principles via a simulated banking environment in the United States.
Implemented as Flask-powered Restful API.

API Documentation can be found at <https://app.swaggerhub.com/apis-docs/askvortsov1/Banking-Simulation-PoC/1.0.0>


## Running Instructions

`docker-compose up` to start the container

`docker exec -it banking flask create-superuser FIRSTNAME LASTNAME` to create a superuser


## Inaccuracies

I used this project to explore RESTful APIs with Flask. However, it is still a graded assignment with a deadline, so in the interests of time and GPA, the following simplifications were excused. This is also a future to-do list if I want to explore this project further.

[o] Automated tests should be added.
[o] API Endpoints should be secured and properly authenticated.
[o] Multi-user accounts lack support
[o] Loans, debit cards, and credit cards lack support
[o] Record Ids should not be sequential
[o] Getting record information should return a whitelisted subset of attribute and property values
[o] Lookup options by name should be implemented
[o] Basic GIS support for bank branches should be considered
[o] Further research should be done into U.S. Banking Law
[o] User credit score should be considered in account approval, loan approval, and interest calculations
[o] A token-based authentication system should be implemented
[o] The error message system should be redone
