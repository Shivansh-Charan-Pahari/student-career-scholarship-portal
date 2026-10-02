"""
Career Intelligence, Skill Gap & Dynamic Roadmap Engine
Provides:
- Transparent multi-dimensional Career Readiness Score (0-100)
- Skill Gap Analysis comparing student skills to industry benchmarks
- Multi-disciplinary Career Roadmaps tailored to specific career roles
- Roadmap progress tracking & milestone management
"""

from models import db, StudentProfile, Skill, Project, Certification, RoadmapProgress

CAREER_ROLE_REQUIREMENTS = {
    "Software Engineer": ["Python", "C++", "DSA", "OOP", "SQL", "Git", "Linux", "System Design"],
    "Full Stack Developer": ["HTML", "CSS", "JavaScript", "Python", "Flask", "SQL", "Git", "DSA"],
    "Backend Developer": ["Python", "Flask", "SQL", "Database Design", "REST APIs", "Git", "DSA", "Linux"],
    "Frontend Developer": ["HTML", "CSS", "JavaScript", "Responsive Design", "Git", "UI/UX", "Web Performance"],
    "Data Scientist": ["Python", "SQL", "Machine Learning", "Pandas", "NumPy", "Statistics", "Data Visualization"],
    "AI/ML Engineer": ["Python", "Machine Learning", "Deep Learning", "Mathematics", "PyTorch", "Git", "Data Analysis"],
    "Cloud & DevOps Engineer": ["Linux", "AWS", "Docker", "Python", "Networking", "Git", "CI/CD", "DevOps"],
    "Cybersecurity Analyst": ["Networking", "Linux", "Python", "Cryptography", "Security Protocols", "Ethical Hacking"],
    "Embedded Systems & IoT": ["C", "C++", "Microcontrollers", "RTOS", "Embedded C", "IoT Protocols", "Electronics"]
}

ROADMAP_DEFINITIONS = {
    "Full Stack Developer": [
        {"id": "01", "title": "Programming & Logic Fundamentals", "description": "Master core syntax, variables, loops, control flow, functions, and logic building with Python or JavaScript.", "skills": ["Python", "JavaScript", "Control Flow", "Functions"], "category": "Foundation", "resources": "https://www.freecodecamp.org"},
        {"id": "02", "title": "HTML5 & Modern CSS3 Layouts", "description": "Understand semantic markup, responsive grid/flexbox layouts, CSS custom properties, and modern web styling.", "skills": ["HTML5", "CSS3", "Flexbox", "CSS Grid", "Responsive Design"], "category": "Frontend", "resources": "https://developer.mozilla.org"},
        {"id": "03", "title": "Vanilla JavaScript & Async DOM", "description": "Learn ES6+ syntax, asynchronous JS (Promises, async/await), Fetch API, event listeners, and DOM manipulation.", "skills": ["JavaScript ES6+", "DOM Manipulation", "Async/Await", "Fetch API"], "category": "Frontend", "resources": "https://javascript.info"},
        {"id": "04", "title": "Python & Backend Architecture", "description": "Develop proficiency in modular Python, file I/O, error handling, virtual environments, and REST principles.", "skills": ["Python 3", "Virtual Environments", "Package Management", "JSON/APIs"], "category": "Backend", "resources": "https://docs.python.org/3"},
        {"id": "05", "title": "Relational Databases & SQL Modeling", "description": "Understand 3NF schema design, normalization, joins, composite indexing, and SQLite/PostgreSQL optimization.", "skills": ["SQL", "SQLite", "PostgreSQL", "Database Design", "Indexing"], "category": "Database", "resources": "https://sqlbolt.com"},
        {"id": "06", "title": "Flask Web Development & ORM", "description": "Build server-rendered web apps, REST APIs, session authentication, and database ORMs with Flask-SQLAlchemy.", "skills": ["Flask", "Flask-SQLAlchemy", "Jinja2", "RESTful Routing", "Sessions"], "category": "Backend", "resources": "https://flask.palletsprojects.com"},
        {"id": "07", "title": "Git & GitHub Version Control", "description": "Master version control, branches, pull requests, resolving merge conflicts, and publishing open-source repositories.", "skills": ["Git", "GitHub", "Branching", "Merge Conflicts", "Open Source"], "category": "DevOps", "resources": "https://learngitbranching.js.org"},
        {"id": "08", "title": "Data Structures & Problem Solving", "description": "Practice arrays, linked lists, stacks, queues, trees, graphs, sorting, searching, and algorithm complexity.", "skills": ["Arrays & Strings", "Trees & Graphs", "Sorting & Searching", "Time Complexity"], "category": "DSA", "resources": "https://leetcode.com"},
        {"id": "09", "title": "Build Production Capstone Project", "description": "Create a multi-tiered full-stack application featuring live authentication, database transactions, and responsive SaaS UI.", "skills": ["Full Stack Integration", "UI/UX Polish", "Error Handling", "Testing"], "category": "Portfolio", "resources": "https://github.com"},
        {"id": "10", "title": "Internship Applications & Networking", "description": "Craft an ATS-compliant resume, optimize LinkedIn/GitHub profiles, and actively apply to curated internship postings.", "skills": ["Resume Building", "Portfolio", "Cold Outreach", "Application Tracking"], "category": "Career", "resources": "#"},
        {"id": "11", "title": "Technical & System Design Interviews", "description": "Conduct mock coding interviews, whiteboard system fundamentals, and rehearse behavioral STAR questions.", "skills": ["Mock Interviews", "System Design Basics", "Behavioral Prep", "CS Fundamentals"], "category": "Interview", "resources": "https://neetcode.io"},
        {"id": "12", "title": "Industry Career Launch & Growth", "description": "Secure entry-level engineering roles, contribute to production codebases, and maintain continuous technical learning.", "skills": ["Production Code", "Agile/Scrum", "Continuous Learning", "Networking"], "category": "Career", "resources": "#"}
    ],
    "Software Engineer": [
        {"id": "01", "title": "Core Programming (C++ / Python)", "description": "Develop strong command over language syntax, memory management, pointers, and standard libraries.", "skills": ["C++", "Python", "Memory Management", "STL"], "category": "Foundation", "resources": "https://learncpp.com"},
        {"id": "02", "title": "Object-Oriented Design & Principles", "description": "Master encapsulation, inheritance, polymorphism, abstraction, and SOLID architectural design principles.", "skills": ["OOP", "Design Patterns", "SOLID Principles", "Modularity"], "category": "Foundation", "resources": "https://refactoring.guru"},
        {"id": "03", "title": "Data Structures Mastery", "description": "Implement arrays, linked lists, trees, heaps, hash maps, and graph structures from scratch.", "skills": ["Data Structures", "Trees", "Graphs", "Hash Tables"], "category": "DSA", "resources": "https://leetcode.com"},
        {"id": "04", "title": "Algorithms & Optimization", "description": "Practice binary search, dynamic programming, greedy algorithms, divide-and-conquer, and asymptotic notation.", "skills": ["Algorithms", "Dynamic Programming", "Recursion", "Big-O Analysis"], "category": "DSA", "resources": "https://geeksforgeeks.org"},
        {"id": "05", "title": "Operating Systems & Linux Shell", "description": "Understand process scheduling, threads, concurrency, deadlocks, virtual memory, and Bash scripting.", "skills": ["Linux", "Operating Systems", "Threads & Concurrency", "Bash"], "category": "Systems", "resources": "https://linuxjourney.com"},
        {"id": "06", "title": "Computer Networks & Protocols", "description": "Study OSI layers, TCP/UDP sockets, HTTP/HTTPS, DNS, routing, and client-server socket programming.", "skills": ["Computer Networks", "TCP/IP", "HTTP", "Sockets"], "category": "Systems", "resources": "https://cloudflare.com/learning"},
        {"id": "07", "title": "Database Systems & SQL Optimization", "description": "Write complex SQL queries, index optimization, ACID transaction management, and schema design.", "skills": ["SQL", "Relational DBs", "Transactions", "Query Optimization"], "category": "Database", "resources": "https://sqlbolt.com"},
        {"id": "08", "title": "Low-Level & High-Level System Design", "description": "Learn scaling, load balancing, caching, microservices architecture, and UML diagram modeling.", "skills": ["System Design", "Scalability", "Caching", "Microservices"], "category": "Architecture", "resources": "https://github.com/donnemartin/system-design-primer"},
        {"id": "09", "title": "Comprehensive Capstone Software", "description": "Build and document a full-fledged software system with automated test suites and continuous integration.", "skills": ["Testing", "Software Architecture", "CI/CD", "Documentation"], "category": "Portfolio", "resources": "https://github.com"},
        {"id": "10", "title": "Coding Challenges & Mock Interviews", "description": "Solve 150+ standard coding interview problems on LeetCode/HackerRank and practice live problem solving.", "skills": ["LeetCode 150", "Mock Interviews", "Whiteboarding", "Behavioral"], "category": "Interview", "resources": "https://neetcode.io"}
    ],
    "Data Scientist": [
        {"id": "01", "title": "Python for Data Science", "description": "Master Python data structures, list comprehensions, functional programming, and data scripting.", "skills": ["Python", "Data Types", "Scripting", "Modules"], "category": "Foundation", "resources": "https://python.org"},
        {"id": "02", "title": "Applied Mathematics & Statistics", "description": "Master linear algebra, multivariate calculus, probability distributions, hypothesis testing, and p-values.", "skills": ["Statistics", "Linear Algebra", "Calculus", "Probability"], "category": "Mathematics", "resources": "https://khanacademy.org"},
        {"id": "03", "title": "Data Manipulation (Pandas & NumPy)", "description": "Clean, reshape, transform, and aggregate structured datasets using NumPy arrays and Pandas dataframes.", "skills": ["Pandas", "NumPy", "Data Cleaning", "Feature Extraction"], "category": "Data Wrangling", "resources": "https://pandas.pydata.org"},
        {"id": "04", "title": "Exploratory Data Analysis & Visualization", "description": "Create intuitive statistical plots using Matplotlib, Seaborn, and interactive dashboards in Plotly.", "skills": ["Data Visualization", "Matplotlib", "Seaborn", "Plotly"], "category": "Analysis", "resources": "https://seaborn.pydata.org"},
        {"id": "05", "title": "Advanced SQL & Data Warehousing", "description": "Write window functions, CTEs, complex joins, and query large analytical datasets efficiently.", "skills": ["SQL", "Window Functions", "Data Warehousing", "ETL"], "category": "Database", "resources": "https://mode.com/sql-tutorial"},
        {"id": "06", "title": "Classical Machine Learning Algorithms", "description": "Implement regression, decision trees, random forests, SVM, clustering, and evaluation metrics with Scikit-Learn.", "skills": ["Machine Learning", "Scikit-Learn", "Cross Validation", "Model Metrics"], "category": "ML", "resources": "https://scikit-learn.org"},
        {"id": "07", "title": "Deep Learning Fundamentals", "description": "Understand neural network architectures, backpropagation, CNNs, RNNs, and Transformers.", "skills": ["Deep Learning", "PyTorch", "TensorFlow", "Neural Networks"], "category": "Deep Learning", "resources": "https://fast.ai"},
        {"id": "08", "title": "Model Deployment & Portfolio", "description": "Deploy machine learning models as REST APIs using Flask/FastAPI and build a portfolio of data science case studies.", "skills": ["Model Deployment", "FastAPI", "Streamlit", "Portfolio"], "category": "Portfolio", "resources": "https://kaggle.com"}
    ],
    "AI/ML Engineer": [
        {"id": "01", "title": "Mathematics for Machine Learning", "description": "Matrix operations, eigenvalues, gradient descent, multivariate optimization, and probability theory.", "skills": ["Linear Algebra", "Vector Calculus", "Probability", "Optimization"], "category": "Mathematics", "resources": "https://mml-book.github.io"},
        {"id": "02", "title": "Python & Scientific Computing", "description": "High-performance computation with NumPy, Pandas, Scipy, and GPU accelerated workflows.", "skills": ["Python", "NumPy", "GPU Computing", "Data Pipelines"], "category": "Foundation", "resources": "https://numpy.org"},
        {"id": "03", "title": "Supervised & Unsupervised Learning", "description": "Classification, regression, dimension reduction (PCA), clustering, and hyperparameter tuning.", "skills": ["Machine Learning", "Scikit-Learn", "Model Tuning", "Feature Engineering"], "category": "ML", "resources": "https://scikit-learn.org"},
        {"id": "04", "title": "Deep Neural Networks with PyTorch", "description": "Build multi-layer perceptrons, custom loss functions, optimizers, and training loops in PyTorch.", "skills": ["PyTorch", "Neural Networks", "Backprop", "CUDA"], "category": "Deep Learning", "resources": "https://pytorch.org/tutorials"},
        {"id": "05", "title": "Computer Vision & Image Processing", "description": "Image classification, object detection (YOLO), segmentation, and OpenCV transformations.", "skills": ["Computer Vision", "OpenCV", "CNNs", "Object Detection"], "category": "Specialization", "resources": "https://opencv.org"},
        {"id": "06", "title": "Natural Language Processing (NLP)", "description": "Text tokenization, embeddings, RNNs/LSTMs, Transformers, BERT, and Large Language Model architectures.", "skills": ["NLP", "Transformers", "BERT", "LLMs"], "category": "Specialization", "resources": "https://huggingface.co"},
        {"id": "07", "title": "MLOps & Scalable AI Infrastructure", "description": "Model registry, experiment tracking (MLflow), containerization with Docker, and CI/CD for ML.", "skills": ["MLOps", "MLflow", "Docker", "Model Monitoring"], "category": "Engineering", "resources": "https://ml-ops.org"},
        {"id": "08", "title": "End-to-End AI Capstone Project", "description": "Build, deploy, and benchmark a production-ready AI application with real-time inference endpoints.", "skills": ["AI Production", "API Integration", "Model Benchmarking", "GitHub"], "category": "Portfolio", "resources": "https://github.com"}
    ],
    "Cloud & DevOps Engineer": [
        {"id": "01", "title": "Linux Administration & Shell Scripting", "description": "User management, file permissions, process monitoring, systemd, SSH, and Bash automation.", "skills": ["Linux", "Bash", "SSH", "System Administration"], "category": "Foundation", "resources": "https://linuxjourney.com"},
        {"id": "02", "title": "Networking & Cloud Security Fundamentals", "description": "Subnets, CIDR blocks, VPCs, DNS, firewalls, load balancers, TLS/SSL certificates, and IAM policies.", "skills": ["Networking", "VPC", "Security", "IAM"], "category": "Networking", "resources": "https://cloudflare.com"},
        {"id": "03", "title": "Git & Infrastructure Collaboration", "description": "Advanced Git workflows, semantic versioning, and code review practices for infrastructure scripts.", "skills": ["Git", "GitHub Actions", "Collaboration", "Versioning"], "category": "DevOps", "resources": "https://git-scm.com"},
        {"id": "04", "title": "Containerization with Docker", "description": "Build lightweight multi-stage Dockerfiles, manage images, compose multi-service apps, and container networking.", "skills": ["Docker", "Docker Compose", "Containers", "Microservices"], "category": "Containers", "resources": "https://docs.docker.com"},
        {"id": "05", "title": "Cloud Computing (AWS / GCP)", "description": "Deploy on EC2, S3, RDS, Lambda, CloudWatch, and understand core cloud architecture best practices.", "skills": ["AWS", "EC2", "S3", "Serverless"], "category": "Cloud", "resources": "https://aws.amazon.com/training"},
        {"id": "06", "title": "Kubernetes & Container Orchestration", "description": "Deploy Pods, Services, Deployments, Ingress controllers, Helm charts, and manage cluster scaling.", "skills": ["Kubernetes", "Helm", "Cluster Management", "Orchestration"], "category": "Containers", "resources": "https://kubernetes.io/docs"},
        {"id": "07", "title": "Infrastructure as Code (Terraform)", "description": "Write declarative infrastructure modules, state management, and automate cloud provisioning.", "skills": ["Terraform", "IaC", "Cloud Provisioning", "Automation"], "category": "Automation", "resources": "https://learn.hashicorp.com/terraform"},
        {"id": "08", "title": "CI/CD Pipelines & Monitoring", "description": "Build automated test/build/deploy pipelines (GitHub Actions, Jenkins) and observability with Prometheus/Grafana.", "skills": ["CI/CD", "GitHub Actions", "Prometheus", "Grafana"], "category": "DevOps", "resources": "https://grafana.com"}
    ],
    "Cybersecurity Analyst": [
        {"id": "01", "title": "Networking & Security Fundamentals", "description": "TCP/IP handshake, DNS, DHCP, routing, packet sniffing with Wireshark, and firewall configurations.", "skills": ["Networking", "Wireshark", "Firewalls", "TCP/IP"], "category": "Foundation", "resources": "https://wireshark.org"},
        {"id": "02", "title": "Linux & Command-Line Security", "description": "Kali Linux tools, security auditing, permission auditing, log inspection, and shell automation.", "skills": ["Linux", "Kali Linux", "Auditing", "Bash"], "category": "Systems", "resources": "https://kali.org"},
        {"id": "03", "title": "Cryptography & Public Key Infrastructure", "description": "Symmetric vs asymmetric encryption, RSA, AES, hashing (SHA-256), digital signatures, and SSL/TLS.", "skills": ["Cryptography", "Encryption", "Hashing", "PKI"], "category": "Security", "resources": "https://cryptopals.com"},
        {"id": "04", "title": "Python for Security & Automation", "description": "Build port scanners, vulnerability probes, automated log parsers, and custom penetration scripts.", "skills": ["Python", "Security Scripting", "Automation", "Sockets"], "category": "Scripting", "resources": "https://python.org"},
        {"id": "05", "title": "Web Application Security (OWASP Top 10)", "description": "Understand SQL Injection, XSS, CSRF, SSRF, Broken Authentication, and secure code remediations.", "skills": ["OWASP Top 10", "SQL Injection", "XSS", "Burp Suite"], "category": "Web Security", "resources": "https://portswigger.net/web-security"},
        {"id": "06", "title": "Vulnerability Assessment & Penetration Testing", "description": "Conduct reconnaissance, scanning (Nmap), exploitation (Metasploit), and write remediation reports.", "skills": ["Nmap", "Metasploit", "Penetration Testing", "Reporting"], "category": "Pen Testing", "resources": "https://tryhackme.com"},
        {"id": "07", "title": "SOC Operations & Threat Detection", "description": "Analyze SIEM telemetry (Splunk/ELK), detect intrusions, investigate incident response scenarios.", "skills": ["SIEM", "Splunk", "Incident Response", "Threat Hunting"], "category": "Defense", "resources": "https://splunk.com"},
        {"id": "08", "title": "Security Compliance & Certification Prep", "description": "Study NIST framework, ISO 27001 standards, and prepare for industry certifications (CompTIA Security+).", "skills": ["NIST", "Compliance", "Security+", "Ethics"], "category": "Career", "resources": "https://cisa.gov"}
    ],
    "Embedded Systems & IoT": [
        {"id": "01", "title": "C & Embedded C Programming", "description": "Master bitwise operations, memory layout, register manipulation, pointers, and interrupts.", "skills": ["C", "Embedded C", "Bitwise Operations", "Interrupts"], "category": "Foundation", "resources": "https://learn-c.org"},
        {"id": "02", "title": "Microcontroller Architectures (ARM / AVR)", "description": "Study 8051, ATmega, ARM Cortex-M architecture, clock systems, timers, ADC, and PWM.", "skills": ["Microcontrollers", "ARM Cortex", "Timers", "ADC/PWM"], "category": "Hardware", "resources": "https://arm.com"},
        {"id": "03", "title": "Hardware Communication Protocols", "description": "Interface sensors using UART, SPI, I2C, CAN, and RS-485 serial communication buses.", "skills": ["I2C", "SPI", "UART", "CAN Bus"], "category": "Protocols", "resources": "https://sparkfun.com"},
        {"id": "04", "title": "Real-Time Operating Systems (FreeRTOS)", "description": "Implement task scheduling, semaphores, mutexes, message queues, and memory management.", "skills": ["FreeRTOS", "Task Scheduling", "Concurrency", "Semaphores"], "category": "RTOS", "resources": "https://freertos.org"},
        {"id": "05", "title": "IoT Protocols & Wireless Networking", "description": "Connect devices via Wi-Fi, Bluetooth BLE, Zigbee, LoRa, and MQTT telemetry brokers.", "skills": ["MQTT", "IoT Protocols", "BLE", "ESP32"], "category": "IoT", "resources": "https://espressif.com"},
        {"id": "06", "title": "PCB Design & Circuit Prototyping", "description": "Design schematic diagrams and multi-layer printed circuit boards using KiCAD or EasyEDA.", "skills": ["PCB Design", "KiCAD", "Schematics", "Circuit Analysis"], "category": "Hardware", "resources": "https://kicad.org"},
        {"id": "07", "title": "Embedded Linux & Device Drivers", "description": "Build custom Linux kernels using Yocto, write kernel modules, and interface GPIO drivers on Raspberry Pi.", "skills": ["Embedded Linux", "Device Drivers", "Kernel Modules", "Raspberry Pi"], "category": "Systems", "resources": "https://bootlin.com"},
        {"id": "08", "title": "IoT Smart System Capstone", "description": "Build an end-to-end edge-to-cloud IoT device with real-time sensor processing and remote monitoring.", "skills": ["IoT Capstone", "Cloud Telemetry", "Hardware Integration", "Firmware"], "category": "Portfolio", "resources": "https://github.com"}
    ]
}

class CareerService:
    @staticmethod
    def calculate_career_readiness(profile: StudentProfile | None, skills: list | None = None) -> dict:
        """
        Calculates a dynamic, transparent Career Readiness Score (0-100)
        derived from 6 distinct dimensions:
        1. Academic Score (15 pts) - CGPA scaled
        2. Technical Skill Match (25 pts) - Benchmark skill fulfillment & proficiency level
        3. Projects & Portfolio (20 pts) - Practical project implementations
        4. Professional Certifications (10 pts) - Validated credentials
        5. Problem Solving / DSA (15 pts) - DSA presence & competence
        6. Professional Completeness (15 pts) - GitHub, LinkedIn, Resume, Bio completeness
        """
        if not profile:
            target_role = "Full Stack Developer"
            benchmarks = CAREER_ROLE_REQUIREMENTS[target_role]
            return {
                'target_role': target_role,
                'readiness_score': 0,
                'benchmark_skills': benchmarks,
                'acquired_skills': [],
                'missing_skills': benchmarks,
                'additional_skills': [],
                'all_roles': list(CAREER_ROLE_REQUIREMENTS.keys()),
                'dimensions': {
                    'academic_score': 0,
                    'skills_score': 0,
                    'projects_score': 0,
                    'certifications_score': 0,
                    'dsa_score': 0,
                    'profile_score': 0
                }
            }

        # Determine target role
        raw_target = profile.preferred_role or profile.career_goal or "Full Stack Developer"
        matched_role = "Full Stack Developer"
        for role_name in CAREER_ROLE_REQUIREMENTS:
            if role_name.lower() in raw_target.lower() or raw_target.lower() in role_name.lower():
                matched_role = role_name
                break

        benchmark_skills = CAREER_ROLE_REQUIREMENTS[matched_role]
        skills_list = skills if skills is not None else (profile.skills or [])
        student_skill_map = {s.name.strip().lower(): s.level for s in skills_list}

        # ---------------------------------------------------------
        # Dimension 1: Academic Score (15 pts)
        # ---------------------------------------------------------
        cgpa = float(profile.cgpa or 0.0)
        academic_score = 15.0 * min(1.0, cgpa / 10.0) if cgpa > 0 else 7.5

        # ---------------------------------------------------------
        # Dimension 2: Technical Skills Match (25 pts)
        # ---------------------------------------------------------
        acquired_skills = []
        missing_skills = []
        skill_points = 0.0

        for req in benchmark_skills:
            req_lower = req.lower()
            found = False
            user_level = "Missing"

            for s_name, s_level in student_skill_map.items():
                if s_name in req_lower or req_lower in s_name:
                    found = True
                    user_level = s_level
                    if s_level == 'Advanced':
                        skill_points += 1.0
                    elif s_level == 'Intermediate':
                        skill_points += 0.8
                    else: # Beginner
                        skill_points += 0.6
                    break

            if found:
                acquired_skills.append({'name': req, 'level': user_level, 'status': 'acquired'})
            else:
                missing_skills.append(req)
                acquired_skills.append({'name': req, 'level': 'Not Added', 'status': 'missing'})

        skills_score = (skill_points / len(benchmark_skills)) * 25.0 if benchmark_skills else 0.0

        # Additional skills outside benchmark
        additional_skills = []
        for s in skills_list:
            if not any(s.name.lower() in req.lower() or req.lower() in s.name.lower() for req in benchmark_skills):
                additional_skills.append({'name': s.name, 'level': s.level, 'status': 'additional'})

        # ---------------------------------------------------------
        # Dimension 3: Projects & Portfolio (20 pts)
        # ---------------------------------------------------------
        projects_count = len(profile.projects or [])
        if projects_count >= 2:
            projects_score = 20.0
        elif projects_count == 1:
            projects_score = 12.0
        else:
            projects_score = 0.0

        # ---------------------------------------------------------
        # Dimension 4: Professional Certifications (10 pts)
        # ---------------------------------------------------------
        certs_count = len(profile.certifications or [])
        if certs_count >= 2:
            certs_score = 10.0
        elif certs_count == 1:
            certs_score = 6.0
        else:
            certs_score = 0.0

        # ---------------------------------------------------------
        # Dimension 5: DSA Readiness (15 pts)
        # ---------------------------------------------------------
        dsa_score = 0.0
        for s_name, s_level in student_skill_map.items():
            if any(k in s_name for k in ['dsa', 'data structures', 'algorithms', 'problem solving', 'c++', 'java']):
                if s_level == 'Advanced':
                    dsa_score = max(dsa_score, 15.0)
                elif s_level == 'Intermediate':
                    dsa_score = max(dsa_score, 11.0)
                else:
                    dsa_score = max(dsa_score, 7.0)

        # ---------------------------------------------------------
        # Dimension 6: Profile & Professional Links (15 pts)
        # ---------------------------------------------------------
        profile_score = 0.0
        if profile.resume_url:
            profile_score += 5.0
        if profile.github_url:
            profile_score += 4.0
        if profile.linkedin_url:
            profile_score += 3.0
        if profile.bio or profile.headline:
            profile_score += 3.0

        total_readiness = round(academic_score + skills_score + projects_score + certs_score + dsa_score + profile_score)
        total_readiness = max(0, min(100, total_readiness))

        return {
            'target_role': matched_role,
            'readiness_score': total_readiness,
            'benchmark_skills': benchmark_skills,
            'acquired_skills': acquired_skills,
            'missing_skills': missing_skills,
            'additional_skills': additional_skills,
            'all_roles': list(CAREER_ROLE_REQUIREMENTS.keys()),
            'dimensions': {
                'academic_score': round(academic_score, 1),
                'skills_score': round(skills_score, 1),
                'projects_score': round(projects_score, 1),
                'certifications_score': round(certs_score, 1),
                'dsa_score': round(dsa_score, 1),
                'profile_score': round(profile_score, 1)
            }
        }

    @staticmethod
    def get_roadmap_for_role(role_name: str, user_id: int) -> dict:
        """
        Retrieves custom milestone roadmap for specified career role
        and enhances each stage with the student's persistent progress from DB.
        """
        # Match closest available roadmap
        matched_role = "Full Stack Developer"
        for key in ROADMAP_DEFINITIONS:
            if key.lower() in role_name.lower() or role_name.lower() in key.lower():
                matched_role = key
                break

        stages = ROADMAP_DEFINITIONS[matched_role]
        
        # Load user saved progress
        progress_records = RoadmapProgress.query.filter_by(user_id=user_id).all()
        user_progress_map = {p.roadmap_item: p.completed for p in progress_records}

        enhanced_stages = []
        completed_count = 0
        for stage in stages:
            is_done = user_progress_map.get(stage['id'], False)
            if is_done:
                completed_count += 1
            enhanced_stages.append({
                **stage,
                'completed': is_done
            })

        total_stages = len(stages)
        progress_percent = round((completed_count / total_stages) * 100) if total_stages > 0 else 0

        return {
            'role': matched_role,
            'stages': enhanced_stages,
            'total_stages': total_stages,
            'completed_count': completed_count,
            'progress_percent': progress_percent,
            'all_available_roles': list(ROADMAP_DEFINITIONS.keys())
        }

    @staticmethod
    def toggle_stage_progress(user_id: int, stage_id: str, career_role: str = 'Full Stack Developer', completed: bool | None = None) -> dict:
        stage_id = str(stage_id).strip()
        record = RoadmapProgress.query.filter_by(user_id=user_id, roadmap_item=stage_id).first()

        if record:
            if completed is not None:
                record.completed = completed
            else:
                record.completed = not record.completed
        else:
            record = RoadmapProgress(
                user_id=user_id,
                roadmap_item=stage_id,
                career_role=career_role,
                completed=completed if completed is not None else True
            )
            db.session.add(record)

        db.session.commit()

        # Recalculate roadmap stats
        roadmap_data = CareerService.get_roadmap_for_role(career_role, user_id)
        return {
            'stage_id': stage_id,
            'completed': record.completed,
            'progress_percent': roadmap_data['progress_percent'],
            'completed_count': roadmap_data['completed_count'],
            'total_stages': roadmap_data['total_stages']
        }
