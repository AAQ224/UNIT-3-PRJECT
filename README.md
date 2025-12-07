# EduGate – Online Courses Management Platform

## Project Description
EduGate is an online learning management system (LMS) built using Django. The system supports multiple user roles, including administrators, teachers, students, and parents. The platform allows teachers to create lessons, assignments, and quizzes; students to enroll and learn; parents to track their children's progress; and administrators to manage the entire platform. EduGate features a sleek architecture, a responsive user interface, and modern best practices using Django templates, static files, and media processing.

## Main Features

### 1. Authentication & Roles
- Register, login, logout with Django auth.
- Profile model storing **full name**, **national ID**, and **role** (admin / teacher / student / parent).
- Role-based dashboard:
  - **Admin dashboard** with management tools.
  - **Teacher dashboard** showing assigned classes & subjects.
  - **Student dashboard** showing class enrollment and pending homework/quizzes.
  - **Parent dashboard** listing linked children and quick access to their grades.

### 2. User & Relations Management (Admin)
- Create new users from the admin dashboard (with role + profile info).
- Manage users screen with tabs:
  - **Admins**, **Teachers**, **Students**, **Parents** – each in a separate table.
- Edit & delete users from the Manage Users page.
- Link parents to multiple children using a dedicated **“Link Parent to Children”** page with multi-select.
- Manage all parent–child relations in **Manage Parent–Children Links** (table + delete action).

### 3. Classes, Subjects & Enrollment (courses app)
- **SchoolClass** model to represent school classes (e.g. “Grade 3 – A”).
- **Subject** model (e.g. Math, Science).
- **ClassSubject** model to attach a Subject to a SchoolClass and assign a Teacher.
- Admin tools:
  - Manage school classes (create / update / delete).
  - Manage subjects.
  - Manage subject–class–teacher assignments.
- **StudentClassEnrollment**: enroll multiple students in a class using a multi-select widget (with search and tags).

### 4. Lessons, Homework & Quizzes (progress app)
- Teachers can create:
  - **Lessons** for a class subject.
  - **Homework** with due dates.
  - **Quizzes** with questions & choices and total marks.
- Students:
  - View available quizzes and homework for their subjects.
  - Submit quiz attempts and homework solutions.
- Teachers:
  - View all submissions.
  - Grade homework and quizzes and store marks.

### 5. Student & Parent Progress Views
- **Student grade page**:
  - Shows homework and quiz grades grouped by subject.
- **Parent child grades page**:
  - Parent chooses one of their linked children and sees homework & quiz grades.
- Dashboards show counts of **pending homework** and **pending quizzes** for students.

### 6. Announcements & Home Page (main app)
- Public **home page** explaining EduGate and main platform features.
- **School announcements** CRUD for admins:
  - List of announcements with cards.
  - Detail page and delete confirmation.
- Default placeholder image for announcements when no image is uploaded.

### 7. UI & Frontend
- Built with **Bootstrap 5** and Font Awesome icons.
- Shared layout in `templates/base.html`:
  - Top navbar (Home, Dashboard, auth buttons).
  - Global messages area using Django messages framework.
- Custom styling in `static/css/style.css`.
- Multi-select tags for forms using the **multi-select-tag** JS library.

### 8. Security & Environment Variables
- Sensitive settings moved to `.env` and loaded with **python-dotenv**:
  - `SECRET_KEY`
  - `DEBUG`
  - Email settings used for password reset (`EMAIL_HOST`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, etc.).
- `.env` is excluded from Git via `.gitignore`.


## User Stories for the EduGate Platform

### Student
- As a Student, I can register and log in so that I can access my dashboard.
- As a Student, I can see my enrolled **class and subjects** so that I know what I am studying this term.
- As a Student, I can view lessons, homework, and quizzes for each subject so that I can follow the teacher’s materials.
- As a Student, I can **submit homework** so that teachers can grade my work.
- As a Student, I can **take quizzes online** so that my grades are recorded in the system.
- As a Student, I can view my **homework and quiz grades** so I can track my progress and performance.
- As a Student, I can see how many **pending homework and quizzes** I still have to complete.

### Teacher
- As a Teacher, I can see the **classes and subjects** assigned to me so that I know which students I teach.
- As a Teacher, I can create and edit **lessons** for my class subjects so that I can share learning content with students.
- As a Teacher, I can create **homework** with due dates so that students can submit their answers on time.
- As a Teacher, I can create **quizzes and questions** so that I can assess student understanding.
- As a Teacher, I can view **student submissions** (homework and quizzes) so that I can grade them.
- As a Teacher, I can enter **grades and feedback** so that students and parents can see the results.

### Parent
- As a Parent, I can log in and see a list of my **linked children** so that I can choose which child to follow.
- As a Parent, I can view each child’s **homework and quiz grades** so that I can monitor their academic progress.
- As a Parent, I can check if my child has **missing or low grades** so that I can support them.

### Admin
- As an Admin, I can **create new users** (students, teachers, parents, admins) from the dashboard so that the school can onboard users easily.
- As an Admin, I can **manage users** (view, edit, delete) so that the platform data stays clean and up to date.
- As an Admin, I can manage **school classes and subjects**, and assign a **teacher to each class subject**.
- As an Admin, I can **enroll students** into a class using a multi-select tool so that many students can be added quickly.
- As an Admin, I can **link parents to children** and manage these relations so that parents can see the correct student data.
- As an Admin, I can create and manage **school announcements** so that important news appears on the home page.
- As an Admin, I can access an **administrative dashboard** that centralizes all management tools in one place.



## UML Diagram :
<img width="1889" height="1530" alt="UML_Class_Diagram2" src="https://github.com/user-attachments/assets/68f4e9a5-b9bf-446a-9a9b-1a711edc58e6" />

## Wireframes :
<img width="1213" height="863" alt="Parent_Dashboard" src="https://github.com/user-attachments/assets/f8b74dea-984c-4eff-96c4-223bdd021e89" />
<img width="1214" height="864" alt="Student_Dashboard" src="https://github.com/user-attachments/assets/c66dbf58-4306-4555-ad2a-d5935b943790" />
<img width="1215" height="866" alt="Teacher_Dashboard" src="https://github.com/user-attachments/assets/78afb644-a4e0-4713-85dc-8fba5e66cad3" />
<img width="1214" height="865" alt="Admin" src="https://github.com/user-attachments/assets/5665828f-a61f-4939-ba87-6290566743e2" />
<img width="1051" height="748" alt="Home" src="https://github.com/user-attachments/assets/f70dcfe9-19e8-473c-b990-cb80bb8566d9" />
