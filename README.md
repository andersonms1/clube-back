# Task Manager application with authentication + redis cache with jwt token

* The application allows users to perform login/logout operations
* Password reset functionality was implemented and users can execute CRUD operations (create, read, update, and delete) on tasks. Each task is associated with a user.
* The frontend and backend were developed separately, and communication between them is handled through a RESTful API.
* User authentication was implemented using JWT.
* The backend uses a secret_key stored in an environment variable to sign and verify JWT tokens.
* The key was configured with a TTL of 5 minutes.

## Project setup

1. Clone the `backend`:

`git clone https://github.com/andersonms1/clube-back.git`

2. Clone the frontend repository:
Navigate to the cloned project folder:

`cd club-back`

And create the frontend application repository:

`git clone https://github.com/andersonms1/clube-front.git`

- The project structure follows this pattern:
```
.
├── back
├── clube-front
├── docker-compose.yml
├── Makefile
└── README.md
```

3. Return to the project root. Edit the `.env.example` file, rename it to `.env` and add the necessary fields.

4. Build Docker and run the application:
`docker compose build`

5. Execute the application. The `docker-compose` is responsible for starting the necessary services for the project architecture: `redis` and `mongo`.
Access the application in your browser at https://localhost:80

![plot](Mockup.png)
