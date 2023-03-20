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
## 6. TODO tracking 
- The system must provide an interface to the student to track their assigned class work and their deadlines. 
- The system must provide a user-friendly interface for students and teachers to add, delete, prioritize, and update tasks in their to-do lists.
- The system must allow students and teachers to receive reminders and notifications for upcoming deadlines.
- The system must allow students and teachers to view their completed and upcoming tasks.
- The system must have security measures in place to prevent unauthorized access or modification of tasks and deadlines.
## 7. Performance tracking 
- The system must allow teachers to view and analyze student performance data on assignments, quizzes, and exams.
- The system must allow students to view their own performance data on assignments, quizzes, and exams.
- The system must be able to track student performance over time and provide data on trends and patterns.
- The system must provide visual representations of performance data, such as graphs or charts, to assist with analysis and understanding.
- The system must have filtering and sorting capabilities to allow teachers to view performance data by assignment type, class, or other criteria.
- The system must have the ability to provide recommendations for additional support or interventions based on student performance data.
- ## 8. Posts and comments 
- The system must allow teachers to create posts and announcements, including specifying the title, content, and relevant course or class.
- The system must allow teachers to schedule posts and announcements to be published at a future date and time.
- The system must allow teachers to edit or delete their own posts and announcements.
- The system must allow students to comment on posts and announcements, including adding text, images, and links.
- The system must allow students to receive notifications when new posts or announcements are published.
- The system must allow students to view and reply to other students' comments.
- The system must notify teachers when new comments are added to their posts or announcements.
- The system must allow teachers to moderate comments.
- The system must have security measures in place to prevent unauthorized access or modification of posts and comments.
## 9. Notification system 
- The system should provide automated notifications to students about upcoming assignments, quizzes, and other important course events.
- The system should include an option for students to turn off notifications for specific courses or events.
- The system should provide an interface for teachers to create and send notifications to their students.
- The interface should allow teachers to select the recipients of the notification (e.g., specific students, entire class).
- The interface should allow teachers to schedule notifications for a specific date and time.
- The system should allow students to manage their notification preferences and turn off notifications for specific courses or events.
## 10. Automated exam creation
- The system should provide an automated exam creation interface that samples weighted question from a test bank.  
- The automated exam creation system must be able to randomly select questions from a test bank and generate an exam for a specified course.
- The system must ensure that the exams created are fair and balanced, with an appropriate mix of question types and difficulty levels.
- The system should allow teachers to specify the number of questions, time limit, and other parameters for the exam.
- The system should allow teachers to review and edit the exams generated by the system, including the ability to add or remove specific questions.
- The system should provide a secure platform for students to take the exams, with features such as timed exams and random question order.
- The system should provide teachers with the ability to review and analyze exam results, including individual student performance and overall exam statistics.
- The system should allow teachers to manage the test bank by adding, removing, or updating questions as needed.
- The system should provide user-friendly interfaces for teachers to access and use the automated exam creation system.
## 11. Automated Grading 
- The system must provide support for automated grading for exam , quiz or assignment questions with definitive answer keys. 
- The system must allow teachers to upload answer keys for supported question types. 
- The system shall automatically grade submitted assignments, quizzes, and exams based on the uploaded answer keys.
- The system shall provide students with immediate feedback on their assignments, quizzes, and exams, including their scores and any incorrect answers.
## 12. Student toolbox 
- The system should provide student with a toolbox to accelerate common tasks for students. 
- The toolbox should include a cloud-based IDE to allow students to directly work on and submit their programming assignments.
- The toolbox should include a calculator tool with a simple interface.
- The time tracking tool should allow students to track the time spent on different tasks related to their coursework, and should provide helpful insights such as reports and graphs to help students improve their time management skills.
- The toolbox should be customizable so that students can add or remove tools as needed.
- The toolbox should be designed with a user-friendly interface that is easy to navigate and use.