import sqlite3
import os

db_path = os.path.join(os.getcwd(), 'instance', 'job_portal.db')

os.makedirs(os.path.dirname(db_path), exist_ok=True)

conn = sqlite3.connect(db_path)

cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS user;")
cursor.execute("DROP TABLE IF EXISTS company;")
cursor.execute("DROP TABLE IF EXISTS job;")
print("Dropped existing tables")

cursor.execute("""
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    disability TEXT NOT NULL,
    job_field_interest TEXT NOT NULL,
    skills TEXT NOT NULL,
    latitude REAL,
    longitude REAL,
    is_active BOOLEAN DEFAULT 1
);
""")

# Create the Company table
cursor.execute("""
CREATE TABLE IF NOT EXISTS company (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    job_field TEXT NOT NULL,
    amenities TEXT NOT NULL,
    rating REAL NOT NULL,
    address TEXT NOT NULL,
    latitude REAL,
    longitude REAL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS job (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    job_field TEXT NOT NULL,
    required_skills TEXT NOT NULL,
    company_id INTEGER NOT NULL,
    FOREIGN KEY (company_id) REFERENCES company (id)
);
""")

users = [
     ('John Doe', 'johndoe@example.com', 'hashed_password1', 'Visual Impairment', 'Software Development', 'Python, Java, SQL', 40.7128, -74.0060, True),
    ('Jane Smith', 'janesmith@example.com', 'hashed_password2', 'Hearing Impairment', 'Graphic Design', 'Figma, Photoshop, Illustrator', 34.0522, -118.2437, True),
    ('Alice Brown', 'alicebrown@example.com', 'hashed_password3', 'Mobility Impairment', 'Data Analysis', 'Excel, Python, Tableau', 51.5074, -0.1278, True),
    ('Bob Johnson', 'bobjohnson@example.com', 'hashed_password4', 'Speech Impairment', 'Content Writing', 'SEO, Blogging, Technical Writing', 48.8566, 2.3522, True),
    ('Emily Davis', 'emilydavis@example.com', 'hashed_password5', 'Autism', 'Digital Marketing', 'SEO, Google Ads, Social Media Management', 37.7749, -122.4194, True),
    ('Michael Wilson', 'michaelwilson@example.com', 'hashed_password6', 'Hearing Impairment', 'Customer Support', 'CRM Tools, Problem Solving, Communication', 41.8781, -87.6298, True),
    ('Sarah Lee', 'sarahlee@example.com', 'hashed_password7', 'Visual Impairment', 'Teaching', 'Lesson Planning, Educational Psychology, Communication', 34.6937, 135.5023, True),
    ('James Taylor', 'jamestaylor@example.com', 'hashed_password8', 'Mobility Impairment', 'Accounting', 'Tally, Financial Reporting, Taxation', 33.8688, 151.2093, True),
    ('Mia Hernandez', 'miahernandez@example.com', 'hashed_password9', 'Speech Impairment', 'Healthcare', 'Nursing, Patient Care, First Aid', 19.4326, -99.1332, True),
    ('David Martinez', 'davidmartinez@example.com', 'hashed_password10', 'Visual Impairment', 'Law', 'Legal Research, Advocacy, Case Management', 28.6139, 77.2090, True),
    ('Sofia Anderson', 'sofiaanderson@example.com', 'hashed_password11', 'Autism', 'Software Testing', 'Manual Testing, Automation Testing, Selenium', 39.9042, 116.4074, True),
    ('Liam Moore', 'liammoore@example.com', 'hashed_password12', 'Hearing Impairment', 'Mechanical Engineering', 'CAD, SolidWorks, Manufacturing Processes', 55.7558, 37.6173, True),
    ('Olivia Garcia', 'oliviagarcia@example.com', 'hashed_password13', 'Mobility Impairment', 'Data Science', 'Python, R, Machine Learning', 35.6895, 139.6917, True),
    ('Noah Thomas', 'noahthomas@example.com', 'hashed_password14', 'Speech Impairment', 'Human Resources', 'Recruitment, Employee Relations, Payroll Management', 52.5200, 13.4050, True),
    ('Emma Jackson', 'emmajackson@example.com', 'hashed_password15', 'Visual Impairment', 'Graphic Design', 'CorelDRAW, Figma, UI Design', 40.7306, -73.9352, True),
    ('Lucas Martin', 'lucasmartin@example.com', 'hashed_password16', 'Autism', 'Project Management', 'Agile, Scrum, Resource Management', 41.3851, 2.1734, True),
    ('Ava Walker', 'avawalker@example.com', 'hashed_password17', 'Hearing Impairment', 'Web Development', 'HTML, CSS, JavaScript', 48.2082, 16.3738, True),
    ('Isabella Young', 'isabellayoung@example.com', 'hashed_password18', 'Mobility Impairment', 'Customer Support', 'Problem Solving, CRM, Conflict Resolution', 31.2304, 121.4737, True),
    ('Ethan Perez', 'ethanperez@example.com', 'hashed_password19', 'Speech Impairment', 'Finance', 'Financial Analysis, Investment Strategies, Risk Management', 59.3293, 18.0686, True),
    ('Harper Gonzalez', 'harpergonzalez@example.com', 'hashed_password20', 'Visual Impairment', 'Content Writing', 'Blogging, Technical Writing, Editing', 45.4642, 9.1900, True),
    ('Mason Hall', 'masonhall@example.com', 'hashed_password21', 'Autism', 'Photography', 'Photo Editing, DSLR Handling, Composition', 41.0082, 28.9784, True),
    ('Ella Lewis', 'ellalewis@example.com', 'hashed_password22', 'Hearing Impairment', 'Event Management', 'Planning, Coordination, Vendor Management', 13.7563, 100.5018, True),
    ('Logan Harris', 'loganharris@example.com', 'hashed_password23', 'Mobility Impairment', 'IT Support', 'Networking, Troubleshooting, Customer Assistance', 37.5665, 126.9780, True),
    ('Charlotte Clark', 'charlotteclark@example.com', 'hashed_password24', 'Speech Impairment', 'Education', 'Curriculum Development, Research, Lesson Planning', 19.0760, 72.8777, True),
    ('Benjamin Adams', 'benjaminadams@example.com', 'hashed_password25', 'Visual Impairment', 'Business Analysis', 'Process Improvement, Stakeholder Management, Reporting', 25.2760, 55.2962, True),
    ('Amelia Roberts', 'ameliaroberts@example.com', 'hashed_password26', 'Autism', 'Product Design', 'Prototyping, CAD, 3D Printing', 23.8103, 90.4125, True),
    ('Henry Wilson', 'henrywilson@example.com', 'hashed_password27', 'Hearing Impairment', 'Cybersecurity', 'Ethical Hacking, Network Security, Cryptography', 35.6895, 51.3890, True),
    ('Aria White', 'ariawhite@example.com', 'hashed_password28', 'Mobility Impairment', 'Legal Assistance', 'Case Research, Client Counseling, Drafting Legal Documents', 30.0444, 31.2357, True),
    ('Jacob Sanchez', 'jacobsanchez@example.com', 'hashed_password29', 'Speech Impairment', 'Marketing', 'Content Strategy, Digital Ads, Campaign Management', 21.0285, 105.8542, True),
    ('Mila King', 'milaking@example.com', 'hashed_password30', 'Visual Impairment', 'Software Testing', 'Selenium, Java, Regression Testing', 39.9042, 116.4074, True),
    ('Elijah Scott', 'elijahscott@example.com', 'hashed_password31', 'Autism', 'Data Analysis', 'Python, Power BI, SQL', 6.5244, 3.3792, True),
    ('Chloe Green', 'chloegreen@example.com', 'hashed_password32', 'Hearing Impairment', 'Animation', 'Maya, Blender, Storyboarding', 35.6895, 139.6917, True),
    ('Daniel Turner', 'danielturner@example.com', 'hashed_password33', 'Mobility Impairment', 'Operations Management', 'Inventory Control, Logistics, Process Optimization', 33.8688, 151.2093, True),
    ('Grace Parker', 'graceparker@example.com', 'hashed_password34', 'Speech Impairment', 'Healthcare', 'Nursing, Patient Care, Teamwork', 43.6532, -79.3832, True),
    ('Matthew Torres', 'matthewtorres@example.com', 'hashed_password35', 'Visual Impairment', 'Civil Engineering', 'AutoCAD, Structural Analysis, Site Management', 14.5995, 120.9842, True),
    ('Lily Ramirez', 'lilyramirez@example.com', 'hashed_password36', 'Autism', 'Creative Writing', 'Fiction Writing, Poetry, Blogging', 37.7749, -122.4194, True),
    ('Sebastian Murphy', 'sebastianmurphy@example.com', 'hashed_password37', 'Hearing Impairment', 'Audio Engineering', 'Sound Mixing, Pro Tools, Editing', 51.5074, -0.1278, True),
    ('Zoe Rivera', 'zoerivera@example.com', 'hashed_password38', 'Mobility Impairment', 'Fitness Coaching', 'Personal Training, Nutrition, Rehabilitation', 48.8566, 2.3522, True),
    ('Ryan Peterson', 'ryanpeterson@example.com', 'hashed_password39', 'Speech Impairment', 'Translation', 'English-Spanish, English-French, Localization', 40.4168, -3.7038, True),
    
]

companies = [
    ('Inclusive Tech Solutions', 'Software Development', 'Screen readers, Braille signage, Elevator audio support', 4.8, '123 Tech Drive, New York, NY', 40.7128, -74.0060),
    ('Creative Designs Ltd.', 'Graphic Design', 'Height-adjustable desks, Quiet zones, Sign language interpreters', 4.7, '456 Art Street, Los Angeles, CA', 34.0522, -118.2437),
    ('DataPros Analytics', 'Data Analysis', 'Wheelchair ramps, Accessible restrooms, Ergonomic chairs', 4.6, '789 Data Lane, London, UK', 51.5074, -0.1278),
    ('Content Innovators', 'Content Writing', 'Speech-to-text tools, Voice-activated devices, Writing assistants', 4.5, '321 Word Way, Paris, FR', 48.8566, 2.3522),
    ('Digital Marketing Hub', 'Digital Marketing', 'Adjustable desks, Sign language interpreters, Accessible software', 4.9, '123 Media Blvd, Toronto, CA', 43.6532, -79.3832),
    ('Creative Coders', 'Software Development', 'Hearing loops, Screen readers, Adjustable desks', 4.6, '789 Developer Drive, Berlin, DE', 52.5200, 13.4050),
    ('Inclusive Education Systems', 'Education', 'Accessible classrooms, Hearing aids, Braille textbooks', 4.8, '456 Learning Lane, Sydney, AU', -33.8688, 151.2093),
    ('Health Solutions Corp.', 'Healthcare', 'Voice-controlled devices, Adjustable beds, Wheelchair access', 4.5, '123 Health Ave, Chicago, IL', 41.8781, -87.6298),
    ('Empowerment Technologies', 'Cybersecurity', 'Accessible workstations, Speech recognition, Visual alerts', 4.7, '123 Secure Street, San Francisco, CA', 37.7749, -122.4194),
    ('Tech For All', 'Software Development', 'Height-adjustable desks, Large fonts, Sign language interpreters', 4.8, '321 Tech Plaza, Amsterdam, NL', 52.3676, 4.9041),
    ('Innovative Education Solutions', 'Education', 'Audio-visual aids, Wheelchair accessible ramps, Screen magnifiers', 4.9, '987 School St, Tokyo, JP', 35.6762, 139.6503),
    ('Universal Designs', 'Product Design', 'Voice-activated design tools, Height-adjustable desks, Large monitors', 4.8, '456 Creative Drive, Barcelona, ES', 41.3851, 2.1734),
    ('Flexible Solutions Inc.', 'Consulting', 'Remote work options, Visual alerts, Adjustable chairs', 4.6, '123 Consultation Rd, Madrid, ES', 40.4168, -3.7038),
    ('Digital Accessibility Experts', 'IT Support', 'Screen magnifiers, Voice-controlled software, Wheelchair access', 4.7, '555 Tech Avenue, Dubai, AE', 25.276987, 55.296249),
    ('Accessibility Labs', 'Software Testing', 'Voice-to-text, Customizable font sizes, Hearing aids', 4.8, '123 Lab Lane, London, UK', 51.5074, -0.1278),
    ('Equal Opportunity Solutions', 'Human Resources', 'Screen readers, Remote work options, Audio cues', 4.5, '890 HR Park, Vancouver, CA', 49.2827, -123.1207),
    ('Adaptive Technologies', 'Engineering', 'Accessible hardware, Voice-activated equipment, Ergonomic desks', 4.9, '234 Tech Ave, Montreal, CA', 45.5017, -73.5673),
    ('Global Inclusion Technologies', 'Tech Development', 'Elevator audio support, Accessible meeting rooms, Adjustable lighting', 4.7, '789 Inclusive Blvd, Paris, FR', 48.8566, 2.3522),
    ('Smart Accessibility Solutions', 'Product Development', 'Adjustable workstations, Speech recognition, Customizable lighting', 4.6, '555 Innovation St, San Francisco, CA', 37.7749, -122.4194),
    ('Barrier-Free Living Solutions', 'Architecture', 'Accessible building designs, Wheelchair access, Audio feedback systems', 4.8, '321 Design Rd, Tokyo, JP', 35.6762, 139.6503),
    ('Advanced Healthcare Tech', 'Healthcare', 'Assistive technology, Remote health services, Adjustable medical devices', 4.9, '789 Health Drive, Berlin, DE', 52.5200, 13.4050),
    ('Inclusive Communities Foundation', 'Non-profit', 'Ramps, Audio guidance, Support for remote work', 4.5, '456 Community St, London, UK', 51.5074, -0.1278),
]

jobs = [
    ('Frontend Developer', 'Software Development', 'HTML, CSS, JavaScript', 1),
    ('UI/UX Designer', 'Graphic Design', 'Figma, Adobe XD, Wireframing', 2),
    ('Data Scientist', 'Data Analysis', 'Python, Machine Learning, SQL', 3),
    ('Technical Writer', 'Content Writing', 'SEO, Blogging, Research', 4),
    ('SEO Specialist', 'Digital Marketing', 'SEO, Google Analytics, Content Strategy', 5),
    ('Full Stack Developer', 'Software Development', 'JavaScript, React, Node.js', 6),
    ('System Administrator', 'IT Support', 'Linux, Networking, Security', 7),
    ('Healthcare Consultant', 'Healthcare', 'Medical Knowledge, Communication, Analysis', 8),
    ('Security Analyst', 'Cybersecurity', 'Firewalls, Encryption, Risk Management', 9),
    ('Product Manager', 'Product Design', 'Agile, Scrum, User Research', 10),
    ('Social Media Manager', 'Digital Marketing', 'Social Media Strategy, Content Creation', 11),
    ('Project Manager', 'Project Management', 'Agile, Scrum, Resource Management', 12),
    ('Data Analyst', 'Data Analysis', 'Excel, SQL, Power BI', 13),
    ('Network Administrator', 'IT Support', 'Networking, Router Configuration, Troubleshooting', 14),
    ('Audio Engineer', 'Engineering', 'Sound Mixing, Pro Tools, Audio Editing', 15),
    ('Educational Coordinator', 'Education', 'Lesson Planning, Curriculum Development', 16),
    ('Legal Advisor', 'Law', 'Research, Legal Analysis, Client Communication', 17),
    ('Civil Engineer', 'Engineering', 'AutoCAD, Structural Design, Surveying', 18),
    ('Content Strategist', 'Content Writing', 'Content Marketing, SEO, Copywriting', 19),
    ('Customer Support Representative', 'Customer Support', 'CRM Software, Problem Solving, Communication', 20),
    ('Sales Manager', 'Sales', 'Sales Strategy, Negotiation, Client Management', 21),
    ('Marketing Manager', 'Marketing', 'Marketing Strategy, Content Creation, Brand Management', 22),
    ('Business Analyst', 'Business Analysis', 'Process Improvement, Requirements Gathering', 23),
    ('QA Tester', 'Software Testing', 'Manual Testing, Automation, Selenium', 24),
    ('Graphic Designer', 'Graphic Design', 'Photoshop, Illustrator, Branding', 25),
    ('Machine Learning Engineer', 'Software Development', 'Python, TensorFlow, Data Science', 26),
    ('Operations Manager', 'Operations Management', 'Process Optimization, Scheduling, Logistics', 27),
    ('Product Designer', 'Product Design', 'Prototyping, Sketch, User Interface Design', 28),
    ('Mechanical Engineer', 'Engineering', 'SolidWorks, CAD, Manufacturing', 29),
    ('Marketing Director', 'Marketing', 'SEO, SEM, Analytics', 30),
    ('UI Developer', 'Software Development', 'HTML, CSS, React', 31),
    ('Database Administrator', 'Data Analysis', 'SQL, Database Management, Performance Tuning', 32),
    ('Healthcare Administrator', 'Healthcare', 'Health Services, Project Management, Leadership', 33),
    ('IT Support Specialist', 'IT Support', 'Networking, Troubleshooting, Security', 34),
    ('Cybersecurity Expert', 'Cybersecurity', 'Penetration Testing, Security Auditing', 35),
    ('Legal Researcher', 'Law', 'Case Law, Legal Writing, Research', 36),
    ('Event Coordinator', 'Event Management', 'Event Planning, Vendor Management, Budgeting', 37),
    ('Fitness Trainer', 'Fitness Coaching', 'Personal Training, Fitness Planning, Nutrition', 38),
    ('Translator', 'Translation', 'English-Spanish, Localization, Proofreading', 39),
    ('Web Developer', 'Web Development', 'HTML, CSS, JavaScript', 40),
    ('Copywriter', 'Content Writing', 'Copywriting, SEO, Blogging', 41),
    ('Financial Analyst', 'Finance', 'Financial Modeling, Excel, Analysis', 42),
    ('HR Specialist', 'Human Resources', 'Recruitment, Employee Relations, Benefits', 43),
    ('UX Researcher', 'UX Design', 'Usability Testing, User Research, Analytics', 44),
    ('Sales Support', 'Sales', 'Customer Support, Lead Generation, CRM', 45),
    ('Digital Marketing Specialist', 'Digital Marketing', 'Social Media, PPC, Google Ads', 46),
]


cursor.executemany("""
INSERT INTO user (name, email, password, disability, job_field_interest, skills, latitude, longitude, is_active)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
""", users)

cursor.executemany("""
INSERT INTO company (name, job_field, amenities, rating, address, latitude, longitude)
VALUES (?, ?, ?, ?, ?, ?, ?);
""", companies)

cursor.executemany("""
INSERT INTO job (title, job_field, required_skills, company_id)
VALUES (?, ?, ?, ?);
""", jobs)

conn.commit()

print("Tables created and bulk data inserted successfully.")

conn.close()
