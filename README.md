# banking-simulation-poc

CMPSC 132 to explore OOP principles via a simulated banking environment in the United States.

Implemented as Flask-powered Restful API.

API Documentation can be found at <https://app.swaggerhub.com/apis-docs/askvortsov1/Banking-Simulation-PoC/1.0.0>


## Running Instructions

`docker-compose up` to start the container

`docker exec -it banking flask create-superuser FIRSTNAME LASTNAME` to create a superuser


## Inaccuracies

I used this project to explore RESTful APIs with Flask. However, it is still a graded assignment with a deadline, so in the interests of time and GPA, the following simplifications were excused. This is also a future to-do list if I want to explore this project further.

- [ ] Automated tests should be added.

- [ ] API Endpoints should be secured and properly authenticated.

- [ ] Multi-user accounts lack support

- [ ] Loans, debit cards, and credit cards lack support

- [ ] Record Ids should not be sequential

- [ ] Getting record information should return a whitelisted sbset of attribute and property values

- [ ] Lookup options by name should be implemented

- [ ] Basic GIS support for bank branches should be considered

- [ ] Further research should be done into U.S. Banking Law

- [ ] User credit score should be considered in account approval, loan approval, and interest calculations

- [ ] A token-based authentication system should be implemented

- [ ] The error message system should be redone
