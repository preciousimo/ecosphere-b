# **EcoSphere: A Community-Driven Sustainability Platform**

EcoSphere is a sustainability-focused platform that helps communities promote eco-friendly practices such as resource sharing, waste reduction, recycling, and sustainable energy management. By integrating smart devices and data tracking, EcoSphere enables individuals and communities to reduce their environmental footprint and engage in collective sustainability goals.

## **Table of Contents**

1. [Features](#features)
3. [Installation and Setup](#installation-and-setup)
4. [API Documentation](#api-documentation)
5. [Contribution Guidelines](#contribution-guidelines)
6. [License](#license)

---


- **Resource Sharing & Booking**: Share and book eco-friendly resources within the community.
- **Waste Reduction & Recycling**: Track waste, locate recycling centers, participate in eco-challenges, and view community leaderboards.
- **Sustainable Energy Dashboard**: Integrate smart home devices, monitor energy usage, receive personalized energy-saving recommendations, and contribute to community energy goals.
- **Community Engagement**: Create and track sustainability challenges, view leaderboards, and foster a sense of shared responsibility for the environment.


## **Installation and Setup**

### **Prerequisites**

Ensure you have the following installed:

- **Python 3.8+**
- **Django 4.0+**
- **PostgreSQL** (or any other preferred database)
- **Docker** (optional, for containerized deployment)

### **Step-by-Step Setup**

1. **Clone the repository:**
   ```bash
   git clone https://github.com/preciousimo/ecosphere-b.git
   cd ecosphere

2. **Set up a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

3. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt

4. **Configure the .env file:**

   Copy the .env.example file to .env and fill in the necessary environment variables such as database credentials and secret keys.
   ```bash
   cp .env.example .env

4. **Set up the database:**
   Ensure your PostgreSQL database is running, then run:
   ```bash
   python manage.py makemigrations
   python manage.py migrate


## **API Documentation**

EcoSphere includes a robust API for managing resources, energy tracking, waste reduction, and community engagement. The API is built using Django REST Framework.

### **Example API Endpoints:**

- **GET `/api/resources/`** – Retrieve a list of resources.
- **POST `/api/waste-entries/`** – Submit a new waste tracking entry.
- **GET `/api/energy-usage/`** – View energy consumption data for connected devices.

You can explore the API using tools like Postman or the built-in Django REST Framework browsable API at `http://localhost:8000/api/`.

For detailed API documentation, check out the `api/docs/` endpoint.


## **Contribution Guidelines**

We welcome contributions from the community! If you'd like to contribute to EcoSphere, please follow these steps:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature-name`.
3. Commit your changes: `git commit -m 'Add new feature'`.
4. Push to the branch: `git push origin feature/your-feature-name`.
5. Open a Pull Request.

Please ensure your code adheres to the project's style guidelines and passes all tests.


## **License**

EcoSphere is licensed under the MIT License. See the LICENSE file for more details.
