import json
import os
from pathlib import Path
from datetime import datetime, timedelta
import random

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------------------------
# 1. CAREER PROFILES (13 Roles)
# ------------------------------------------------------------------------------
CAREER_PROFILES = [
    {
        "id": "data-analyst",
        "title": "Data Analyst",
        "category": "Data & Analytics",
        "description": "Translate complex data into actionable business insights using SQL, statistical analysis, and interactive dashboards.",
        "responsibilities": [
            "Query and manipulate structured relational datasets using ANSI SQL",
            "Build interactive dashboards and visualizations in Power BI or Tableau",
            "Perform exploratory data analysis and statistical validation",
            "Collaborate with business stakeholders to define KPIs and metrics"
        ],
        "required_skills": {
            "SQL": 10,
            "Excel": 8,
            "Python": 8,
            "Power BI": 8,
            "Tableau": 7,
            "Statistics": 8,
            "Data Visualization": 9,
            "Problem Solving": 8
        },
        "interest_tags": ["Data & Analytics", "Business Strategy", "Visualization", "Statistics"],
        "learning_priorities": [
            "Advanced SQL queries, window functions, and aggregations",
            "Data cleaning and transformation with Python Pandas",
            "Business dashboard design in Power BI/Tableau",
            "A/B testing and statistical significance"
        ],
        "related_roles": ["data-scientist", "dba", "product-manager"],
        "is_demo": False
    },
    {
        "id": "data-scientist",
        "title": "Data Scientist",
        "category": "Data & Analytics",
        "description": "Leverage mathematics, statistics, and machine learning algorithms to uncover patterns and predict future outcomes.",
        "responsibilities": [
            "Design and evaluate predictive machine learning models",
            "Conduct hypothesis testing, experiment design, and causal inference",
            "Clean and engineer features from complex unstructured and structured data",
            "Communicate data stories and analytical findings to leadership"
        ],
        "required_skills": {
            "Python": 10,
            "Statistics": 10,
            "Machine Learning": 9,
            "SQL": 8,
            "Pandas": 9,
            "NumPy": 9,
            "Scikit-Learn": 8,
            "Data Visualization": 7
        },
        "interest_tags": ["Data & Analytics", "AI / ML", "Mathematics", "Research"],
        "learning_priorities": [
            "Probability distributions, regression, and hypothesis testing",
            "Supervised and unsupervised learning with Scikit-Learn",
            "Feature engineering and cross-validation pipelines",
            "Model interpretability and evaluation metrics"
        ],
        "related_roles": ["data-analyst", "ml-engineer"],
        "is_demo": False
    },
    {
        "id": "ml-engineer",
        "title": "Machine Learning Engineer",
        "category": "AI & Engineering",
        "description": "Bridge data science and software engineering by building, training, optimizing, and deploying ML models to production.",
        "responsibilities": [
            "Build scalable machine learning and deep learning pipelines",
            "Deploy models as high-throughput REST or gRPC APIs",
            "Monitor data drift, latency, and model accuracy in production",
            "Optimize inference performance using containerization and hardware acceleration"
        ],
        "required_skills": {
            "Python": 10,
            "Machine Learning": 9,
            "Deep Learning": 9,
            "PyTorch": 8,
            "TensorFlow": 8,
            "Docker": 8,
            "REST API": 8,
            "Data Structures": 8
        },
        "interest_tags": ["AI / ML", "Software Development", "Deep Learning", "Systems"],
        "learning_priorities": [
            "Neural network architectures and deep learning frameworks",
            "Model serving with FastAPI and Docker containerization",
            "MLOps pipelines and artifact versioning",
            "Model compression and inference optimization"
        ],
        "related_roles": ["data-scientist", "backend-engineer"],
        "is_demo": False
    },
    {
        "id": "sde",
        "title": "Software Development Engineer",
        "category": "Software Engineering",
        "description": "Design and build scalable software components, master data structures and algorithms, and write maintainable clean code.",
        "responsibilities": [
            "Implement high-performance algorithms and reliable data structures",
            "Write modular, clean, and testable object-oriented code",
            "Participate in design reviews, peer code reviews, and debugging",
            "Analyze time and space complexity of computational solutions"
        ],
        "required_skills": {
            "Java": 9,
            "C++": 9,
            "Python": 8,
            "Data Structures": 10,
            "Algorithms": 10,
            "Object Oriented Programming": 9,
            "DBMS": 8,
            "Problem Solving": 10
        },
        "interest_tags": ["Software Development", "Competitive Programming", "System Design", "Core CS"],
        "learning_priorities": [
            "Master arrays, linked lists, trees, graphs, and dynamic programming",
            "Object-oriented design patterns and SOLID principles",
            "Memory management, concurrency, and operating system basics",
            "Algorithmic complexity optimization"
        ],
        "related_roles": ["backend-engineer", "fullstack-engineer"],
        "is_demo": False
    },
    {
        "id": "frontend-engineer",
        "title": "Frontend Engineer",
        "category": "Web Development",
        "description": "Craft responsive, accessible, high-performance web user interfaces with modern JavaScript/TypeScript and React.",
        "responsibilities": [
            "Develop modular, reusable UI components using React and TypeScript",
            "Optimize web application performance, bundle size, and Core Web Vitals",
            "Implement accessible design standards (WCAG) and responsive styling",
            "Integrate frontend state management with backend RESTful APIs"
        ],
        "required_skills": {
            "JavaScript": 10,
            "TypeScript": 8,
            "React": 10,
            "HTML": 10,
            "CSS": 9,
            "Tailwind CSS": 8,
            "REST API": 8,
            "Git": 8
        },
        "interest_tags": ["Web Development", "UI / UX", "Frontend Technologies", "Design"],
        "learning_priorities": [
            "JavaScript event loop, closures, async/await, and ES6+",
            "React component lifecycle, hooks, context, and state architecture",
            "CSS Grid, Flexbox, responsive design, and CSS variables",
            "Client-side routing, API caching, and performance profiling"
        ],
        "related_roles": ["fullstack-engineer", "ui-ux-engineer"],
        "is_demo": False
    },
    {
        "id": "backend-engineer",
        "title": "Backend Engineer",
        "category": "Web Development",
        "description": "Architect robust server-side APIs, database schemas, authentication layers, and reliable distributed systems.",
        "responsibilities": [
            "Design secure, versioned REST and gRPC API endpoints",
            "Architect relational and NoSQL database schemas with indexes",
            "Implement stateless sessions, JWT/cookies, and role-based access control",
            "Scale server applications using caching, queues, and async workers"
        ],
        "required_skills": {
            "Python": 9,
            "Node.js": 9,
            "FastAPI": 8,
            "SQL": 9,
            "PostgreSQL": 8,
            "Redis": 7,
            "REST API": 10,
            "Docker": 7,
            "System Design": 8
        },
        "interest_tags": ["Software Development", "Backend Technologies", "Databases", "Distributed Systems"],
        "learning_priorities": [
            "API design principles, status codes, and idempotency",
            "Relational database normalization, indexing, and ACID transactions",
            "Caching strategies with Redis and background job workers",
            "Microservices architecture and database migrations"
        ],
        "related_roles": ["fullstack-engineer", "sde", "devops-engineer"],
        "is_demo": False
    },
    {
        "id": "fullstack-engineer",
        "title": "Full Stack Developer",
        "category": "Web Development",
        "description": "Own features end-to-end, building interactive web frontends and resilient backend services and database pipelines.",
        "responsibilities": [
            "Build cohesive features spanning frontend UI, backend API, and database",
            "Maintain consistent data models and validation across client and server",
            "Deploy and monitor integrated full-stack web applications",
            "Debug issues across the browser network tab, API layer, and database"
        ],
        "required_skills": {
            "JavaScript": 9,
            "React": 9,
            "Python": 8,
            "Node.js": 8,
            "SQL": 8,
            "HTML": 8,
            "CSS": 8,
            "REST API": 9,
            "Git": 8
        },
        "interest_tags": ["Web Development", "Full Stack", "Product Development", "Startups"],
        "learning_priorities": [
            "Modern frontend application architecture with React",
            "Backend API creation with FastAPI or Express",
            "Database integration with ORMs and relational schema design",
            "End-to-end deployment, environment configuration, and CI/CD"
        ],
        "related_roles": ["frontend-engineer", "backend-engineer", "sde"],
        "is_demo": False
    },
    {
        "id": "cloud-engineer",
        "title": "Cloud Engineer",
        "category": "Cloud & Infrastructure",
        "description": "Design, provision, and maintain secure, highly available cloud infrastructure on AWS, Azure, or GCP.",
        "responsibilities": [
            "Provision cloud infrastructure using Infrastructure as Code (Terraform)",
            "Configure virtual networks, security groups, and IAM policies",
            "Manage containerized workloads and serverless cloud functions",
            "Optimize cloud infrastructure costs, availability, and disaster recovery"
        ],
        "required_skills": {
            "AWS": 10,
            "Linux": 9,
            "Terraform": 8,
            "Docker": 8,
            "Computer Networks": 8,
            "Python": 7,
            "Bash": 8,
            "Git": 7
        },
        "interest_tags": ["Cloud Computing", "Infrastructure", "Linux", "Networking"],
        "learning_priorities": [
            "Core cloud architecture: compute, storage, networking, and IAM",
            "Linux systems administration and shell automation",
            "Infrastructure as Code with Terraform",
            "Cloud security best practices and compliance"
        ],
        "related_roles": ["devops-engineer", "cybersecurity-analyst"],
        "is_demo": False
    },
    {
        "id": "devops-engineer",
        "title": "DevOps Engineer",
        "category": "Cloud & Infrastructure",
        "description": "Automate deployment pipelines, maintain Kubernetes clusters, and guarantee high system reliability and observability.",
        "responsibilities": [
            "Build automated CI/CD pipelines for test execution and automated deployment",
            "Orchestrate containerized services using Kubernetes and Docker",
            "Implement centralized logging and alerting with Prometheus and Grafana",
            "Enforce security scans and automated compliance checks in build steps"
        ],
        "required_skills": {
            "Docker": 10,
            "Kubernetes": 9,
            "CI/CD": 10,
            "Linux": 9,
            "Git": 9,
            "Bash": 8,
            "Prometheus": 7,
            "AWS": 8
        },
        "interest_tags": ["DevOps", "Automation", "Containers", "Reliability"],
        "learning_priorities": [
            "Containerization principles and multi-stage Docker builds",
            "CI/CD pipeline construction with GitHub Actions",
            "Kubernetes deployments, services, ingress, and helm charts",
            "System metrics monitoring, log aggregation, and alerting"
        ],
        "related_roles": ["cloud-engineer", "backend-engineer"],
        "is_demo": False
    },
    {
        "id": "cybersecurity-analyst",
        "title": "Cybersecurity Analyst",
        "category": "Security",
        "description": "Protect organizational networks, systems, and data from breaches, vulnerabilities, and cyber threats.",
        "responsibilities": [
            "Conduct vulnerability assessments and penetration testing",
            "Monitor security alerts, firewall logs, and intrusion detection events",
            "Ensure adherence to security standards, authentication, and encryption",
            "Perform incident response and root-cause security forensics"
        ],
        "required_skills": {
            "Computer Networks": 10,
            "Linux": 9,
            "Cybersecurity": 10,
            "Python": 7,
            "Bash": 8,
            "Operating Systems": 8,
            "Problem Solving": 8
        },
        "interest_tags": ["Security", "Networking", "Cryptography", "Defense"],
        "learning_priorities": [
            "Network protocols (TCP/IP, DNS, SSL/TLS, HTTP headers)",
            "Web application security (OWASP Top 10 vulnerabilities)",
            "Linux security hardening and log analysis",
            "Cryptography, hashing, and authentication standards"
        ],
        "related_roles": ["cloud-engineer", "devops-engineer"],
        "is_demo": False
    },
    {
        "id": "dba",
        "title": "Database Administrator",
        "category": "Databases & Storage",
        "description": "Manage, tune, secure, and ensure 24/7 availability of critical enterprise relational and distributed databases.",
        "responsibilities": [
            "Optimize query execution plans, indexes, and cache configurations",
            "Set up replication, automated backups, and disaster recovery procedures",
            "Manage user permissions, encryption at rest, and audit logs",
            "Design database migration strategies with minimal downtime"
        ],
        "required_skills": {
            "SQL": 10,
            "PostgreSQL": 9,
            "MySQL": 9,
            "DBMS": 10,
            "Linux": 8,
            "Bash": 7,
            "Operating Systems": 7
        },
        "interest_tags": ["Databases", "Systems Administration", "Performance Tuning"],
        "learning_priorities": [
            "Deep SQL query optimization and EXPLAIN ANALYZE interpretation",
            "B-Tree, Hash, and GIN indexing strategies",
            "WAL logging, transaction isolation levels, and MVCC",
            "Database clustering, read replicas, and backup automation"
        ],
        "related_roles": ["data-analyst", "backend-engineer"],
        "is_demo": False
    },
    {
        "id": "product-manager",
        "title": "Product Manager (Associate / Technical)",
        "category": "Product & Strategy",
        "description": "Bridge technology, business, and user experience to define product roadmaps and guide execution.",
        "responsibilities": [
            "Conduct user research and translate problems into actionable user stories",
            "Define product requirements documents (PRDs) and success metrics",
            "Prioritize engineering backlogs using value vs effort frameworks",
            "Coordinate cross-functional releases between design, dev, and QA"
        ],
        "required_skills": {
            "Product Management": 10,
            "Agile": 9,
            "Data Analysis": 8,
            "SQL": 7,
            "Problem Solving": 9,
            "JIRA": 8
        },
        "interest_tags": ["Product Strategy", "User Experience", "Agile", "Leadership"],
        "learning_priorities": [
            "Customer journey mapping and problem discovery",
            "Writing clear specifications and measurable acceptance criteria",
            "Data-driven product decision making and metrics tracking",
            "Agile sprint planning and stakeholder communication"
        ],
        "related_roles": ["data-analyst", "qa-engineer"],
        "is_demo": False
    },
    {
        "id": "qa-engineer",
        "title": "QA Engineer / Test Automation",
        "category": "QA & Testing",
        "description": "Guarantee software quality, reliability, and security through comprehensive manual and automated test suites.",
        "responsibilities": [
            "Design end-to-end test cases covering functional and edge cases",
            "Develop automated regression test suites using Selenium, Cypress, or Pytest",
            "Perform API testing, load testing, and defect tracking in JIRA",
            "Integrate automated test runs into CI/CD build deployment steps"
        ],
        "required_skills": {
            "Unit Testing": 9,
            "Integration Testing": 9,
            "Selenium": 8,
            "Pytest": 8,
            "Python": 8,
            "Postman": 8,
            "SQL": 7,
            "Git": 7
        },
        "interest_tags": ["Testing", "Automation", "Quality Assurance", "Software Engineering"],
        "learning_priorities": [
            "Test planning, boundary value analysis, and equivalence partitioning",
            "API test automation with Postman and Python requests",
            "UI automation using Selenium / Playwright",
            "Performance and regression testing in CI/CD pipelines"
        ],
        "related_roles": ["sde", "frontend-engineer", "backend-engineer"],
        "is_demo": False
    }
]

with open(DATA_DIR / "career_profiles.json", "w", encoding="utf-8") as f:
    json.dump(CAREER_PROFILES, f, indent=2)

print(f"Generated {len(CAREER_PROFILES)} career profiles in career_profiles.json")
