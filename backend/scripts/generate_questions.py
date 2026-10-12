import json
from pathlib import Path
from datetime import datetime, timedelta
import random

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Run career profiles generator first
import generate_seed_data

# ==============================================================================
# 2. SKILL ASSESSMENTS (8 Categories x 3 Difficulties x 5+ Questions)
# ==============================================================================
CATEGORIES = [
    "Python",
    "SQL",
    "DSA",
    "DBMS",
    "OOP",
    "Web",
    "Statistics/Data Analysis",
    "Problem Solving"
]

DIFFICULTIES = ["Beginner", "Intermediate", "Advanced"]

# Question bank definitions
QUESTIONS = []

def add_q(category, difficulty, q_text, options, ans, topic, explanation, q_type="multiple_choice", code_starter=None, test_cases=None):
    QUESTIONS.append({
        "category": category,
        "difficulty": difficulty,
        "question_type": q_type,
        "question_text": q_text,
        "options": options,
        "correct_answer": ans,
        "topic_tag": topic,
        "explanation": explanation,
        "code_starter": code_starter,
        "test_cases_or_rubric": test_cases
    })

# --- PYTHON QUESTIONS ---
# Beginner
add_q("Python", "Beginner", "Which of the following data structures is immutable in Python?",
      ["List", "Dictionary", "Tuple", "Set"], "Tuple", "Python Fundamentals",
      "Tuples cannot be modified after creation, making them immutable sequences.")
add_q("Python", "Beginner", "What is the output of `type([])` in Python?",
      ["<class 'tuple'>", "<class 'list'>", "<class 'array'>", "<class 'dict'>"], "<class 'list'>", "Data Types",
      "Empty square brackets `[]` create a list instance.")
add_q("Python", "Beginner", "Which keyword is used to handle exceptions in Python?",
      ["catch", "try", "except", "error"], "except", "Error Handling",
      "In Python, errors raised in a `try` block are intercepted by `except` blocks.")
add_q("Python", "Beginner", "How do you define a function in Python?",
      ["function myFunc():", "def myFunc():", "func myFunc():", "define myFunc():"], "def myFunc():", "Functions",
      "The `def` keyword declares a function signature in Python.")
add_q("Python", "Beginner", "What does the `len()` function return for a string 'SkillForage'?",
      ["10", "11", "12", "9"], "11", "String Methods",
      "'SkillForage' contains 11 characters.")

# Intermediate
add_q("Python", "Intermediate", "What does a generator function return when called with `yield`?",
      ["A list of values", "A generator object (iterator)", "A tuple", "None"], "A generator object (iterator)", "Generators & Iterators",
      "Functions containing `yield` return a generator iterator that computes values on demand.")
add_q("Python", "Intermediate", "What is the difference between `==` and `is` in Python?",
      ["No difference", "`==` checks value equality, while `is` checks identity (memory location)", "`is` checks value, `==` checks memory", "`is` is only for numbers"],
      "`==` checks value equality, while `is` checks identity (memory location)", "Memory & Identity",
      "`==` evaluates equality of values, whereas `is` evaluates if two variables refer to the exact same object in memory.")
add_q("Python", "Intermediate", "What is the time complexity of looking up a key in a Python dictionary?",
      ["O(n)", "O(log n)", "O(1) on average", "O(n log n)"], "O(1) on average", "Time Complexity",
      "Python dictionaries are implemented using hash tables, offering O(1) average lookup time.")
add_q("Python", "Intermediate", "What does the `@property` decorator do in a class?",
      ["Makes a method static", "Allows accessing a method as an attribute getter", "Protects a method from inheritance", "Transforms a class into a singleton"],
      "Allows accessing a method as an attribute getter", "Decorators & OOP",
      "`@property` turns an instance method into a read-only property attribute getter.")
add_q("Python", "Intermediate", "Implement a function `count_vowels(s)` that counts vowels (a, e, i, o, u) case-insensitively.",
      ["4", "5", "6", "3"], "5", "Practical Task",
      "Iterating through the lowercase string and counting matches in 'aeiou' returns 5 for 'Interview Ready'.",
      q_type="practical_task",
      code_starter="def count_vowels(s: str) -> int:\n    # Return number of vowels\n    return sum(1 for c in s.lower() if c in 'aeiou')",
      test_cases=[{"input": "Interview Ready", "expected": 5}, {"input": "SkillForage", "expected": 4}])

# Advanced
add_q("Python", "Advanced", "What is the Global Interpreter Lock (GIL) in CPython?",
      ["A lock preventing memory leaks", "A mutex that prevents multiple native threads from executing Python bytecodes at once", "A compiler optimization for loops", "A security sandbox"],
      "A mutex that prevents multiple native threads from executing Python bytecodes at once", "Concurrency & Internals",
      "The GIL ensures thread safety by allowing only one native OS thread to run Python bytecodes simultaneously within a single CPython process.")
add_q("Python", "Advanced", "What are `*args` and `**kwargs` in function signatures?",
      ["Positional arguments list and keyword arguments dictionary", "Pointers and double pointers", "Multiplication and power operators", "Tuple unpacked variables only"],
      "Positional arguments list and keyword arguments dictionary", "Metaprogramming",
      "`*args` gathers excess positional arguments into a tuple, while `**kwargs` gathers excess keyword arguments into a dictionary.")
add_q("Python", "Advanced", "Which metaclass method controls the creation of a new class object?",
      ["__init__", "__call__", "__new__", "__prepare__"], "__new__", "Metaclasses",
      "`__new__` is the constructor that creates and returns the class object instance before `__init__` initializes it.")
add_q("Python", "Advanced", "What does `asyncio.gather()` do in asynchronous Python?",
      ["Runs coroutines sequentially", "Runs multiple awaitable objects concurrently and aggregates their results", "Kills background threads", "Spawns new subprocesses"],
      "Runs multiple awaitable objects concurrently and aggregates their results", "AsyncIO",
      "`asyncio.gather()` takes multiple awaitables, schedules them as concurrent tasks, and returns a list of results in order.")
add_q("Python", "Advanced", "In Python memory management, how does the garbage collector handle cyclic references?",
      ["Reference counting alone", "Generational cyclic garbage collector using doubly linked lists", "Manual freeing", "It never cleans cyclic references"],
      "Generational cyclic garbage collector using doubly linked lists", "Memory Management",
      "CPython supplements reference counting with a generational cyclic garbage collector that detects and cleans isolated reference loops.")

# --- SQL QUESTIONS ---
# Beginner
add_q("SQL", "Beginner", "Which SQL clause is used to filter records returned by a SELECT statement?",
      ["ORDER BY", "GROUP BY", "WHERE", "LIMIT"], "WHERE", "Basic Queries",
      "The `WHERE` clause specifies search conditions to filter rows.")
add_q("SQL", "Beginner", "Which SQL command deletes all records from a table without removing table structure?",
      ["DROP", "REMOVE", "TRUNCATE", "ALTER"], "TRUNCATE", "DDL/DML",
      "`TRUNCATE TABLE` empties table rows while retaining table columns, constraints, and indexes.")
add_q("SQL", "Beginner", "Which function calculates the average value of a numeric column in SQL?",
      ["SUM()", "COUNT()", "AVG()", "MEAN()"], "AVG()", "Aggregate Functions",
      "`AVG(column)` computes the arithmetic mean of non-null values.")
add_q("SQL", "Beginner", "How do you select distinct values from a column named `city`?",
      ["SELECT UNIQUE city FROM users;", "SELECT DISTINCT city FROM users;", "SELECT DIFFERENT city FROM users;", "SELECT FILTER city FROM users;"],
      "SELECT DISTINCT city FROM users;", "Basic Queries",
      "`SELECT DISTINCT` removes duplicate rows from the query output.")
add_q("SQL", "Beginner", "What is the primary purpose of a PRIMARY KEY in a relational table?",
      ["To format dates", "To uniquely identify each record and enforce non-null values", "To sort rows alphabetically", "To link foreign databases"],
      "To uniquely identify each record and enforce non-null values", "Constraints",
      "A PRIMARY KEY constraint enforces uniqueness and NOT NULL on identifying columns.")

# Intermediate
add_q("SQL", "Intermediate", "What is the difference between WHERE and HAVING in SQL?",
      ["No difference", "WHERE filters rows before aggregation; HAVING filters aggregated groups", "HAVING filters rows before aggregation; WHERE filters groups", "HAVING only works with strings"],
      "WHERE filters rows before aggregation; HAVING filters aggregated groups", "Aggregations",
      "`WHERE` evaluates row predicates prior to `GROUP BY`, whereas `HAVING` filters results after aggregate calculations.")
add_q("SQL", "Intermediate", "Which JOIN returns all rows from the left table and matching rows from the right table?",
      ["INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "CROSS JOIN"], "LEFT JOIN", "Joins",
      "A `LEFT OUTER JOIN` preserves all records from the left table, filling unmatched right columns with NULL.")
add_q("SQL", "Intermediate", "What will `ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary DESC)` do?",
      ["Sums salaries by department", "Assigns a sequential ranking integer starting at 1 for each employee in each department", "Deletes duplicates", "Sorts the whole table by department"],
      "Assigns a sequential ranking integer starting at 1 for each employee in each department", "Window Functions",
      "It partitions by department and numbers rows sequentially 1, 2, ... based on descending salary.")
add_q("SQL", "Intermediate", "What does an INDEX on a relational database column do?",
      ["Encrypts the column", "Creates a separate search tree data structure (like B-Tree) to speed up queries at the cost of slower writes", "Restricts value range", "Duplicates the whole table"],
      "Creates a separate search tree data structure (like B-Tree) to speed up queries at the cost of slower writes", "Performance Tuning",
      "Indexes use B-Trees or Hash indexes to quickly locate rows without scanning every row sequentially.")
add_q("SQL", "Intermediate", "Write an SQL query to find the second highest distinct salary from an `employees` table.",
      ["SELECT MAX(salary) FROM employees WHERE salary < (SELECT MAX(salary) FROM employees);",
       "SELECT salary FROM employees ORDER BY salary DESC LIMIT 2;",
       "SELECT DISTINCT salary FROM employees OFFSET 2;",
       "SELECT SECOND(salary) FROM employees;"],
      "SELECT MAX(salary) FROM employees WHERE salary < (SELECT MAX(salary) FROM employees);", "Practical Task",
      "The subquery gets the top salary, and the outer query takes the MAX of all salaries below it.",
      q_type="practical_task",
      code_starter="SELECT MAX(salary) AS second_highest FROM employees WHERE salary < (SELECT MAX(salary) FROM employees);")

# Advanced
add_q("SQL", "Advanced", "What are the four ANSI SQL transaction isolation levels in increasing order of strictness?",
      ["Read Uncommitted, Read Committed, Repeatable Read, Serializable",
       "Serializable, Read Committed, Repeatable Read, Read Uncommitted",
       "Snapshot, Repeatable Read, Read Committed, Serializable",
       "Atomic, Consistent, Isolated, Durable"],
      "Read Uncommitted, Read Committed, Repeatable Read, Serializable", "Transactions & ACID",
      "Read Uncommitted permits dirty reads; Serializable provides full mathematical serial consistency.")
add_q("SQL", "Advanced", "In PostgreSQL, what is the purpose of EXPLAIN ANALYZE?",
      ["Validates table schema syntax", "Executes the query and displays the actual execution plan with node-level runtime metrics", "Compiles query into C code", "Backs up query execution"],
      "Executes the query and displays the actual execution plan with node-level runtime metrics", "Query Optimization",
      "`EXPLAIN ANALYZE` executes the plan and shows estimated vs actual startup/total costs and row counts.")
add_q("SQL", "Advanced", "What is the difference between RANK() and DENSE_RANK() window functions?",
      ["RANK leaves gaps in numbering after ties; DENSE_RANK assigns consecutive numbers without gaps",
       "DENSE_RANK leaves gaps; RANK does not",
       "RANK works only on numbers; DENSE_RANK works on text",
       "They are aliases of each other"],
      "RANK leaves gaps in numbering after ties; DENSE_RANK assigns consecutive numbers without gaps", "Window Functions",
      "If two rows tie for rank 1, RANK assigns rank 3 to the next row, while DENSE_RANK assigns rank 2.")
add_q("SQL", "Advanced", "What is a Common Table Expression (CTE) and recursive CTE used for?",
      ["Creating temporary named result sets, useful for hierarchical or graph traversal queries",
       "Creating permanent physical views",
       "Dropping cyclic dependencies",
       "Replacing foreign keys"],
      "Creating temporary named result sets, useful for hierarchical or graph traversal queries", "Advanced SQL",
      "`WITH` clause CTEs enhance readability, and recursive CTEs enable traversals of trees and graphs.")
add_q("SQL", "Advanced", "What phenomenon occurs in Repeatable Read isolation level that is prevented by Serializable?",
      ["Dirty read", "Non-repeatable read", "Phantom read", "Write skew / Serialization anomaly"],
      "Write skew / Serialization anomaly", "Concurrency Anomalies",
      "Repeatable Read prevents dirty and non-repeatable reads; serializable isolation prevents phantom inserts and write skew anomalies.")

# --- DSA QUESTIONS ---
# Beginner
add_q("DSA", "Beginner", "Which data structure operates on a Last-In-First-Out (LIFO) basis?",
      ["Queue", "Stack", "Binary Search Tree", "Linked List"], "Stack", "Data Structures",
      "A Stack pushes and pops elements from the top (LIFO).")
add_q("DSA", "Beginner", "What is the best-case time complexity of linear search?",
      ["O(n)", "O(log n)", "O(1)", "O(n^2)"], "O(1)", "Searching Algorithms",
      "When the target item is at the very first index, linear search terminates in O(1) time.")
add_q("DSA", "Beginner", "Which node in a tree has no parent?",
      ["Leaf node", "Root node", "Sibling node", "Internal node"], "Root node", "Trees",
      "The root node is the topmost node in a tree hierarchy without parent links.")
add_q("DSA", "Beginner", "What is the time complexity to insert an element at the end of a dynamic array (amortized)?",
      ["O(n)", "O(1)", "O(log n)", "O(n^2)"], "O(1)", "Arrays",
      "Appending to a dynamic array takes amortized O(1) time despite occasional O(n) reallocations.")
add_q("DSA", "Beginner", "Which sorting algorithm repeatedly swaps adjacent elements if they are in the wrong order?",
      ["Merge Sort", "Bubble Sort", "Quick Sort", "Heap Sort"], "Bubble Sort", "Sorting Algorithms",
      "Bubble Sort steps through the list, comparing and swapping adjacent items.")

# Intermediate
add_q("DSA", "Intermediate", "What is the average time complexity of QuickSort?",
      ["O(n)", "O(n log n)", "O(n^2)", "O(log n)"], "O(n log n)", "Sorting",
      "QuickSort divides the array by a pivot, achieving O(n log n) average running time.")
add_q("DSA", "Intermediate", "In a balanced Binary Search Tree (AVL or Red-Black), what is the search time complexity for n nodes?",
      ["O(n)", "O(log n)", "O(1)", "O(n log n)"], "O(log n)", "Trees",
      "Because height is maintained at O(log n), search, insert, and delete are all bounded by O(log n).")
add_q("DSA", "Intermediate", "Which algorithm is used to find the shortest path in a graph with non-negative edge weights?",
      ["Breadth First Search (BFS)", "Dijkstra's Algorithm", "Kruskal's Algorithm", "Floyd-Warshall Algorithm"],
      "Dijkstra's Algorithm", "Graph Algorithms",
      "Dijkstra's greedy algorithm using a priority queue finds single-source shortest paths in O((V + E) log V).")
add_q("DSA", "Intermediate", "How do you detect a cycle in a singly linked list with O(1) auxiliary space?",
      ["Hash Set of visited nodes", "Floyd's Cycle-Finding Algorithm (Tortoise and Hare pointer approach)", "Reverse the list", "Count nodes up to infinity"],
      "Floyd's Cycle-Finding Algorithm (Tortoise and Hare pointer approach)", "Linked Lists",
      "A slow pointer moves 1 step and a fast pointer moves 2 steps; if a cycle exists, they must meet.")
add_q("DSA", "Intermediate", "Solve Two Sum: Find indices of two numbers in an array that add up to a target using a Hash Map.",
      ["O(n^2) time, O(1) space", "O(n) time, O(n) space", "O(n log n) time, O(1) space", "O(1) time, O(n) space"],
      "O(n) time, O(n) space", "Practical Task",
      "Using a hash map to store complements allows single-pass O(n) lookup.",
      q_type="practical_task",
      code_starter="def two_sum(nums, target):\n    seen = {}\n    for i, num in enumerate(nums):\n        diff = target - num\n        if diff in seen:\n            return [seen[diff], i]\n        seen[num] = i\n    return []")

# Advanced
add_q("DSA", "Advanced", "What is the time complexity of building a heap from an unsorted array of n elements?",
      ["O(n log n)", "O(n)", "O(log n)", "O(n^2)"], "O(n)", "Heaps",
      "Bottom-up heap construction (sift-down on all non-leaf nodes) sums to O(n) mathematically.")
add_q("DSA", "Advanced", "What data structure supports amortized O(1) Union and Find operations with path compression?",
      ["Disjoint Set Union (DSU / Union-Find)", "Segment Tree", "Fenwick Tree", "Trie"],
      "Disjoint Set Union (DSU / Union-Find)", "Advanced Data Structures",
      "DSU with union-by-rank and path compression operates in nearly O(1) time using the inverse Ackermann function.")
add_q("DSA", "Advanced", "In dynamic programming, what is the difference between top-down and bottom-up approaches?",
      ["Top-down uses memoization with recursion; bottom-up uses tabulation iteratively",
       "Bottom-up uses recursion; top-down uses loops",
       "Top-down requires O(n^3); bottom-up is always O(1)",
       "No difference"],
      "Top-down uses memoization with recursion; bottom-up uses tabulation iteratively", "Dynamic Programming",
      "Top-down solves subproblems recursively as requested, while bottom-up builds answers from base cases upwards.")
add_q("DSA", "Advanced", "What algorithm computes Strongly Connected Components (SCCs) in a directed graph in linear O(V + E) time?",
      ["Tarjan's or Kosaraju's algorithm", "Bellman-Ford algorithm", "Prim's algorithm", "Ford-Fulkerson algorithm"],
      "Tarjan's or Kosaraju's algorithm", "Graph Theory",
      "Tarjan's algorithm uses DFS traversal with low-link values to find all SCCs in a single pass.")
add_q("DSA", "Advanced", "What data structure is optimal for range sum queries with point updates in O(log n) time?",
      ["Binary Indexed Tree (Fenwick Tree) or Segment Tree", "Array", "Linked List", "Hash Table"],
      "Binary Indexed Tree (Fenwick Tree) or Segment Tree", "Range Queries",
      "Both Fenwick and Segment trees allow O(log n) prefix updates and queries.")

# --- DBMS QUESTIONS ---
# Beginner
add_q("DBMS", "Beginner", "What does ACID stand for in database management systems?",
      ["Atomicity, Consistency, Isolation, Durability",
       "Accuracy, Completeness, Integrity, Durability",
       "Authentication, Concurrency, Isolation, Distribution",
       "Access, Control, Indexing, Data"],
      "Atomicity, Consistency, Isolation, Durability", "ACID Properties",
      "ACID defines the foundational transactional guarantees in relational database systems.")
add_q("DBMS", "Beginner", "Which normal form removes partial dependency on composite primary keys?",
      ["First Normal Form (1NF)", "Second Normal Form (2NF)", "Third Normal Form (3NF)", "Boyce-Codd Normal Form (BCNF)"],
      "Second Normal Form (2NF)", "Normalization",
      "2NF requires 1NF compliance and that non-key attributes depend on the complete primary key.")
add_q("DBMS", "Beginner", "What is a Foreign Key?",
      ["A key generated outside the system", "A column that references the primary key of another table", "A password hash", "An unindexed unique column"],
      "A column that references the primary key of another table", "Relational Integrity",
      "Foreign keys enforce referential integrity between connected tables.")
add_q("DBMS", "Beginner", "Which of the following is a non-relational (NoSQL) database?",
      ["PostgreSQL", "MySQL", "MongoDB", "SQLite"], "MongoDB", "Database Types",
      "MongoDB stores data as BSON documents rather than relational tables.")
add_q("DBMS", "Beginner", "What does DDL stand for in SQL?",
      ["Data Definition Language", "Data Distribution Level", "Dynamic Data Logic", "Direct Data Link"],
      "Data Definition Language", "SQL Categories",
      "DDL includes commands that define schema structure (CREATE, ALTER, DROP, TRUNCATE).")

# Intermediate
add_q("DBMS", "Intermediate", "What condition must be satisfied for a relation to be in 3NF?",
      ["It must be in 2NF and contain no transitive functional dependencies",
       "It must have only atomic values",
       "It must have no foreign keys",
       "All columns must be numbers"],
      "It must be in 2NF and contain no transitive functional dependencies", "Normalization",
      "3NF eliminates dependencies where a non-prime attribute depends on another non-prime attribute.")
add_q("DBMS", "Intermediate", "What is the difference between optimistic and pessimistic concurrency control?",
      ["Optimistic assumes conflicts are rare and validates at commit; pessimistic locks resources in advance",
       "Optimistic uses locks; pessimistic uses timestamps",
       "Optimistic is only for NoSQL; pessimistic is for SQL",
       "No difference"],
      "Optimistic assumes conflicts are rare and validates at commit; pessimistic locks resources in advance", "Concurrency Control",
      "Pessimistic locking prevents concurrent access (SELECT FOR UPDATE); optimistic concurrency checks version numbers.")
add_q("DBMS", "Intermediate", "What is Write-Ahead Logging (WAL) in database engines?",
      ["Writing debug logs to disk", "A technique where changes are recorded on durable storage before being applied to data pages", "Encrypting database transactions", "Writing user queries to history"],
      "A technique where changes are recorded on durable storage before being applied to data pages", "Storage & Recovery",
      "WAL guarantees durability by flushing log records before memory buffers update disk pages.")
add_q("DBMS", "Intermediate", "What is the difference between a clustered and non-clustered index?",
      ["Clustered index dictates physical storage order of rows; non-clustered creates an auxiliary lookup structure",
       "Non-clustered dictates physical storage order; clustered is auxiliary",
       "Clustered indexes are slower than non-clustered",
       "Clustered indexes cannot be used on primary keys"],
      "Clustered index dictates physical storage order of rows; non-clustered creates an auxiliary lookup structure", "Indexing",
      "A table can have only one clustered index because rows can be physically ordered in only one way.")
add_q("DBMS", "Intermediate", "Identify the foreign key constraint syntax that automatically deletes child records when parent is deleted.",
      ["ON DELETE RESTRICT", "ON DELETE CASCADE", "ON DELETE SET NULL", "ON DELETE NO ACTION"],
      "ON DELETE CASCADE", "Practical Task",
      "CASCADE propagates delete actions from referenced parent records to dependent children.",
      q_type="practical_task",
      code_starter="CREATE TABLE orders (\n    id INT PRIMARY KEY,\n    user_id INT,\n    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE\n);")

# Advanced
add_q("DBMS", "Advanced", "What does the CAP theorem state regarding distributed data stores?",
      ["A distributed system can guarantee at most two out of Consistency, Availability, and Partition Tolerance",
       "All systems must be ACID compliant",
       "Consistency is always guaranteed across distributed clouds",
       "Performance scales linearly with nodes"],
      "A distributed system can guarantee at most two out of Consistency, Availability, and Partition Tolerance", "Distributed Systems",
      "In the presence of network partitions (P), a distributed system must choose between Consistency (C) and Availability (A).")
add_q("DBMS", "Advanced", "In Multi-Version Concurrency Control (MVCC), how do read transactions avoid blocking write transactions?",
      ["By locking the entire table", "By reading an immutable snapshot/version of data corresponding to the transaction start time", "By caching in browser memory", "By delaying writes until reads finish"],
      "By reading an immutable snapshot/version of data corresponding to the transaction start time", "MVCC & Internals",
      "MVCC generates row versions with transaction IDs, so readers see a consistent view without taking read locks.")
add_q("DBMS", "Advanced", "What is Two-Phase Locking (2PL) and what does strict 2PL guarantee?",
      ["Growing phase (acquiring locks) and shrinking phase (releasing locks); strict 2PL holds exclusive locks until commit to ensure serializability and avoid cascading aborts",
       "A protocol for replicating databases across two servers",
       "A method to encrypt passwords in two passes",
       "A sorting algorithm for B-Trees"],
      "Growing phase (acquiring locks) and shrinking phase (releasing locks); strict 2PL holds exclusive locks until commit to ensure serializability and avoid cascading aborts", "Transactions",
      "Strict 2PL prevents cascading aborts by holding all locks until transaction completion.")
add_q("DBMS", "Advanced", "How does a B+ Tree differ from a standard B Tree?",
      ["In a B+ Tree, data pointers are stored only in leaf nodes, and leaf nodes are linked sequentially for fast range scans",
       "B+ Trees have no leaf nodes",
       "Standard B Trees do not allow balancing",
       "B+ Trees are strictly binary"],
      "In a B+ Tree, data pointers are stored only in leaf nodes, and leaf nodes are linked sequentially for fast range scans", "Storage Engines",
      "B+ tree internal nodes contain only routing keys; leaves store all data records and link to each other for sequential iteration.")
add_q("DBMS", "Advanced", "What is database sharding and how does consistent hashing improve it?",
      ["Horizontal partitioning across nodes; consistent hashing minimizes key remapping when nodes are added or removed",
       "Vertical column splitting; consistent hashing encrypts data",
       "Backing up data to S3; consistent hashing compresses files",
       "Creating read replicas; consistent hashing balances CPU"],
      "Horizontal partitioning across nodes; consistent hashing minimizes key remapping when nodes are added or removed", "Scaling",
      "Consistent hashing maps nodes and keys onto a circular hash ring, requiring only k/N keys to move upon node resizing.")

# --- OOP QUESTIONS ---
# Beginner
add_q("OOP", "Beginner", "What are the four core pillars of Object-Oriented Programming?",
      ["Encapsulation, Inheritance, Polymorphism, Abstraction",
       "Variables, Loops, Functions, Classes",
       "Compilation, Interpretation, Execution, Debugging",
       "Modules, Packages, Libraries, Frameworks"],
      "Encapsulation, Inheritance, Polymorphism, Abstraction", "OOP Pillars",
      "These 4 concepts form the theoretical foundation of object-oriented architecture.")
add_q("OOP", "Beginner", "What is Encapsulation?",
      ["Inheriting from multiple parents", "Bundling data and methods that operate on that data, restricting direct access from outside", "Writing abstract methods", "Overloading operators"],
      "Bundling data and methods that operate on that data, restricting direct access from outside", "Encapsulation",
      "Encapsulation hides internal state and exposes safe interfaces via getters and setters.")
add_q("OOP", "Beginner", "What is an instance of a class called?",
      ["Function", "Object", "Module", "Variable"], "Object", "Classes & Objects",
      "An object is a concrete runtime instantiation of a class blueprint.")
add_q("OOP", "Beginner", "Which keyword is used by a child class to call a constructor of its parent class in Java and Python?",
      ["this / self", "super / super()", "base / parent", "extend / inherit"], "super / super()", "Inheritance",
      "`super()` provides access to parent class methods and constructors.")
add_q("OOP", "Beginner", "What is method overloading?",
      ["Multiple methods in the same class with the same name but different parameter signatures",
       "Redefining a method in a child class",
       "Deleting a method",
       "Calling a method too many times"],
      "Multiple methods in the same class with the same name but different parameter signatures", "Polymorphism",
      "Overloading allows multiple signatures for one method name resolved at compile/definition time.")

# Intermediate
add_q("OOP", "Intermediate", "What is method overriding in OOP?",
      ["Defining a method with the same name and signature in a child class to provide a specific implementation",
       "Calling a method with wrong arguments",
       "Declaring static variables",
       "Hiding private attributes"],
      "Defining a method with the same name and signature in a child class to provide a specific implementation", "Polymorphism",
      "Method overriding provides polymorphic runtime behavior based on the concrete object type.")
add_q("OOP", "Intermediate", "What is the difference between an Abstract Class and an Interface?",
      ["An abstract class can contain state (fields) and implemented methods; an interface defines contract specifications",
       "Interfaces cannot be implemented",
       "Abstract classes cannot have constructors",
       "They are completely identical"],
      "An abstract class can contain state (fields) and implemented methods; an interface defines contract specifications", "Design",
      "Abstract classes share common state and default logic, whereas interfaces prescribe public APIs.")
add_q("OOP", "Intermediate", "What does the 'S' in SOLID principles stand for?",
      ["Static Typing Principle", "Single Responsibility Principle (a class should have only one reason to change)", "Subclassing Principle", "Scope Principle"],
      "Single Responsibility Principle (a class should have only one reason to change)", "SOLID Principles",
      "Single Responsibility Principle asserts that every class should be accountable for a single functional slice.")
add_q("OOP", "Intermediate", "What is the Diamond Problem in multiple inheritance?",
      ["Ambiguity that arises when a child class inherits from two parent classes that both inherit from a single grandparent class",
       "A visual diagram styling issue",
       "A memory leak in pointers",
       "A compiler security bug"],
      "Ambiguity that arises when a child class inherits from two parent classes that both inherit from a single grandparent class", "Inheritance",
      "Languages resolve this using Method Resolution Order (MRO in Python) or prohibiting multiple class inheritance (Java).")
add_q("OOP", "Intermediate", "Implement the Singleton design pattern in Python ensuring only one instance is ever created.",
      ["Using __new__ to check for an existing _instance attribute", "Using a while loop", "Creating multiple classes", "Using global variables only"],
      "Using __new__ to check for an existing _instance attribute", "Practical Task",
      "Overriding `__new__` intercepts object creation and returns the cached instance.",
      q_type="practical_task",
      code_starter="class Singleton:\n    _instance = None\n    def __new__(cls):\n        if cls._instance is None:\n            cls._instance = super().__new__(cls)\n        return cls._instance")

# Advanced
add_q("OOP", "Advanced", "What does the Liskov Substitution Principle (LSP) require?",
      ["Subtypes must be substitutable for their base types without altering program correctness",
       "Classes must be closed for modification",
       "Interfaces should be small",
       "High-level modules should depend on abstractions"],
      "Subtypes must be substitutable for their base types without altering program correctness", "SOLID Principles",
      "LSP requires derived classes to honor contracts and preconditions/postconditions of the base type.")
add_q("OOP", "Advanced", "Why is composition favored over inheritance in software engineering ('Favor Composition Over Inheritance')?",
      ["Inheritance couples child classes tightly to parent implementation details and breaks encapsulation; composition offers flexible runtime behavior",
       "Composition is faster to compile",
       "Inheritance is deprecated in modern languages",
       "Composition requires fewer lines of code"],
      "Inheritance couples child classes tightly to parent implementation details and breaks encapsulation; composition offers flexible runtime behavior", "Design Principles",
      "Composition provides loose coupling and enables swapping component behavior dynamically.")
add_q("OOP", "Advanced", "In the Factory and Abstract Factory design patterns, what problem is solved?",
      ["Decoupling object creation logic from client code, allowing creation of families of related objects without specifying concrete classes",
       "Creating single global instances",
       "Managing database migrations",
       "Adding caching to methods"],
      "Decoupling object creation logic from client code, allowing creation of families of related objects without specifying concrete classes", "Design Patterns",
      "Factories encapsulate instantiation logic, making applications extensible to new subclasses.")
add_q("OOP", "Advanced", "What does Dependency Inversion Principle (DIP) state?",
      ["High-level modules should not depend on low-level modules; both should depend on abstractions",
       "Modules should import only system libraries",
       "Variables should be inverted in memory",
       "Subclasses must invert parent methods"],
      "High-level modules should not depend on low-level modules; both should depend on abstractions", "SOLID Principles",
      "DIP decouples business logic from implementation mechanisms using interfaces or dependency injection.")
add_q("OOP", "Advanced", "What is the Observer pattern and how does it prevent tight coupling?",
      ["A subject maintains a list of observers and notifies them automatically of state changes via an interface method",
       "A pattern for logging user keystrokes",
       "A compiler debugging technique",
       "A database indexing structure"],
      "A subject maintains a list of observers and notifies them automatically of state changes via an interface method", "Design Patterns",
      "The Subject only knows observers implement a notification interface, maintaining loose event-driven coupling.")

# --- WEB QUESTIONS ---
# Beginner
add_q("Web", "Beginner", "What does HTTP stand for in web technologies?",
      ["HyperText Transfer Protocol", "High-level Text Translation Program", "Hyperlink Transit Platform", "Home Terminal Transfer Policy"],
      "HyperText Transfer Protocol", "Web Protocols",
      "HTTP is the foundational application layer protocol of the World Wide Web.")
add_q("Web", "Beginner", "Which HTTP status code represents 'Resource Not Found'?",
      ["200", "400", "404", "500"], "404", "HTTP Status Codes",
      "404 indicates the server cannot locate the requested endpoint URL.")
add_q("Web", "Beginner", "What is the purpose of the HTML `<meta name='viewport'>` tag?",
      ["Enables SEO keywords", "Controls layout and viewport scaling on mobile device screens", "Loads CSS stylesheets", "Sets page title"],
      "Controls layout and viewport scaling on mobile device screens", "Responsive Design",
      "The viewport meta tag instructs mobile browsers to render the website at device width.")
add_q("Web", "Beginner", "What does the DOM stand for in browser web development?",
      ["Document Object Model", "Data Organization Method", "Digital Orientation Mode", "Direct Object Mapping"],
      "Document Object Model", "Browser Architecture",
      "The DOM is the tree representation of an HTML document accessible to JavaScript.")
add_q("Web", "Beginner", "Which CSS property is used to create flexible layout arrangements in modern web pages?",
      ["float", "display: flex;", "margin: auto;", "clear: both;"], "display: flex;", "CSS Layouts",
      "Flexbox provides powerful 1-dimensional alignment and distribution of items.")

# Intermediate
add_q("Web", "Intermediate", "What is Cross-Origin Resource Sharing (CORS)?",
      ["A browser security mechanism that restricts HTTP requests from scripts hosted on a different origin unless authorized via HTTP headers",
       "A JavaScript compression library",
       "A database connection pool protocol",
       "A CSS preprocessor"],
      "A browser security mechanism that restricts HTTP requests from scripts hosted on a different origin unless authorized via HTTP headers", "Web Security",
      "CORS uses headers like Access-Control-Allow-Origin to govern cross-origin API requests safely.")
add_q("Web", "Intermediate", "What is the purpose of the `useEffect` hook in React?",
      ["To render JSX", "To perform side effects (data fetching, DOM mutations, subscriptions) in function components", "To create global Redux stores", "To define URL routes"],
      "To perform side effects (data fetching, DOM mutations, subscriptions) in function components", "React Hooks",
      "`useEffect` executes side-effect logic after component render according to its dependency array.")
add_q("Web", "Intermediate", "What is the difference between `localStorage` and `sessionStorage` in the Web Storage API?",
      ["`localStorage` persists across browser sessions; `sessionStorage` clears when the page tab closes",
       "`sessionStorage` persists forever; `localStorage` expires in 1 hour",
       "`localStorage` is stored on the server; `sessionStorage` in the client",
       "There is no functional difference"],
      "`localStorage` persists across browser sessions; `sessionStorage` clears when the page tab closes", "Client Storage",
      "`localStorage` has no expiration date, while `sessionStorage` lifetime is bound to the tab.")
add_q("Web", "Intermediate", "What are HTTP cookies marked with `HttpOnly` protected against?",
      ["Cross-Site Request Forgery (CSRF)", "Cross-Site Scripting (XSS) stealing cookie tokens via `document.cookie`", "SQL Injection", "Distributed Denial of Service (DDoS)"],
      "Cross-Site Scripting (XSS) stealing cookie tokens via `document.cookie`", "Web Security",
      "`HttpOnly` prevents client-side JavaScript from reading cookies, mitigating XSS credential theft.")
add_q("Web", "Intermediate", "Write a fetch GET request that parses JSON and handles non-200 HTTP responses.",
      ["fetch(url).then(r => { if(!r.ok) throw new Error(); return r.json(); })",
       "fetch(url).json()",
       "window.load(url)",
       "http.get(url)"],
      "fetch(url).then(r => { if(!r.ok) throw new Error(); return r.json(); })", "Practical Task",
      "`fetch` only rejects on network failure, so `response.ok` must be checked explicitly.",
      q_type="practical_task",
      code_starter="async function fetchSkills(url) {\n    const res = await fetch(url);\n    if (!res.ok) throw new Error('API failed');\n    return await res.json();\n}")

# Advanced
add_q("Web", "Advanced", "How does the JavaScript Event Loop handle microtasks vs macrotasks?",
      ["Microtasks (Promise callbacks, queueMicrotask) execute immediately after the current task finishes and before the next macrotask (setTimeout, I/O)",
       "Macrotasks have higher priority than microtasks",
       "Both execute on parallel CPU cores simultaneously",
       "Microtasks execute only during garbage collection"],
      "Microtasks (Promise callbacks, queueMicrotask) execute immediately after the current task finishes and before the next macrotask (setTimeout, I/O)", "JavaScript Runtime",
      "The engine clears the entire microtask queue at the end of each tick before dequeuing the next macrotask.")
add_q("Web", "Advanced", "What is the difference between Server-Side Rendering (SSR) and Client-Side Rendering (CSR)?",
      ["SSR compiles HTML on the server before sending to the browser (better initial load & SEO); CSR delivers bare HTML and renders via JavaScript in the browser",
       "CSR is always faster for initial page load",
       "SSR cannot use JavaScript",
       "CSR is only used on mobile phones"],
      "SSR compiles HTML on the server before sending to the browser (better initial load & SEO); CSR delivers bare HTML and renders via JavaScript in the browser", "Web Architecture",
      "SSR renders markup on request for immediate paint and search indexability; CSR hydrates UI in the client.")
add_q("Web", "Advanced", "What security header prevents Clickjacking attacks by forbidding iframe embedding?",
      ["Content-Security-Policy with frame-ancestors or X-Frame-Options: DENY",
       "X-XSS-Protection",
       "Strict-Transport-Security",
       "Access-Control-Allow-Origin"],
      "Content-Security-Policy with frame-ancestors or X-Frame-Options: DENY", "Web Security",
      "`X-Frame-Options` and CSP `frame-ancestors` stop attackers from rendering sites inside transparent iframes.")
add_q("Web", "Advanced", "What is Tree Shaking in modern JavaScript bundlers (Vite, Webpack)?",
      ["Removing unused code exports from final bundle output using ES module static import/export analysis",
       "Minifying variable names",
       "Compressing image assets",
       "Sorting DOM nodes"],
      "Removing unused code exports from final bundle output using ES module static import/export analysis", "Bundling & Optimization",
      "Tree shaking eliminates dead code by analyzing static `import`/`export` syntax.")
add_q("Web", "Advanced", "How does HTTP/2 improve network throughput compared to HTTP/1.1?",
      ["Multiplexing multiple requests over a single TCP connection, header compression (HPACK), and binary framing",
       "Removing SSL encryption",
       "Using UDP exclusively without handshakes",
       "Allowing client-side server hosting"],
      "Multiplexing multiple requests over a single TCP connection, header compression (HPACK), and binary framing", "Protocols",
      "Multiplexing eliminates head-of-line blocking at the application layer by streaming frames concurrently.")

# --- STATISTICS / DATA ANALYSIS QUESTIONS ---
# Beginner
add_q("Statistics/Data Analysis", "Beginner", "What is the difference between Mean and Median?",
      ["Mean is the arithmetic average; Median is the middle value in sorted data, which is robust to outliers",
       "Median is always larger than Mean",
       "Mean is only for integers",
       "No difference"],
      "Mean is the arithmetic average; Median is the middle value in sorted data, which is robust to outliers", "Descriptive Statistics",
      "The median represents the 50th percentile and resists extreme outliers.")
add_q("Statistics/Data Analysis", "Beginner", "What does standard deviation measure in a dataset?",
      ["The average value", "The amount of variation or dispersion of data points around the mean", "The maximum minus minimum", "The sample size"],
      "The amount of variation or dispersion of data points around the mean", "Descriptive Statistics",
      "Standard deviation quantifies how spread out values are relative to the mean.")
add_q("Statistics/Data Analysis", "Beginner", "What is a scatter plot primarily used for?",
      ["Displaying category frequencies", "Visualizing the relationship or correlation between two continuous numeric variables", "Showing data over time only", "Displaying proportions of a whole"],
      "Visualizing the relationship or correlation between two continuous numeric variables", "Data Visualization",
      "Scatter plots map pairs of numeric values to X and Y coordinates to spot trends and clusters.")
add_q("Statistics/Data Analysis", "Beginner", "In Python Pandas, which method returns summary statistics (mean, std, min, max) for numeric columns?",
      ["df.summary()", "df.describe()", "df.info()", "df.stats()"], "df.describe()", "Pandas",
      "`df.describe()` outputs count, mean, std, min, quartiles, and max for numeric Series.")
add_q("Statistics/Data Analysis", "Beginner", "What does a correlation coefficient of +1.0 indicate?",
      ["No relationship", "A perfect positive linear relationship between two variables", "A negative correlation", "That data is corrupted"],
      "A perfect positive linear relationship between two variables", "Correlation",
      "+1.0 signifies that as variable X increases, variable Y increases in exact linear proportion.")

# Intermediate
add_q("Statistics/Data Analysis", "Intermediate", "In hypothesis testing, what is a p-value?",
      ["The probability of obtaining test results at least as extreme as observed, assuming the null hypothesis is true",
       "The probability that the alternative hypothesis is true",
       "The percentage error of data collection",
       "The parameter mean"],
      "The probability of obtaining test results at least as extreme as observed, assuming the null hypothesis is true", "Hypothesis Testing",
      "A p-value below alpha (e.g. 0.05) leads to rejecting the null hypothesis.")
add_q("Statistics/Data Analysis", "Intermediate", "What is the difference between Type I and Type II errors?",
      ["Type I is rejecting a true null hypothesis (false positive); Type II is failing to reject a false null hypothesis (false negative)",
       "Type I is false negative; Type II is false positive",
       "Type I is coding error; Type II is math error",
       "There is no difference"],
      "Type I is rejecting a true null hypothesis (false positive); Type II is failing to reject a false null hypothesis (false negative)", "Hypothesis Testing",
      "Type I error rate is alpha; Type II error rate is beta (1 - beta is statistical power).")
add_q("Statistics/Data Analysis", "Intermediate", "What does the Central Limit Theorem state?",
      ["The distribution of sample means approximates a normal distribution as sample size increases, regardless of population distribution shape",
       "All populations are normally distributed",
       "Sample size must equal population size",
       "Variance equals standard deviation"],
      "The distribution of sample means approximates a normal distribution as sample size increases, regardless of population distribution shape", "Probability Theory",
      "CLT allows parametric statistical inference for large samples (n >= 30).")
add_q("Statistics/Data Analysis", "Intermediate", "How does IQR (Interquartile Range) help identify outliers in a dataset?",
      ["Values below Q1 - 1.5*IQR or above Q3 + 1.5*IQR are flagged as potential outliers",
       "By taking the square root of mean",
       "By dropping all negative numbers",
       "By comparing with standard error"],
      "Values below Q1 - 1.5*IQR or above Q3 + 1.5*IQR are flagged as potential outliers", "Outlier Detection",
      "The Tukey boxplot rule uses 1.5 * IQR beyond the 25th and 75th percentiles.")
add_q("Statistics/Data Analysis", "Intermediate", "Calculate the median of the list [12, 3, 7, 19, 5, 21].",
      ["8.5", "9.5", "7.0", "12.0"], "9.5", "Practical Task",
      "Sorted list is [3, 5, 7, 12, 19, 21]. Middle two values are 7 and 12. Median = (7 + 12)/2 = 9.5.",
      q_type="practical_task",
      code_starter="import numpy as np\ndef get_median(arr):\n    return float(np.median(arr))")

# Advanced
add_q("Statistics/Data Analysis", "Advanced", "What is Simpson's Paradox in statistical analysis?",
      ["A trend that appears in several different groups of data disappears or reverses when the groups are combined",
       "A phenomenon where variance is infinite",
       "An error when dividing by zero in correlation",
       "A paradox about coin tosses"],
      "A trend that appears in several different groups of data disappears or reverses when the groups are combined", "Statistical Anomalies",
      "Confounding variables and unbalanced group sizes cause aggregate trends to contradict subgroup trends.")
add_q("Statistics/Data Analysis", "Advanced", "What is the primary assumption of Ordinary Least Squares (OLS) linear regression regarding residuals?",
      ["Residuals should be normally distributed, independent, and have constant variance (homoscedasticity)",
       "Residuals must be zero",
       "Residuals must increase with X",
       "Features must be categorical"],
      "Residuals should be normally distributed, independent, and have constant variance (homoscedasticity)", "Regression Analysis",
      "OLS assumes zero mean, homoscedasticity, and lack of autocorrelation in errors.")
add_q("Statistics/Data Analysis", "Advanced", "What does Bayes' Theorem calculate mathematically?",
      ["P(A|B) = [P(B|A) * P(A)] / P(B)",
       "P(A and B) = P(A) + P(B)",
       "P(A|B) = P(A) * P(B)",
       "P(A|B) = P(B) / P(A)"],
      "P(A|B) = [P(B|A) * P(A)] / P(B)", "Bayesian Statistics",
      "Bayes' Theorem updates the prior probability P(A) given evidence B using likelihood and marginal evidence.")
add_q("Statistics/Data Analysis", "Advanced", "Why is Adjusted R-squared preferred over R-squared in multiple linear regression?",
      ["R-squared automatically increases as more variables are added even if irrelevant; Adjusted R-squared penalizes non-informative predictors",
       "Adjusted R-squared is always between 0 and 100",
       "R-squared cannot be used for linear models",
       "Adjusted R-squared converts predictions to percentages"],
      "R-squared automatically increases as more variables are added even if irrelevant; Adjusted R-squared penalizes non-informative predictors", "Model Evaluation",
      "Adjusted R^2 accounts for degrees of freedom and guards against overfitting.")
add_q("Statistics/Data Analysis", "Advanced", "In A/B testing, what is the purpose of statistical power (1 - beta)?",
      ["The probability of correctly rejecting the null hypothesis when a true effect actually exists (avoiding false negatives)",
       "The maximum sample size allowed",
       "The speed of server response",
       "The confidence interval width"],
      "The probability of correctly rejecting the null hypothesis when a true effect actually exists (avoiding false negatives)", "Experimentation",
      "Targeting 80% or 90% power ensures experiments detect minimum detectable effects reliably.")

# --- PROBLEM SOLVING QUESTIONS ---
# Beginner
add_q("Problem Solving", "Beginner", "If a car travels at 60 km/h for 2.5 hours, what distance does it cover?",
      ["120 km", "150 km", "160 km", "180 km"], "150 km", "Quantitative Aptitude",
      "Distance = Speed * Time = 60 * 2.5 = 150 km.")
add_q("Problem Solving", "Beginner", "What is the next number in the series: 2, 4, 8, 16, 32, ...?",
      ["48", "64", "54", "60"], "64", "Pattern Recognition",
      "Each term is multiplied by 2 (powers of 2: 2^6 = 64).")
add_q("Problem Solving", "Beginner", "A product costs $80 and is discounted by 25%. What is the final selling price?",
      ["$60", "$65", "$55", "$70"], "$60", "Percentages",
      "Discount = 25% of 80 = $20. Final price = 80 - 20 = $60.")
add_q("Problem Solving", "Beginner", "Which algorithmic paradigm breaks a problem into non-overlapping subproblems and combines results?",
      ["Divide and Conquer", "Greedy Approach", "Dynamic Programming", "Backtracking"],
      "Divide and Conquer", "Algorithmic Paradigms",
      "Divide and Conquer divides into independent subproblems (like Merge Sort).")
add_q("Problem Solving", "Beginner", "If 5 workers build 5 chairs in 5 days, how many days will 10 workers take to build 10 chairs?",
      ["5 days", "10 days", "2 days", "1 day"], "5 days", "Rate & Work",
      "1 worker builds 1 chair in 5 days. Thus 10 workers build 10 chairs in 5 days.")

# Intermediate
add_q("Problem Solving", "Intermediate", "In a room of 23 people, what is approximately the probability that at least two share a birthday?",
      ["About 10%", "About 50%", "About 90%", "About 5%"], "About 50%", "Probability & Puzzles",
      "By the Birthday Paradox, with 23 people there are 253 pairs, giving a ~50.7% chance of shared birthday.")
add_q("Problem Solving", "Intermediate", "What is the minimum number of binary comparisons required to find a counterfeit heavy coin among 9 coins using a balance scale?",
      ["1", "2", "3", "4"], "2", "Logic & Scales",
      "Divide into groups of 3 (3, 3, 3). Weigh two groups; identifies the faulty group in 1 weigh. Second weigh from 3 coins finds the coin.")
add_q("Problem Solving", "Intermediate", "A train 150m long crosses a pole in 15 seconds. What is the speed of the train in km/h?",
      ["36 km/h", "40 km/h", "54 km/h", "60 km/h"], "36 km/h", "Time & Distance",
      "Speed = 150m / 15s = 10 m/s. 10 * (18/5) = 36 km/h.")
add_q("Problem Solving", "Intermediate", "Which algorithmic technique systematically explores all possible candidates for a solution and abandons dead ends?",
      ["Backtracking", "Dynamic Programming", "Greedy", "Binary Search"], "Backtracking", "Algorithmic Techniques",
      "Backtracking searches depth-first and prunes non-viable branches (e.g. N-Queens, Sudoku).")
add_q("Problem Solving", "Intermediate", "Determine if a string has all unique characters using bitwise operations or a boolean array.",
      ["True for 'abcdef', False for 'aabc'", "True for all", "False for all", "Error on space"],
      "True for 'abcdef', False for 'aabc'", "Practical Task",
      "Tracking seen character codes in an integer bitmask gives O(n) runtime and O(1) space.",
      q_type="practical_task",
      code_starter="def is_unique_chars(s: str) -> bool:\n    checker = 0\n    for char in s:\n        val = ord(char) - ord('a')\n        if (checker & (1 << val)) > 0:\n            return False\n        checker |= (1 << val)\n    return True")

# Advanced
add_q("Problem Solving", "Advanced", "What is the optimal strategy for the classic 2-Egg Drop problem with a 100-story building?",
      ["Drop the first egg at intervals of x, x-1, x-2... stories where x(x+1)/2 >= 100 (x = 14 drops minimum)",
       "Drop at floor 50 then floor 25",
       "Drop from floor 1 upwards one by one",
       "Drop at 10-floor intervals (19 drops)"],
      "Drop the first egg at intervals of x, x-1, x-2... stories where x(x+1)/2 >= 100 (x = 14 drops minimum)", "Puzzle Optimization",
      "Balancing worst-case drops for both eggs requires step decrements, yielding 14 drops in the worst case.")
add_q("Problem Solving", "Advanced", "In the Dining Philosophers problem, how can deadlock be formally prevented?",
      ["Introduce resource hierarchy (e.g. philosophers pick lowest-numbered fork first) or an arbitrator",
       "Let all philosophers pick the left fork simultaneously",
       "Increase philosopher thinking time",
       "Infinite forks"],
      "Introduce resource hierarchy (e.g. philosophers pick lowest-numbered fork first) or an arbitrator", "Deadlock Prevention",
      "Imposing a total ordering on shared resources breaks Coffman's circular wait condition.")
add_q("Problem Solving", "Advanced", "What is the time complexity of the Floyd-Warshall all-pairs shortest paths algorithm?",
      ["O(V^3)", "O(V^2 log V)", "O(E log V)", "O(V * E)"], "O(V^3)", "Algorithmic Analysis",
      "Three nested loops iterating over intermediate vertices V lead to O(V^3) complexity.")
add_q("Problem Solving", "Advanced", "How does Reservoir Sampling select k items from an unknown stream of n elements with uniform probability?",
      ["Fill reservoir with first k items, then for each i-th item replace a random slot with probability k/i",
       "Store all items in RAM",
       "Hash all items with SHA-256",
       "Drop even-indexed items"],
      "Fill reservoir with first k items, then for each i-th item replace a random slot with probability k/i", "Streaming Algorithms",
      "Induction proves that every element processed up to item i has an exact k/i probability of selection.")
add_q("Problem Solving", "Advanced", "What distinguishes NP-Complete problems from NP-Hard problems?",
      ["NP-Complete problems must be in NP (verifiable in polynomial time) and NP-hard; NP-hard problems need not be in NP",
       "NP-Complete problems are solved in O(n) time",
       "NP-Hard problems are strictly easier than NP-Complete",
       "No difference"],
      "NP-Complete problems must be in NP (verifiable in polynomial time) and NP-hard; NP-hard problems need not be in NP", "Computational Complexity",
      "NP-Complete problems are the hardest problems inside NP whose solutions can be verified in polynomial time.")

with open(DATA_DIR / "assessment_questions.json", "w", encoding="utf-8") as f:
    json.dump(QUESTIONS, f, indent=2)

print(f"Generated {len(QUESTIONS)} assessment questions across {len(CATEGORIES)} categories in assessment_questions.json")
