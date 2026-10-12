"""
SkillForage AI — Hand-Labeled Validation Dataset for Market Skill Extractor
Contains 52 hand-labeled job description snippets across 13 roles and all categories
to evaluate Precision, Recall, and F1 score reproducibly.
"""

VALIDATION_DATASET = [
    # 1 - 10: Data & Analytics
    {
        "id": "JOB_001",
        "text": "We are looking for a Data Analyst with strong SQL, Python, Excel and Power BI skills. The candidate should understand statistics and be able to build analytical dashboards.",
        "expected_skills": ["SQL", "Python", "Excel", "Power BI", "Statistics", "Data Visualization"]
    },
    {
        "id": "JOB_002",
        "text": "The Data Analyst will work with SQL databases, Microsoft Excel and Tableau to create business reports and dashboards.",
        "expected_skills": ["SQL", "Excel", "Tableau", "Data Visualization"]
    },
    {
        "id": "JOB_003",
        "text": "Seeking a Data Scientist proficient in Python, Pandas, NumPy, Scikit-Learn, and statistical hypothesis testing with relational SQL.",
        "expected_skills": ["Python", "Pandas", "NumPy", "Scikit-Learn", "Statistics", "SQL"]
    },
    {
        "id": "JOB_004",
        "text": "Senior Data Scientist role requiring deep learning with PyTorch, NLP (natural language processing), Python 3, and Apache Spark.",
        "expected_skills": ["Deep Learning", "PyTorch", "Natural Language Processing", "Python", "Apache Spark"]
    },
    {
        "id": "JOB_005",
        "text": "Junior Analyst needed with strong Microsoft Excel formulas, Power BI dashboards, and basic ANSI SQL querying skills.",
        "expected_skills": ["Excel", "Power BI", "SQL"]
    },
    {
        "id": "JOB_006",
        "text": "Analytics Engineer will build dbt models, write advanced SQL, manage Snowflake data warehouses, and create Tableau dashboards.",
        "expected_skills": ["SQL", "Tableau", "Data Visualization"]
    },
    {
        "id": "JOB_007",
        "text": "Data Science intern to perform exploratory data analysis using Python, Matplotlib, Seaborn, and Pandas on tabular data.",
        "expected_skills": ["Python", "Pandas", "Data Visualization", "Data Analysis"]
    },
    {
        "id": "JOB_008",
        "text": "Quantitative researcher position requires advanced Statistics, R programming, time-series modeling, and SQL database access.",
        "expected_skills": ["Statistics", "R", "SQL"]
    },
    {
        "id": "JOB_009",
        "text": "Business Intelligence Analyst to design Power BI KPI cards, write DAX expressions, and query Microsoft SQL Server databases.",
        "expected_skills": ["Power BI", "Microsoft SQL Server", "SQL"]
    },
    {
        "id": "JOB_010",
        "text": "Machine Learning researcher with focus on computer vision, OpenCV, PyTorch, TensorFlow, and Python scripting.",
        "expected_skills": ["Computer Vision", "PyTorch", "TensorFlow", "Python", "Machine Learning"]
    },

    # 11 - 20: Software Engineering & Core CS
    {
        "id": "JOB_011",
        "text": "Hiring SDE-1 with strong Data Structures, Algorithms, C++, and Object Oriented Programming principles.",
        "expected_skills": ["Data Structures", "Algorithms", "C++", "Object Oriented Programming"]
    },
    {
        "id": "JOB_012",
        "text": "Java Software Engineer with Core Java 17, Spring Boot, MySQL, REST API design, and JUnit testing experience.",
        "expected_skills": ["Java", "Spring Boot", "MySQL", "REST API", "JUnit", "Unit Testing"]
    },
    {
        "id": "JOB_013",
        "text": "Looking for C++ developer skilled in multithreading, Operating Systems concepts, memory management, and DSA problem solving.",
        "expected_skills": ["C++", "Operating Systems", "Data Structures", "Problem Solving"]
    },
    {
        "id": "JOB_014",
        "text": "Graduate Software Engineer requiring proficiency in Python, Git version control, basic Linux command line, and OOP.",
        "expected_skills": ["Python", "Git", "Linux", "Object Oriented Programming"]
    },
    {
        "id": "JOB_015",
        "text": "Systems programmer needed with strong C language, POSIX threads, socket networking, and Linux kernel fundamentals.",
        "expected_skills": ["C", "Computer Networks", "Linux", "Operating Systems"]
    },
    {
        "id": "JOB_016",
        "text": "Software engineer to build algorithmic trading pipelines in Go (Golang) with low latency and gRPC microservices.",
        "expected_skills": ["Go", "gRPC", "Microservices"]
    },
    {
        "id": "JOB_017",
        "text": "C# .NET developer with ASP.NET Core, Microsoft SQL Server, Entity Framework, and RESTful API architecture.",
        "expected_skills": ["C#", "ASP.NET Core", "Microsoft SQL Server", "REST API"]
    },
    {
        "id": "JOB_018",
        "text": "Backend Engineer with Java, Spring Boot, Kafka, Redis caching, and relational PostgreSQL database design.",
        "expected_skills": ["Java", "Spring Boot", "Redis", "PostgreSQL"]
    },
    {
        "id": "JOB_019",
        "text": "Competitive programmer with mastery of dynamic programming, graph algorithms, trees, and time complexity analysis.",
        "expected_skills": ["Algorithms", "Data Structures", "Problem Solving"]
    },
    {
        "id": "JOB_020",
        "text": "Full Stack SDE with Java backend, React frontend, MySQL database, and Docker containerization.",
        "expected_skills": ["Java", "React", "MySQL", "Docker"]
    },

    # 21 - 30: Frontend & Web Development
    {
        "id": "JOB_021",
        "text": "Frontend developer proficient in React, JavaScript (ES6+), HTML5, CSS3, and Tailwind CSS responsive design.",
        "expected_skills": ["React", "JavaScript", "HTML", "CSS", "Tailwind CSS"]
    },
    {
        "id": "JOB_022",
        "text": "Senior UI Engineer with TypeScript, Next.js, Redux state management, and GraphQL API integration.",
        "expected_skills": ["TypeScript", "Next.js", "Redux", "GraphQL"]
    },
    {
        "id": "JOB_023",
        "text": "Web developer with HTML, modern CSS flexbox and grid, vanilla JS, and cross-browser accessibility.",
        "expected_skills": ["HTML", "CSS", "JavaScript"]
    },
    {
        "id": "JOB_024",
        "text": "Frontend engineer using Vue.js, Vuex, Vite, and RESTful API consumption for high-traffic web portals.",
        "expected_skills": ["Vue.js", "Vite", "REST API"]
    },
    {
        "id": "JOB_025",
        "text": "Angular developer with TypeScript, RxJS, Bootstrap styling, and unit testing using Karma and Jasmine.",
        "expected_skills": ["Angular", "TypeScript", "Bootstrap", "Unit Testing"]
    },
    {
        "id": "JOB_026",
        "text": "Full stack engineer proficient in Node.js, Express.js, React, MongoDB, and Git version control (MERN stack).",
        "expected_skills": ["Node.js", "Express.js", "React", "MongoDB", "Git"]
    },
    {
        "id": "JOB_027",
        "text": "Web app developer skilled in Svelte, SvelteKit, Tailwind CSS, and WebSockets real-time communication.",
        "expected_skills": ["Svelte", "Tailwind CSS", "WebSockets"]
    },
    {
        "id": "JOB_028",
        "text": "Frontend specialist to optimize Webpack bundle size, Core Web Vitals, and TypeScript React components.",
        "expected_skills": ["Webpack", "TypeScript", "React"]
    },
    {
        "id": "JOB_029",
        "text": "JavaScript developer with asynchronous programming (Promises, async/await), DOM manipulation, and Jest testing.",
        "expected_skills": ["JavaScript", "Unit Testing"]
    },
    {
        "id": "JOB_030",
        "text": "Full Stack developer with Python Django backend, PostgreSQL database, HTML/CSS, and React frontend.",
        "expected_skills": ["Python", "Django", "PostgreSQL", "HTML", "CSS", "React"]
    },

    # 31 - 40: Cloud, DevOps & Security
    {
        "id": "JOB_031",
        "text": "Cloud Engineer with hands-on AWS experience (EC2, S3, RDS, Lambda), Linux administration, and Terraform IaC.",
        "expected_skills": ["AWS", "Linux", "Terraform"]
    },
    {
        "id": "JOB_032",
        "text": "DevOps Engineer required with Docker, Kubernetes, CI/CD pipeline automation (GitHub Actions), and Bash scripting.",
        "expected_skills": ["Docker", "Kubernetes", "CI/CD", "Bash"]
    },
    {
        "id": "JOB_033",
        "text": "Site Reliability Engineer (SRE) skilled in Prometheus monitoring, Grafana dashboards, Linux, and Python automation.",
        "expected_skills": ["Prometheus", "Grafana", "Linux", "Python"]
    },
    {
        "id": "JOB_034",
        "text": "Cloud Architect with Microsoft Azure, Kubernetes clusters, Docker containers, and enterprise security policies.",
        "expected_skills": ["Azure", "Kubernetes", "Docker"]
    },
    {
        "id": "JOB_035",
        "text": "Security Analyst with network security, Wireshark, Computer Networks (TCP/IP), and Linux systems auditing.",
        "expected_skills": ["Computer Networks", "Linux", "Cybersecurity"]
    },
    {
        "id": "JOB_036",
        "text": "DevSecOps engineer to integrate automated security scanning, Docker image analysis, and Jenkins CI/CD pipelines.",
        "expected_skills": ["Docker", "Jenkins", "CI/CD", "Cybersecurity"]
    },
    {
        "id": "JOB_037",
        "text": "Infrastructure engineer with Google Cloud Platform (GCP), Terraform, Ansible configuration management, and Git.",
        "expected_skills": ["Google Cloud Platform", "Terraform", "Ansible", "Git"]
    },
    {
        "id": "JOB_038",
        "text": "Cybersecurity penetration tester experienced in web application security (OWASP Top 10), Python, and cryptography.",
        "expected_skills": ["Cybersecurity", "Python"]
    },
    {
        "id": "JOB_039",
        "text": "System Administrator with Red Hat Linux, Bash shell scripting, Nginx reverse proxy configuration, and SSH.",
        "expected_skills": ["Linux", "Bash", "Nginx"]
    },
    {
        "id": "JOB_040",
        "text": "Cloud developer building serverless microservices with AWS Lambda, DynamoDB, API Gateway, and Python.",
        "expected_skills": ["AWS", "DynamoDB", "Python", "Microservices"]
    },

    # 41 - 52: QA, Database & Specialized Roles
    {
        "id": "JOB_041",
        "text": "QA Automation Engineer with Selenium WebDriver, Java, TestNG, and Postman REST API testing experience.",
        "expected_skills": ["Selenium", "Java", "Postman", "Unit Testing", "REST API"]
    },
    {
        "id": "JOB_042",
        "text": "Python SDET with Pytest test automation, Git, CI/CD pipeline triggers, and SQL database verification.",
        "expected_skills": ["Python", "Pytest", "Git", "CI/CD", "SQL"]
    },
    {
        "id": "JOB_043",
        "text": "Database Administrator (DBA) needed to tune PostgreSQL performance, manage replication, and optimize complex SQL queries.",
        "expected_skills": ["PostgreSQL", "SQL", "DBMS"]
    },
    {
        "id": "JOB_044",
        "text": "MySQL DBA with InnoDB engine tuning, backup automation using Bash, Linux servers, and high availability clustering.",
        "expected_skills": ["MySQL", "Bash", "Linux", "DBMS"]
    },
    {
        "id": "JOB_045",
        "text": "NoSQL Database Engineer with MongoDB replica sets, index optimization, Redis caching, and Express backend integration.",
        "expected_skills": ["MongoDB", "Redis", "Express.js"]
    },
    {
        "id": "JOB_046",
        "text": "Mobile App Developer with Flutter and Dart, REST APIs integration, and SQLite local offline storage.",
        "expected_skills": ["Dart", "REST API", "SQLite"]
    },
    {
        "id": "JOB_047",
        "text": "Associate Product Manager with Agile sprint planning, JIRA backlog management, and SQL data queries for KPI tracking.",
        "expected_skills": ["Product Management", "Agile", "JIRA", "SQL"]
    },
    {
        "id": "JOB_048",
        "text": "Data Engineer with Apache Spark, PySpark, Python, Hadoop, and relational SQL data pipelines.",
        "expected_skills": ["Apache Spark", "Python", "SQL"]
    },
    {
        "id": "JOB_049",
        "text": "Backend developer with FastAPI, async Python, SQLAlchemy, PostgreSQL, and Docker containerization.",
        "expected_skills": ["FastAPI", "Python", "PostgreSQL", "Docker"]
    },
    {
        "id": "JOB_050",
        "text": "QA Engineer for web applications using Cypress end-to-end testing, JavaScript, and defect logging in JIRA.",
        "expected_skills": ["Cypress", "JavaScript", "JIRA", "Integration Testing"]
    },
    {
        "id": "JOB_051",
        "text": "AI Engineer implementing RAG pipelines using LangChain, OpenAI, Python, and vector databases with Fastapi.",
        "expected_skills": ["Python", "FastAPI", "Artificial Intelligence"]
    },
    {
        "id": "JOB_052",
        "text": "Blockchain / Distributed systems developer with Rust programming, cryptography fundamentals, and Linux networking.",
        "expected_skills": ["Rust", "Linux", "Computer Networks"]
    }
]