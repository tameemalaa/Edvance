# Functional Requirements Document Template for Learning Management System Graduation Project

## Introduction

- The purpose and scope of the document: Outline the non-functional requirements for the Learning Management System (LMS) graduation project.

 ## 1. User Management 

- ### User registration page 
    - The user registration page must contain fields for email address , password , first name , last name and other required information. 
    - The user registration page must support sign up as a student , teacher or teacher assistant. 
    - The user registration page must validate input and provide clear error messages on invalid input.
    - The user authentication system should enforce strong password policies, such as requiring minimum password length and complexity. 
    - On submission the user registration information must be stored securely in the database. 
    - The system should encrypt sensitive user information, such as passwords and personal data, both in transit and at rest.
 

- ### User authentication system
    - The user authentication system must verify the user's credentials against stored information in the database when the user attempts to sign in. 
    - The user authentication system must securely store user session information and provide appropriate error messages for invalid login attempts.
    - The system should log authentication events and provide audit trails for security and compliance purposes
    - When multiple login attempts fail within a short period of time, the IP address attempting to sign in will be temporarily blocked. 
    - The system should protect against common attacks, such as brute-force attacks and credential stuffing, by implementing appropriate security measures, such as rate limiting and account lockout.
    - The user authentication system must automatically log out inactive users after a specified period of time.
- ### Password reset functionality
    - The password reset page must prompt users to enter their email address and provide a confirmation message upon submission.
    - The password reset system must securely generate and send a unique password reset link to the user's email address.
    - The password reset link must be valid for a limited period of time and must prompt the user to enter a new password upon clicking the link.

- ### User management interface 
    - The user management interface must allow users to edit their profile data.
    - The user management interface must allow teachers to assign roles and permissions to users.

## 2.Course Management

- ### Course creation interface
  - The course creation interface should allow teachers to enter the course title, description, and other relevant information. 
  - The interface should provide options for setting course grading policies, and assessment methods

- ### Course enrollment and access
  - The system should allow teachers to add students in their courses.  
  - The system should allow students to enroll in courses using join codes. 
  - The system should provide access to course materials based on user's role and enrollment status.
  - The system should allow teachers to manage access permission to course materials.
  - The system should allow users to archive courses.  

- ### Course materials management 
  - The system must provide an interface for teachers to upload and manage course materials, including syllabus, lecture notes, videos, audio files, assignments, and readings.
  - The system should provide a course materials repository to store and manage course materials
  - The system should allow the teachers to upload new files and edit existing content in the course materials repository. 
  - The system should allow teachers to organize course materials into categories to make them easier to find.
  - The system should ensure the security and confidentiality of course materials by implementing appropriate access controls and user permissions.
  - The system should allow students with access to view and download course materials from the course materials repository.
  - The system should provide filters to help students find the relevant course materials quickly.
  - The system should provide search mechanism to easily navigate course materials. 
  - The system should provide error messages and notifications to inform users of any issues with uploading, downloading, or accessing course materials.


## 3. Assignments management
  - ### Teacher management:
    - The system must allow the teacher must to create and manage assignments, including specifying assignment details, requirements, and grading criteria.
    - The system must allow the teacher must to filter and sort assignments based on various criteria, such as submission date or assignment type.
    - The system must allow the teacher must to download assignments submitted by students.

- ### Student access
  - The system must allow students to view and submit assignments, including uploading assignment files and viewing assignment details.
  - The system must allow students to view their grades and feedback for each assignment.
  - The system must allow students to download their graded assignments and feedback.
  - Security measures in place to prevent unauthorized access or modification of assignments, grades, and feedback.
  - The system must allow student to receive notifications when assignments are created, submitted, graded, or updated.
  
## 4. Exam management
-  The system must allow teachers to create and manage quizzes and exams, including setting questions, response options, and time and length of the quiz or exam.
-  The system must allow students to take quizzes and exams, including selecting the quiz or exam, entering their answers, and submitting their responses.
-  The system must automatically grade quizzes and exams and provide feedback to students in the case of multiple choice questions.
-  The system must provide a timer feature that automatically submits the quiz or exam when the time limit has been reached.
-  The system must allow teachers to set different grading criteria for different questions or sections of the quiz or exam.
-  The system must allow teachers to create multiple versions of a quiz or exam to prevent cheating.
-  The system must allow teachers to view and export quiz and exam results for analysis and record-keeping purposes.
-  The system must have security measures in place to prevent unauthorized access or modification of quizzes, exams, and results.
-  The system must provide a user-friendly interface for both teachers and students to access and interact with the quizzes and exams features.

## 5. Attendance Management 
- The system must allow teachers to create and manage attendance records for their courses,  specifying the class, date and recording the attendance of each student.
- The system must allow teachers to create an automatic attendance collector that students can log into using their credentials .   
- The system must allow teachers to generate attendance reports for each course, including a summary of each student's attendance.
- The system must allow students to view their attendance records for each course they are enrolled in . 
- The system must provide notifications to teachers and students when attendance is recorded or updated. 
- The system must have security measures in place to prevent unauthorized access or modification of attendance records.
- The system must allow teachers to export attendance records in various formats, such as PDF or CSV, for record-keeping purposes.
- The system must provide a user-friendly interface for teachers and students to access and interact with the attendance management features.















  












 


    