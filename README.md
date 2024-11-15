

<br />
<div align="center">
  <a href="https://github.com/raihanachmad8/fest-ticketing-backend">
    <img src="./public/assets/images/fest-ticketing-logo.png" alt="Logo" height="80">
  </a>

  <h3 align="center">Fest Ticketing App</h3>

  <p align="center">
    Welcome to the Fest Ticketing App! This backend project aims to streamline the process of ticket sales and management for events, providing features for attendees and organizers.
    <br />
    <a href="https://github.com/raihanachmad8/fest-ticketing-backend"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://festticketingapp.cloud">View Demo</a>
    ·
    <a href="https://github.com/raihanachmad8/fest-ticketing-backend/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/raihanachmad8/fest-ticketing-backend/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#features">Features</a></li>
    <li><a href="#built-with">Built With</a></li>
    <li><a href="#getting-started">Getting Started</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
<h2 id="about-the-project">💡 About The Project</h2>

<!-- [![Product Name Screen Shot](public/assets/images/homescreen-screenshot.png)](public/assets/images/homescreen-screenshot.png) -->

The Fest Ticketing App is designed to facilitate ticket sales and management for various events. This backend application handles ticket bookings, user authentication, event creation, and payment processing, ensuring a seamless experience for both attendees and organizers.

### Features

The Fest Ticketing App provides the following features:
- **User Authentication**: Secure login and registration for users.
- **Event Management**: Organizers can create, update, and delete events easily.
- **Ticket Sales**: Users can browse events and purchase tickets through a straightforward interface.
- **Payment Processing**: Integration with payment gateways for secure transactions.
- **Real-Time Notifications**: Send updates and confirmations via Firebase Cloud Messaging.
- **Analytics Dashboard**: Organizers can view sales and attendance statistics.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

This project is built using:

* [![FastAPI][FastAPI.com]][FastAPI-url]
* [![MongoDB][MongoDB.com]][MongoDB-url]
* [![Alembic][Alembic.com]][Alembic-url]
* [![Firebase][Firebase.com]][Firebase-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started

To set up your backend project locally, follow these steps.

### Prerequisites

You will need to install the following:

- **[Git](https://git-scm.com/downloads)**
- **[GitHub](https://github.com)**
- **[Python 3.8+](https://www.python.org/downloads/)**
- **[Node.js](https://nodejs.org/en/download/current)**
- **[MongoDB](https://www.mongodb.com/try/download/community)**
- **[Postman](https://www.postman.com/downloads/)**
- **[Text Editor](https://code.visualstudio.com/)**

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/raihanachmad8/ngefastapi
    ```

2. Navigate to the project directory:

    ```bash
    cd fest-ticketing-backend
    ```

3. Set up a virtual environment (optional but recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

4. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

5. Set up MongoDB and create a database named `fest_ticketing`.

6. Configure your environment variables in a `.env` file, copying from `.env.example`:

    ```bash
    cp .env.example .env
    ```

7. Run the Alembic migrations to set up your database schema:

    ```bash
    alembic upgrade head
    ```

8. Start the FastAPI application:

    ```bash
    uvicorn app.main:app --reload
    ```



<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Running with Docker

Docker provides a simple way to set up and run the application. Follow the steps below to choose the option that best fits your needs:

#### Prerequisites

1. Ensure **Docker** and **Docker Compose** are installed on your machine.  
   - [Install Docker](https://docs.docker.com/get-docker/)
   - [Install Docker Compose](https://docs.docker.com/compose/install/)

2. Verify Docker and Docker Compose are correctly installed by running:

    ```bash
    docker --version
    docker-compose --version
    ```

3. Create a custom Docker network for the application:

    ```bash
    docker network create app-network
    ```

#### Option 1: Run Everything Together

This option starts all services (application, database, and any additional components) defined in the main `docker-compose.yml` file.

1. Build and start all services:

    ```bash
    docker compose up -d --build
    ```

2. Access the application in your browser at:

    - **API**: [http://localhost:80](http://localhost:80)  
    - **API Docs**: [http://localhost:80/docs](http://localhost:80/docs)

3. Stop the containers when you're done:

    ```bash
    docker compose down
    ```

---

#### Option 2: Run Only the Application Services

Use this option if you want to run just the application without the database. This is useful if the database is already hosted elsewhere.

1. Build and start the application services:

    ```bash
    docker compose -f "docker-compose-app.yml" up -d --build
    ```

2. Access the application at the same endpoints as above:

    - **API**: [http://localhost:80](http://localhost:80)  
    - **API Docs**: [http://localhost:80/docs](http://localhost:80/docs)

3. Stop the containers:

    ```bash
    docker compose -f "docker-compose-app.yml" down
    ```

---

#### Option 3: Run Database and Application Separately

This option gives you more control, allowing you to start the database and the application independently.

1. Start the database container using `docker-compose-db.yml`:

    ```bash
    docker compose -f "docker-compose-db.yml" up -d --build
    ```

2. Verify that the database container is running:

    ```bash
    docker ps
    ```

3. Start the application container:

    ```bash
    docker compose -f "docker-compose-app.yml" up -d --build
    ```

4. Access the application:

    - **API**: [http://localhost:80](http://localhost:80)  
    - **API Docs**: [http://localhost:80/docs](http://localhost:80/docs)

5. Stop the containers:

    ```bash
    docker compose -f "docker-compose-app.yml" down
    docker compose -f "docker-compose-db.yml" down
    ```

---

#### Notes

- **Custom Network**: The `app-network` is used to connect the app and database containers. Ensure this network exists before running the commands.
- **Environment Variables**: Make sure the `.env` file contains the correct environment variables for your database and application.

By following these steps, you can choose the Docker setup that works best for your project!


<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Usage

Access the application in your browser at `http://localhost:8000`.

You can also interact with the API documentation generated by FastAPI at `http://localhost:8000/docs`.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/NewFeature`)
3. Commit your Changes (`git commit -m 'Add some NewFeature'`)
4. Push to the Branch (`git push origin feature/NewFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

[FastAPI.com]: https://img.shields.io/badge/FastAPI-005571?logo=fastapi
[FastAPI-url]: https://fastapi.tiangolo.com/
[MongoDB.com]: https://img.shields.io/badge/MongoDB-47A248?logo=mongodb
[MongoDB-url]: https://www.mongodb.com/
[Alembic.com]: https://img.shields.io/badge/Alembic-FFB6C1?logo=python
[Alembic-url]: https://alembic.sqlalchemy.org/
[Firebase.com]: https://img.shields.io/badge/Firebase-FFCA28?logo=firebase
[Firebase-url]: https://firebase.google.com/