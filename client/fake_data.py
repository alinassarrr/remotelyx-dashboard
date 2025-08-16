from datetime import datetime, timedelta
import random

# Fake job data with all required fields
JOBS_DATA = [
    {
        "job_title": "Senior Full Stack Developer",
        "seniority": "Senior",
        "emp_type": "Full-time",
        "company_name": "TechCorp Solutions",
        "soft_skills": ["Leadership", "Communication", "Problem Solving", "Team Collaboration"],
        "tech_skills": ["React", "Node.js", "Python", "MongoDB", "AWS"],
        "job_desc": "Lead development of scalable web applications using modern technologies. Mentor junior developers and collaborate with cross-functional teams.",
        "salary": "$120,000 - $150,000",
        "date_posted": "2024-01-15",
        "job_link": "https://techcorp.com/careers/senior-dev",
        "status": "New"
    },
    {
        "job_title": "Frontend Developer",
        "seniority": "Mid",
        "emp_type": "Full-time",
        "company_name": "Digital Innovations Inc",
        "soft_skills": ["Creativity", "Attention to Detail", "Time Management"],
        "tech_skills": ["React", "CSS", "JavaScript", "TypeScript", "Figma"],
        "job_desc": "Build responsive and interactive user interfaces. Work closely with designers to implement pixel-perfect designs.",
        "salary": "$80,000 - $100,000",
        "date_posted": "2024-01-14",
        "job_link": "https://digitalinnovations.com/jobs/frontend",
        "status": "Analyzed"
    },
    {
        "job_title": "Python Backend Engineer",
        "seniority": "Mid",
        "emp_type": "Contract",
        "company_name": "DataFlow Systems",
        "soft_skills": ["Analytical Thinking", "Documentation", "Problem Solving"],
        "tech_skills": ["Python", "Django", "PostgreSQL", "Redis", "Docker"],
        "job_desc": "Develop robust backend services and APIs. Optimize database performance and implement data processing pipelines.",
        "salary": "$90,000 - $110,000",
        "date_posted": "2024-01-13",
        "job_link": "https://dataflow.com/careers/python-engineer",
        "status": "Match"
    },
    {
        "job_title": "DevOps Engineer",
        "seniority": "Senior",
        "emp_type": "Full-time",
        "company_name": "CloudTech Solutions",
        "soft_skills": ["Infrastructure Planning", "Risk Management", "Automation Mindset"],
        "tech_skills": ["AWS", "Docker", "Kubernetes", "Terraform", "Jenkins"],
        "job_desc": "Design and maintain cloud infrastructure. Implement CI/CD pipelines and ensure system reliability.",
        "salary": "$110,000 - $140,000",
        "date_posted": "2024-01-12",
        "job_link": "https://cloudtech.com/jobs/devops",
        "status": "New"
    },
    {
        "job_title": "UI/UX Designer",
        "seniority": "Junior",
        "emp_type": "Full-time",
        "company_name": "Creative Studios",
        "soft_skills": ["Creativity", "User Empathy", "Visual Communication"],
        "tech_skills": ["Figma", "Adobe Creative Suite", "Prototyping", "User Research"],
        "job_desc": "Create intuitive and beautiful user interfaces. Conduct user research and design user experiences.",
        "salary": "$60,000 - $75,000",
        "date_posted": "2024-01-11",
        "job_link": "https://creativestudios.com/careers/designer",
        "status": "Analyzed"
    },
    {
        "job_title": "Data Scientist",
        "seniority": "Senior",
        "emp_type": "Full-time",
        "company_name": "Analytics Pro",
        "soft_skills": ["Statistical Analysis", "Business Acumen", "Storytelling"],
        "tech_skills": ["Python", "R", "SQL", "Machine Learning", "Tableau"],
        "job_desc": "Analyze complex datasets and build predictive models. Present insights to stakeholders and drive data-driven decisions.",
        "salary": "$130,000 - $160,000",
        "date_posted": "2024-01-10",
        "job_link": "https://analyticspro.com/jobs/data-scientist",
        "status": "Match"
    },
    {
        "job_title": "Mobile App Developer",
        "seniority": "Mid",
        "emp_type": "Contract",
        "company_name": "AppWorks Mobile",
        "soft_skills": ["User Focus", "Problem Solving", "Adaptability"],
        "tech_skills": ["React Native", "iOS", "Android", "JavaScript", "Firebase"],
        "job_desc": "Develop cross-platform mobile applications. Ensure optimal performance and user experience across devices.",
        "salary": "$85,000 - $105,000",
        "date_posted": "2024-01-09",
        "job_link": "https://appworks.com/careers/mobile-dev",
        "status": "New"
    },
    {
        "job_title": "QA Engineer",
        "seniority": "Junior",
        "emp_type": "Full-time",
        "company_name": "Quality First",
        "soft_skills": ["Attention to Detail", "Critical Thinking", "Communication"],
        "tech_skills": ["Selenium", "Python", "JIRA", "Test Automation", "API Testing"],
        "job_desc": "Design and execute test plans. Automate testing processes and ensure software quality.",
        "salary": "$55,000 - $70,000",
        "date_posted": "2024-01-08",
        "job_link": "https://qualityfirst.com/jobs/qa-engineer",
        "status": "Analyzed"
    },
    {
        "job_title": "Product Manager",
        "seniority": "Senior",
        "emp_type": "Full-time",
        "company_name": "Product Vision",
        "soft_skills": ["Leadership", "Strategic Thinking", "Stakeholder Management"],
        "tech_skills": ["Product Strategy", "Data Analysis", "Agile", "User Research"],
        "job_desc": "Lead product development from concept to launch. Define product vision and work with cross-functional teams.",
        "salary": "$140,000 - $180,000",
        "date_posted": "2024-01-07",
        "job_link": "https://productvision.com/careers/product-manager",
        "status": "Match"
    },
    {
        "job_title": "Cybersecurity Analyst",
        "seniority": "Mid",
        "emp_type": "Full-time",
        "company_name": "SecureNet",
        "soft_skills": ["Analytical Thinking", "Risk Assessment", "Incident Response"],
        "tech_skills": ["Network Security", "Penetration Testing", "SIEM", "Python", "Linux"],
        "job_desc": "Monitor security systems and investigate security incidents. Implement security measures and conduct vulnerability assessments.",
        "salary": "$95,000 - $120,000",
        "date_posted": "2024-01-06",
        "job_link": "https://securenet.com/jobs/cybersecurity",
        "status": "New"
    },
    {
        "job_title": "Blockchain Developer",
        "seniority": "Senior",
        "emp_type": "Contract",
        "company_name": "ChainTech",
        "soft_skills": ["Innovation", "Problem Solving", "Technical Communication"],
        "tech_skills": ["Solidity", "Ethereum", "Smart Contracts", "Web3", "JavaScript"],
        "job_desc": "Develop decentralized applications and smart contracts. Research blockchain technologies and implement innovative solutions.",
        "salary": "$120,000 - $150,000",
        "date_posted": "2024-01-05",
        "job_link": "https://chaintech.com/careers/blockchain-dev",
        "status": "Analyzed"
    },
    {
        "job_title": "Machine Learning Engineer",
        "seniority": "Mid",
        "emp_type": "Full-time",
        "company_name": "AI Solutions",
        "soft_skills": ["Research Mindset", "Problem Solving", "Collaboration"],
        "tech_skills": ["Python", "TensorFlow", "PyTorch", "MLOps", "AWS"],
        "job_desc": "Build and deploy machine learning models. Optimize model performance and create scalable ML pipelines.",
        "salary": "$100,000 - $130,000",
        "date_posted": "2024-01-04",
        "job_link": "https://aisolutions.com/jobs/ml-engineer",
        "status": "Match"
    },
    {
        "job_title": "Cloud Architect",
        "seniority": "Senior",
        "emp_type": "Full-time",
        "company_name": "CloudScale",
        "soft_skills": ["Architecture Planning", "Cost Optimization", "Technical Leadership"],
        "tech_skills": ["AWS", "Azure", "GCP", "Terraform", "Kubernetes"],
        "job_desc": "Design scalable cloud architectures. Lead cloud migration projects and optimize infrastructure costs.",
        "salary": "$150,000 - $190,000",
        "date_posted": "2024-01-03",
        "job_link": "https://cloudscale.com/careers/cloud-architect",
        "status": "New"
    },
    {
        "job_title": "Frontend Team Lead",
        "seniority": "Senior",
        "emp_type": "Full-time",
        "company_name": "WebTech Solutions",
        "soft_skills": ["Team Leadership", "Mentoring", "Project Management"],
        "tech_skills": ["React", "Vue.js", "TypeScript", "CSS", "Performance Optimization"],
        "job_desc": "Lead frontend development team. Set technical standards and mentor developers while delivering high-quality products.",
        "salary": "$130,000 - $160,000",
        "date_posted": "2024-01-02",
        "job_link": "https://webtech.com/jobs/frontend-lead",
        "status": "Analyzed"
    },
    {
        "job_title": "Database Administrator",
        "seniority": "Mid",
        "emp_type": "Full-time",
        "company_name": "DataTech",
        "soft_skills": ["Problem Solving", "Performance Optimization", "Documentation"],
        "tech_skills": ["PostgreSQL", "MySQL", "MongoDB", "SQL", "Database Design"],
        "job_desc": "Manage and optimize database systems. Ensure data security and implement backup strategies.",
        "salary": "$85,000 - $110,000",
        "date_posted": "2024-01-01",
        "job_link": "https://datatech.com/careers/dba",
        "status": "Match"
    },
    {
        "job_title": "Game Developer",
        "seniority": "Junior",
        "emp_type": "Full-time",
        "company_name": "GameStudio",
        "soft_skills": ["Creativity", "Problem Solving", "Attention to Detail"],
        "tech_skills": ["Unity", "C#", "3D Modeling", "Game Design", "Physics"],
        "job_desc": "Develop engaging video games using Unity. Create game mechanics and implement user interactions.",
        "salary": "$65,000 - $80,000",
        "date_posted": "2023-12-31",
        "job_link": "https://gamestudio.com/jobs/game-dev",
        "status": "New"
    },
    {
        "job_title": "Network Engineer",
        "seniority": "Mid",
        "emp_type": "Full-time",
        "company_name": "NetConnect",
        "soft_skills": ["Troubleshooting", "Network Planning", "Documentation"],
        "tech_skills": ["Cisco", "Network Security", "VPN", "Routing", "Switching"],
        "job_desc": "Design and maintain network infrastructure. Troubleshoot network issues and implement security measures.",
        "salary": "$90,000 - $115,000",
        "date_posted": "2023-12-30",
        "job_link": "https://netconnect.com/careers/network-engineer",
        "status": "Analyzed"
    },
    {
        "job_title": "API Developer",
        "seniority": "Mid",
        "emp_type": "Contract",
        "company_name": "APIConnect",
        "soft_skills": ["API Design", "Documentation", "Problem Solving"],
        "tech_skills": ["REST", "GraphQL", "Node.js", "Python", "Postman"],
        "job_desc": "Design and develop RESTful APIs. Ensure API security and create comprehensive documentation.",
        "salary": "$80,000 - $100,000",
        "date_posted": "2023-12-29",
        "job_link": "https://apiconnect.com/jobs/api-dev",
        "status": "Match"
    },
    {
        "job_title": "Technical Writer",
        "seniority": "Junior",
        "emp_type": "Full-time",
        "company_name": "DocTech",
        "soft_skills": ["Technical Writing", "Communication", "Research"],
        "tech_skills": ["Markdown", "Git", "API Documentation", "Technical Writing Tools"],
        "job_desc": "Create technical documentation and user guides. Work with development teams to document software features.",
        "salary": "$55,000 - $70,000",
        "date_posted": "2023-12-28",
        "job_link": "https://doctech.com/careers/technical-writer",
        "status": "New"
    },
    {
        "job_title": "Site Reliability Engineer",
        "seniority": "Senior",
        "emp_type": "Full-time",
        "company_name": "Reliability First",
        "soft_skills": ["Incident Response", "Automation", "Performance Optimization"],
        "tech_skills": ["Docker", "Kubernetes", "Prometheus", "Grafana", "Python"],
        "job_desc": "Ensure system reliability and performance. Implement monitoring and automate operational tasks.",
        "salary": "$130,000 - $160,000",
        "date_posted": "2023-12-27",
        "job_link": "https://reliabilityfirst.com/jobs/sre",
        "status": "Analyzed"
    },
    {
        "job_title": "Embedded Systems Engineer",
        "seniority": "Mid",
        "emp_type": "Full-time",
        "company_name": "EmbedTech",
        "soft_skills": ["Hardware Knowledge", "Problem Solving", "Testing"],
        "tech_skills": ["C/C++", "Embedded Linux", "Microcontrollers", "RTOS", "Hardware Design"],
        "job_desc": "Develop embedded software for IoT devices. Work with hardware teams to optimize system performance.",
        "salary": "$95,000 - $120,000",
        "date_posted": "2023-12-26",
        "job_link": "https://embedtech.com/careers/embedded-engineer",
        "status": "Match"
    },
    {
        "job_title": "Full Stack Developer",
        "seniority": "Junior",
        "emp_type": "Full-time",
        "company_name": "StartupTech",
        "soft_skills": ["Learning Mindset", "Problem Solving", "Team Collaboration"],
        "tech_skills": ["React", "Node.js", "JavaScript", "CSS", "MongoDB"],
        "job_desc": "Build web applications from frontend to backend. Learn new technologies and contribute to product development.",
        "salary": "$70,000 - $85,000",
        "date_posted": "2023-12-25",
        "job_link": "https://startuptech.com/jobs/fullstack-junior",
        "status": "New"
    },
    {
        "job_title": "Data Engineer",
        "seniority": "Mid",
        "emp_type": "Full-time",
        "company_name": "DataPipeline",
        "soft_skills": ["Data Modeling", "Problem Solving", "Performance Optimization"],
        "tech_skills": ["Python", "Apache Spark", "SQL", "ETL", "Data Warehousing"],
        "job_desc": "Build data pipelines and ETL processes. Optimize data processing and ensure data quality.",
        "salary": "$100,000 - $125,000",
        "date_posted": "2023-12-24",
        "job_link": "https://datapipeline.com/careers/data-engineer",
        "status": "Analyzed"
    },
    {
        "job_title": "Security Engineer",
        "seniority": "Senior",
        "emp_type": "Full-time",
        "company_name": "SecureTech",
        "soft_skills": ["Security Mindset", "Risk Assessment", "Incident Response"],
        "tech_skills": ["Penetration Testing", "Security Tools", "Network Security", "Python", "Linux"],
        "job_desc": "Implement security measures and conduct security assessments. Respond to security incidents and protect company assets.",
        "salary": "$140,000 - $170,000",
        "date_posted": "2023-12-23",
        "job_link": "https://securetech.com/jobs/security-engineer",
        "status": "Match"
    },
    {
        "job_title": "UI Developer",
        "seniority": "Junior",
        "emp_type": "Full-time",
        "company_name": "Interface Design",
        "soft_skills": ["Design Sense", "Attention to Detail", "User Focus"],
        "tech_skills": ["HTML", "CSS", "JavaScript", "Responsive Design", "Accessibility"],
        "job_desc": "Create responsive and accessible user interfaces. Work with designers to implement pixel-perfect designs.",
        "salary": "$60,000 - $75,000",
        "date_posted": "2023-12-22",
        "job_link": "https://interfacedesign.com/careers/ui-dev",
        "status": "New"
    },
    {
        "job_title": "Backend Team Lead",
        "seniority": "Senior",
        "emp_type": "Full-time",
        "company_name": "Backend Solutions",
        "soft_skills": ["Technical Leadership", "Architecture Design", "Team Management"],
        "tech_skills": ["Java", "Spring Boot", "Microservices", "Kubernetes", "PostgreSQL"],
        "job_desc": "Lead backend development team. Design system architecture and ensure code quality and performance.",
        "salary": "$150,000 - $180,000",
        "date_posted": "2023-12-21",
        "job_link": "https://backendsolutions.com/jobs/backend-lead",
        "status": "Analyzed"
    },
    {
        "job_title": "React Developer",
        "seniority": "Mid",
        "emp_type": "Contract",
        "company_name": "ReactWorks",
        "soft_skills": ["Component Design", "State Management", "Performance Optimization"],
        "tech_skills": ["React", "Redux", "TypeScript", "CSS", "Testing"],
        "job_desc": "Build scalable React applications. Implement state management and optimize component performance.",
        "salary": "$85,000 - $105,000",
        "date_posted": "2023-12-20",
        "job_link": "https://reactworks.com/careers/react-dev",
        "status": "Match"
    },
    {
        "job_title": "Python Developer",
        "seniority": "Junior",
        "emp_type": "Full-time",
        "company_name": "Python Solutions",
        "soft_skills": ["Problem Solving", "Learning Mindset", "Code Quality"],
        "tech_skills": ["Python", "Django", "Flask", "SQL", "Git"],
        "job_desc": "Develop Python applications and APIs. Learn best practices and contribute to team projects.",
        "salary": "$65,000 - $80,000",
        "date_posted": "2023-12-19",
        "job_link": "https://pythonsolutions.com/careers/python-dev",
        "status": "New"
    }
]

# Trending skills data
TRENDING_SKILLS = [
    {"skill": "React", "percentage": 85},
    {"skill": "Python", "percentage": 78},
    {"skill": "JavaScript", "percentage": 92},
    {"skill": "AWS", "percentage": 73},
    {"skill": "Docker", "percentage": 68},
    {"skill": "TypeScript", "percentage": 81},
    {"skill": "Kubernetes", "percentage": 62},
    {"skill": "Machine Learning", "percentage": 71}
]

# Hard to fill jobs data
HARD_TO_FILL_JOBS = [
    {"title": "Senior DevOps Engineer", "days": 45},
    {"title": "Blockchain Developer", "days": 38},
    {"title": "Cybersecurity Specialist", "days": 52},
    {"title": "ML Engineer", "days": 41},
    {"title": "Cloud Architect", "days": 47}
]

# Recent activity feed data
RECENT_ACTIVITY = [
    {"action": "New job posted", "company": "TechCorp Solutions", "time": "2 hours ago"},
    {"action": "Application received", "job": "Frontend Developer", "time": "4 hours ago"},
    {"action": "Interview scheduled", "candidate": "John Smith", "time": "6 hours ago"},
    {"action": "Job status updated", "job": "Python Engineer", "time": "8 hours ago"},
    {"action": "New company registered", "company": "Innovation Labs", "time": "1 day ago"},
    {"action": "Application reviewed", "job": "Data Scientist", "time": "1 day ago"}
]

# Dashboard statistics
DASHBOARD_STATS = {
    "active_jobs": len(JOBS_DATA),
    "new_this_week": len([job for job in JOBS_DATA if job["status"] == "New"]),
    "avg_process_time": 3.2,
    "status_for_date": "2024-01-15"
}