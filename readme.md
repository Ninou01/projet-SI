# Clinic - Medical System Management

Clinic is a web-based medical system management application designed for efficient management of patient appointments, medical staff, and related tasks. Below are instructions for installing the application and an overview of its functionalities.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/Clinic.git
    ```

2. Create and activate a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install project dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Apply database migrations:

    ```bash
    python manage.py migrate
    ```

5. Create a superuser account for admin access:

    ```bash
    python manage.py createsuperuser
    ```

6. Run the development server:

    ```bash
    python manage.py runserver
    ```

7. Access the application in your web browser at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Accessing the Application

Use the following credentials to access different roles in the application:

- Admin:
  - Email: admin@gmail.com
  - Password: 123456

- Patient:
  - Email: angela07@example.org
  - Password: Thisisacomplexpassword1

- Médecin (Doctor):
  - Email: medecin40@exemple.com
  - Password: Thisisacomplexpassword1

## Project Overview

1. **Login Dashboard:**
   - Users are required to log in to access the system's functionalities.

2. **Admin Functionality:**
   - Full control over the system, including patient, médecin, salle, tâche, and rendez-vous management.
   - Modification of rendezvous is allowed only if the status is not 'terminé'.
   - Creating a new consultation automatically sets the status of its associated rendez-vous to 'terminé'.
   - Admin cannot delete consultations.

3. **Médecin Functionality:**
   - Homepage with a navbar providing access to view médecins, consultations, rendez-vous, and patients.
   - Médecin can only create consultations and modify their own information.

4. **Patient Functionality:**
   - Patients can modify their own information and view médecins, consultations, rendez-vous, services, and salles.

5. **Services Management:**
   - Services are pre-existing in the system.
   - The admin can modify their chef.

6. **Logout:**
   - Users are redirected to the login page upon logout or creation of a new session.

Feel free to explore and make use of the functionalities provided by the Clinic application. If you encounter any issues or have questions, refer to the documentation or reach out to the application administrator.