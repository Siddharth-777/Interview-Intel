# Hand-written question pools per topic.
# Each entry: (weight, [phrasing_1, phrasing_2, ...])
# Higher weight = more likely to be selected (simulates common interview questions).
# Multiple phrasings of the same question create deliberate near-duplicates.

DSA: list[tuple[int, list[str]]] = [
    (
        4,
        [
            "Reverse a linked list",
            "Write a function to reverse a singly linked list",
            "Implement linked list reversal in-place",
        ],
    ),
    (
        4,
        [
            "Two Sum problem",
            "Given an array, find two numbers that add up to a target",
            "Find a pair of elements whose sum equals a given value",
        ],
    ),
    (
        3,
        [
            "Detect a cycle in a linked list",
            "How to find if a linked list has a loop?",
            "Implement Floyd's cycle detection algorithm",
        ],
    ),
    (
        3,
        [
            "Find the maximum subarray sum",
            "Kadane's algorithm implementation",
            "Given an array, find the contiguous subarray with the largest sum",
        ],
    ),
    (
        3,
        [
            "Merge two sorted arrays",
            "How to merge two sorted arrays efficiently?",
            "Combine two sorted arrays into a single sorted array",
        ],
    ),
    (
        2,
        [
            "Level order traversal of a binary tree",
            "BFS traversal of a binary tree",
            "Print binary tree nodes level by level",
        ],
    ),
    (
        2,
        [
            "Lowest common ancestor in a binary tree",
            "Find LCA of two nodes in a BST",
            "How to find the common ancestor of two tree nodes?",
        ],
    ),
    (
        2,
        [
            "Implement a stack using queues",
            "How to simulate a stack with two queues?",
            "Stack implementation using queue data structure",
        ],
    ),
    (
        3,
        [
            "Sort an array of 0s, 1s, and 2s",
            "Dutch National Flag problem",
            "Segregate 0s 1s and 2s in an array in one pass",
        ],
    ),
    (
        2,
        [
            "Find the longest palindromic substring",
            "Given a string, find its longest palindrome",
            "Longest palindrome in a string using dynamic programming",
        ],
    ),
    (
        2,
        [
            "Check if a binary tree is balanced",
            "Determine whether a binary tree is height-balanced",
            "Write code to check if a tree is AVL-balanced",
        ],
    ),
    (
        2,
        [
            "Implement BFS and DFS for a graph",
            "Graph traversal using BFS and DFS",
            "Write breadth-first and depth-first search algorithms",
        ],
    ),
    (
        1,
        [
            "Find the shortest path in a weighted graph",
            "Dijkstra's algorithm implementation",
            "Compute shortest path using Dijkstra's",
        ],
    ),
    (
        2,
        [
            "Coin change problem",
            "Minimum number of coins to make a given sum",
            "DP solution for the coin change problem",
        ],
    ),
    (
        2,
        [
            "Find the kth largest element in an array",
            "Kth largest element using quickselect or heap",
            "How to find the k-th biggest number in an unsorted array?",
        ],
    ),
    (
        1,
        [
            "Trapping rain water problem",
            "Calculate how much water can be trapped between bars",
            "Trapping rainwater using two-pointer approach",
        ],
    ),
    (
        2,
        [
            "Check if a string has valid parentheses",
            "Valid parentheses / balanced brackets problem",
            "Given a string of brackets, check if it is balanced",
        ],
    ),
]

SQL: list[tuple[int, list[str]]] = [
    (
        4,
        [
            "Find the second highest salary",
            "Write a query to get the 2nd highest salary from the employee table",
            "Query to find second maximum salary",
        ],
    ),
    (
        3,
        [
            "Difference between WHERE and HAVING",
            "When do you use HAVING vs WHERE?",
            "Explain WHERE vs HAVING clause with examples",
        ],
    ),
    (
        3,
        [
            "Explain different types of JOINs",
            "What are INNER JOIN, LEFT JOIN, RIGHT JOIN, FULL JOIN?",
            "Write queries showing different SQL join types",
        ],
    ),
    (
        2,
        [
            "Write a self-join query",
            "Explain self join with an example",
            "How does a self join work? Demonstrate with a query",
        ],
    ),
    (
        2,
        [
            "Explain window functions",
            "What are SQL window functions? Give examples of ROW_NUMBER and RANK",
            "Demonstrate RANK, DENSE_RANK and ROW_NUMBER",
        ],
    ),
    (
        3,
        [
            "Database normalization up to 3NF",
            "Explain 1NF, 2NF, 3NF with examples",
            "What is normalization and why is it important?",
        ],
    ),
    (
        2,
        [
            "How do indexes improve query performance?",
            "When should you create an index on a column?",
            "Explain clustered vs non-clustered indexes",
        ],
    ),
    (
        1,
        [
            "Write a query using GROUP BY with aggregate functions",
            "Demonstrate COUNT, SUM, AVG with GROUP BY",
            "Aggregate functions and GROUP BY clause examples",
        ],
    ),
]

OOP: list[tuple[int, list[str]]] = [
    (
        4,
        [
            "Explain the four pillars of OOP",
            "What are the main principles of object-oriented programming?",
            "Describe encapsulation, inheritance, polymorphism, and abstraction",
        ],
    ),
    (
        3,
        [
            "What is polymorphism? Give an example",
            "Explain runtime vs compile-time polymorphism",
            "Demonstrate polymorphism with a code example",
        ],
    ),
    (
        2,
        [
            "Explain SOLID principles",
            "What does SOLID stand for in software design?",
            "Describe each SOLID principle with real-world examples",
        ],
    ),
    (
        3,
        [
            "Difference between abstract class and interface",
            "When to use abstract class vs interface?",
            "Abstract class vs interface - explain with a use case",
        ],
    ),
    (
        2,
        [
            "Explain design patterns you have used",
            "What are Singleton and Factory patterns?",
            "Describe common design patterns with examples",
        ],
    ),
    (
        2,
        [
            "What is encapsulation and why is it important?",
            "Explain data hiding and encapsulation in OOP",
            "How does encapsulation help maintain code quality?",
        ],
    ),
    (
        2,
        [
            "What is inheritance? Explain types of inheritance",
            "Single vs multiple inheritance - what does your language support?",
            "Demonstrate inheritance with a class hierarchy example",
        ],
    ),
]

SYSTEM_DESIGN: list[tuple[int, list[str]]] = [
    (
        3,
        [
            "Design a URL shortener like bit.ly",
            "How would you design a URL shortening service?",
            "System design for TinyURL",
        ],
    ),
    (
        2,
        [
            "Design a chat application",
            "How would you design a real-time messaging app like WhatsApp?",
            "System design for a chat system",
        ],
    ),
    (
        2,
        [
            "Design a rate limiter",
            "How would you implement API rate limiting?",
            "System design for a distributed rate limiter",
        ],
    ),
    (
        2,
        [
            "Design a cache system",
            "How would you design a caching layer similar to Redis?",
            "System design for a distributed cache with eviction policies",
        ],
    ),
    (
        1,
        [
            "Design a notification service",
            "How would you build a push notification system at scale?",
            "System design for a notification delivery platform",
        ],
    ),
    (
        1,
        [
            "Design a file storage service like Google Drive",
            "How would you design Dropbox?",
            "System design for a cloud file storage and sync service",
        ],
    ),
    (
        1,
        [
            "Design a news feed system like Twitter",
            "How would you design a social media feed?",
            "System design for a timeline / feed generation service",
        ],
    ),
]

OS: list[tuple[int, list[str]]] = [
    (
        4,
        [
            "Explain process vs thread",
            "What is the difference between a process and a thread?",
            "Process vs thread - when to use which?",
        ],
    ),
    (
        3,
        [
            "What is a deadlock? How to prevent it?",
            "Explain the four necessary conditions for deadlock",
            "Deadlock detection and prevention strategies",
        ],
    ),
    (
        2,
        [
            "Explain virtual memory and paging",
            "How does virtual memory work?",
            "What is demand paging? Explain with an example",
        ],
    ),
    (
        2,
        [
            "CPU scheduling algorithms",
            "Compare Round Robin, SJF, and Priority scheduling",
            "Explain different OS scheduling algorithms with trade-offs",
        ],
    ),
    (
        2,
        [
            "What is a semaphore vs a mutex?",
            "Explain synchronization primitives in an OS",
            "How do semaphores and mutexes prevent race conditions?",
        ],
    ),
    (
        1,
        [
            "Explain memory management in an OS",
            "What are paging and segmentation?",
            "How does the OS manage physical and virtual memory?",
        ],
    ),
]

NETWORKS: list[tuple[int, list[str]]] = [
    (
        4,
        [
            "Explain TCP vs UDP",
            "What are the differences between TCP and UDP?",
            "When would you choose TCP over UDP?",
        ],
    ),
    (
        3,
        [
            "What happens when you type a URL in the browser?",
            "Explain DNS resolution and the HTTP request lifecycle",
            "Walk through the process of loading a webpage from URL entry",
        ],
    ),
    (
        2,
        [
            "Explain the OSI model layers",
            "Describe each layer of the OSI model",
            "What are the 7 layers of the OSI model and what do they do?",
        ],
    ),
    (
        2,
        [
            "What is REST? Explain RESTful API design principles",
            "Describe REST architecture and its constraints",
            "What makes an API truly RESTful?",
        ],
    ),
    (
        2,
        [
            "Explain HTTP methods and common status codes",
            "What are GET, POST, PUT, DELETE used for?",
            "Describe the meaning of 200, 301, 404, 500 status codes",
        ],
    ),
    (
        1,
        [
            "What is HTTPS and how does TLS work?",
            "Explain the SSL/TLS handshake process",
            "How does HTTPS secure communication?",
        ],
    ),
]

HR: list[tuple[int, list[str]]] = [
    (
        4,
        [
            "Tell me about yourself",
            "Walk me through your background",
            "Give me a brief introduction about yourself",
        ],
    ),
    (
        3,
        [
            "What are your strengths and weaknesses?",
            "Tell me about a weakness you are working on",
            "What do you consider your biggest strength?",
        ],
    ),
    (
        3,
        [
            "Why do you want to join this company?",
            "What attracts you to our organization?",
            "Why this company over others?",
        ],
    ),
    (
        2,
        [
            "Tell me about a challenging project you worked on",
            "Describe a difficult technical problem you solved",
            "What is the most complex project in your experience?",
        ],
    ),
    (
        2,
        [
            "Where do you see yourself in 5 years?",
            "What are your long-term career goals?",
            "How do you plan to grow in this role?",
        ],
    ),
    (
        2,
        [
            "How do you handle conflict in a team?",
            "Tell me about a time you disagreed with a teammate",
            "Describe how you resolved a team disagreement",
        ],
    ),
    (
        1,
        [
            "Why should we hire you?",
            "What makes you the right candidate for this position?",
            "What value will you bring to our team?",
        ],
    ),
]

APTITUDE: list[tuple[int, list[str]]] = [
    (
        3,
        [
            "Quantitative aptitude - percentages, ratios, averages",
            "Quant section with profit/loss, time-and-work, percentages",
            "Numerical ability questions on ratios, percentages, SI/CI",
        ],
    ),
    (
        3,
        [
            "Logical reasoning - puzzles and pattern recognition",
            "Logical section with seating arrangements, blood relations, coding-decoding",
            "Reasoning questions: series completion, syllogisms, arrangements",
        ],
    ),
    (
        2,
        [
            "Verbal ability - reading comprehension and grammar",
            "English section with RC passages, fill-in-the-blanks, para jumbles",
            "Verbal questions on grammar, vocabulary, sentence correction",
        ],
    ),
    (
        2,
        [
            "Data interpretation - charts and graphs",
            "DI section with bar charts, pie charts, tables",
            "Data interpretation questions on graphs and tabular data",
        ],
    ),
    (
        1,
        [
            "Coding aptitude - pseudocode and output prediction",
            "Programming MCQs on output tracing and basic logic",
            "Code snippets - predict the output questions",
        ],
    ),
]

QUESTION_POOLS: dict[str, list[tuple[int, list[str]]]] = {
    "dsa": DSA,
    "sql": SQL,
    "oop": OOP,
    "system_design": SYSTEM_DESIGN,
    "os": OS,
    "networks": NETWORKS,
    "hr": HR,
    "aptitude": APTITUDE,
}
