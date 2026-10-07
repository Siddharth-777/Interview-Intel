# Company round structures, role distributions, and experience counts.
# q_count: (min, max) questions to sample per round.
# topic_year_bias: multiplier applied to topic weight for a given year
#   (>1 = trending up, <1 = fading). Absent topics default to 1.0.

TOPIC_YEAR_BIAS: dict[str, dict[int, float]] = {
    "system_design": {2022: 0.4, 2023: 0.6, 2024: 1.0, 2025: 1.4},
    "aptitude": {2022: 1.3, 2023: 1.1, 2024: 0.9, 2025: 0.6},
    "hr": {2022: 0.8, 2023: 0.9, 2024: 1.0, 2025: 1.2},
}

ROLES = ["SDE", "Data Analyst", "QA", "DevOps", "Backend"]

COMPANIES: dict[str, dict] = {
    "TCS": {
        "rounds": [
            {"name": "Aptitude Test", "topics": ["aptitude"], "q_count": (3, 5)},
            {
                "name": "Technical Interview",
                "topics": ["dsa", "sql", "oop", "os"],
                "q_count": (3, 5),
            },
            {"name": "Managerial Interview", "topics": ["hr", "oop"], "q_count": (2, 3)},
            {"name": "HR Interview", "topics": ["hr"], "q_count": (2, 3)},
        ],
        "count": 22,
        "role_weights": {"SDE": 4, "Data Analyst": 2, "QA": 2, "DevOps": 1, "Backend": 2},
        "year_weights": {2022: 2, 2023: 3, 2024: 4, 2025: 3},
    },
    "Infosys": {
        "rounds": [
            {"name": "Online Test", "topics": ["aptitude", "dsa"], "q_count": (3, 5)},
            {
                "name": "Technical Interview",
                "topics": ["dsa", "sql", "oop", "os", "networks"],
                "q_count": (3, 5),
            },
            {"name": "HR Interview", "topics": ["hr"], "q_count": (2, 4)},
        ],
        "count": 20,
        "role_weights": {"SDE": 3, "Data Analyst": 3, "QA": 2, "DevOps": 1, "Backend": 2},
        "year_weights": {2022: 2, 2023: 3, 2024: 4, 2025: 3},
    },
    "Wipro": {
        "rounds": [
            {"name": "Aptitude Test", "topics": ["aptitude"], "q_count": (3, 4)},
            {"name": "Technical Interview", "topics": ["dsa", "sql", "oop"], "q_count": (3, 5)},
            {"name": "HR Interview", "topics": ["hr"], "q_count": (2, 3)},
        ],
        "count": 16,
        "role_weights": {"SDE": 3, "Data Analyst": 2, "QA": 3, "DevOps": 1, "Backend": 2},
        "year_weights": {2022: 3, 2023: 3, 2024: 3, 2025: 3},
    },
    "Zoho": {
        "rounds": [
            {"name": "Programming Round 1", "topics": ["dsa"], "q_count": (4, 6)},
            {"name": "Programming Round 2", "topics": ["dsa"], "q_count": (3, 4)},
            {
                "name": "Technical Discussion",
                "topics": ["oop", "os", "sql", "system_design"],
                "q_count": (3, 5),
            },
            {"name": "HR Interview", "topics": ["hr"], "q_count": (2, 3)},
        ],
        "count": 18,
        "role_weights": {"SDE": 5, "Backend": 4, "QA": 1, "Data Analyst": 1, "DevOps": 1},
        "year_weights": {2022: 2, 2023: 3, 2024: 4, 2025: 3},
    },
    "Freshworks": {
        "rounds": [
            {"name": "Coding Round", "topics": ["dsa"], "q_count": (3, 5)},
            {"name": "System Design Round", "topics": ["system_design"], "q_count": (1, 2)},
            {
                "name": "Technical Interview",
                "topics": ["dsa", "oop", "sql", "os"],
                "q_count": (3, 5),
            },
            {"name": "HR Interview", "topics": ["hr"], "q_count": (2, 3)},
        ],
        "count": 15,
        "role_weights": {"SDE": 4, "Backend": 4, "QA": 1, "Data Analyst": 1, "DevOps": 1},
        "year_weights": {2022: 2, 2023: 3, 2024: 4, 2025: 4},
    },
    "Amazon": {
        "rounds": [
            {"name": "Online Assessment", "topics": ["dsa"], "q_count": (2, 3)},
            {"name": "Phone Screen", "topics": ["dsa", "system_design"], "q_count": (2, 3)},
            {"name": "Onsite - Coding", "topics": ["dsa"], "q_count": (2, 3)},
            {"name": "Onsite - System Design", "topics": ["system_design"], "q_count": (1, 2)},
            {"name": "Behavioral / Bar Raiser", "topics": ["hr"], "q_count": (3, 5)},
        ],
        "count": 20,
        "role_weights": {"SDE": 5, "Backend": 3, "DevOps": 2, "Data Analyst": 1, "QA": 1},
        "year_weights": {2022: 2, 2023: 3, 2024: 4, 2025: 4},
    },
    "Microsoft": {
        "rounds": [
            {"name": "Online Test", "topics": ["dsa", "aptitude"], "q_count": (3, 5)},
            {"name": "Group Fly Round", "topics": ["dsa"], "q_count": (2, 3)},
            {"name": "Technical Interview 1", "topics": ["dsa", "oop", "os"], "q_count": (3, 4)},
            {
                "name": "Technical Interview 2",
                "topics": ["dsa", "system_design", "sql"],
                "q_count": (3, 4),
            },
            {"name": "HR Interview", "topics": ["hr"], "q_count": (2, 3)},
        ],
        "count": 18,
        "role_weights": {"SDE": 5, "Backend": 3, "DevOps": 1, "Data Analyst": 1, "QA": 1},
        "year_weights": {2022: 2, 2023: 3, 2024: 4, 2025: 4},
    },
    "Goldman Sachs": {
        "rounds": [
            {"name": "Online Assessment", "topics": ["dsa", "aptitude"], "q_count": (3, 5)},
            {
                "name": "Technical Interview",
                "topics": ["dsa", "sql", "os", "networks"],
                "q_count": (3, 5),
            },
            {"name": "System Design Round", "topics": ["system_design"], "q_count": (1, 2)},
            {"name": "HR Interview", "topics": ["hr"], "q_count": (2, 3)},
        ],
        "count": 15,
        "role_weights": {"SDE": 3, "Data Analyst": 3, "Backend": 3, "DevOps": 1, "QA": 1},
        "year_weights": {2022: 2, 2023: 3, 2024: 4, 2025: 3},
    },
    "Cognizant": {
        "rounds": [
            {"name": "Aptitude Test", "topics": ["aptitude"], "q_count": (3, 5)},
            {"name": "Technical Interview", "topics": ["dsa", "sql", "oop"], "q_count": (3, 5)},
            {"name": "HR Interview", "topics": ["hr"], "q_count": (2, 3)},
        ],
        "count": 16,
        "role_weights": {"SDE": 3, "Data Analyst": 2, "QA": 3, "DevOps": 2, "Backend": 2},
        "year_weights": {2022: 3, 2023: 3, 2024: 3, 2025: 3},
    },
    "Accenture": {
        "rounds": [
            {"name": "Aptitude & Communication Test", "topics": ["aptitude"], "q_count": (3, 5)},
            {
                "name": "Technical Interview",
                "topics": ["dsa", "sql", "oop", "networks"],
                "q_count": (3, 5),
            },
            {"name": "HR Interview", "topics": ["hr"], "q_count": (2, 3)},
        ],
        "count": 18,
        "role_weights": {"SDE": 3, "Data Analyst": 2, "QA": 2, "DevOps": 2, "Backend": 2},
        "year_weights": {2022: 3, 2023: 3, 2024: 3, 2025: 3},
    },
    "Flipkart": {
        "rounds": [
            {"name": "Machine Coding Round", "topics": ["dsa", "oop"], "q_count": (1, 2)},
            {"name": "Problem Solving Round", "topics": ["dsa"], "q_count": (2, 3)},
            {"name": "System Design Round", "topics": ["system_design"], "q_count": (1, 2)},
            {"name": "Hiring Manager Round", "topics": ["hr", "system_design"], "q_count": (2, 4)},
        ],
        "count": 15,
        "role_weights": {"SDE": 5, "Backend": 4, "DevOps": 1, "Data Analyst": 1, "QA": 1},
        "year_weights": {2022: 2, 2023: 3, 2024: 4, 2025: 4},
    },
    "Razorpay": {
        "rounds": [
            {"name": "Coding Round", "topics": ["dsa"], "q_count": (2, 3)},
            {
                "name": "System Design Discussion",
                "topics": ["system_design", "oop"],
                "q_count": (2, 3),
            },
            {"name": "Hiring Manager Round", "topics": ["hr"], "q_count": (2, 3)},
        ],
        "count": 2,
        "role_weights": {"SDE": 1, "Backend": 1},
        "year_weights": {2024: 1, 2025: 1},
    },
}
