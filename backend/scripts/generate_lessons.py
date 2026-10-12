import json
from pathlib import Path
from datetime import datetime, timedelta
import random

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# ==============================================================================
# 3. LESSONS (At least 3 lessons per P0 skill = 24+ lessons)
# ==============================================================================
CATEGORIES = [
    "Python", "SQL", "DSA", "DBMS", "OOP", "Web", "Statistics/Data Analysis", "Problem Solving"
]

LESSONS = []

def create_lesson(category, level, title, minutes, markdown, quiz, resources):
    LESSONS.append({
        "skill_category": category,
        "title": title,
        "difficulty": level,
        "estimated_minutes": minutes,
        "content_markdown": markdown,
        "quiz": quiz,
        "external_resources": resources,
        "is_demo": False
    })

# --- PYTHON LESSONS ---
create_lesson(
    "Python", "Beginner", "Python Data Types, Slicing & Collections", 20,
    """# Python Core Data Structures: Lists, Tuples & Slices

Python provides powerful built-in sequence and mapping types:
- **Lists** `[]`: Mutable, ordered, supports indexing and slicing.
- **Tuples** `()`: Immutable, hashable, memory-efficient.
- **Dictionaries** `{}`: Key-value mappings powered by hash tables with O(1) average lookup.
- **Sets** `set()`: Unordered collection of unique items.

### Sequence Slicing Syntax:
```python
# syntax: sequence[start:stop:step]
numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
print(numbers[2:7])    # [2, 3, 4, 5, 6]
print(numbers[::-1])   # Reversed list: [9, 8, 7, ..., 0]
```

### Common Pitfall:
Modifying a list while iterating over it leads to skipped elements. Always iterate over a copy `for item in items[:]:` or construct a new list comprehension.
""",
    {
        "question": "What does `numbers[::-1]` do in Python?",
        "options": ["Prints the first number", "Reverses the sequence", "Multiplies each number by -1", "Raises a SyntaxError"],
        "correct_answer": "Reverses the sequence",
        "explanation": "A step of -1 traverses the sequence from right to left, reversing it."
    },
    [
        {"title": "Official Python Tutorial", "url": "https://docs.python.org/3/tutorial/datastructures.html", "type": "Documentation"},
        {"title": "Real Python: Python Lists and Tuples", "url": "https://realpython.com/python-lists-tuples/", "type": "Article"}
    ]
)

create_lesson(
    "Python", "Intermediate", "List Comprehensions & Generator Expressions", 25,
    """# Pythonic Iteration: Comprehensions vs Generators

### List Comprehensions:
List comprehensions provide a concise way to create lists without boilerplate loops:
```python
squares = [x**2 for x in range(10) if x % 2 == 0]
# [0, 4, 16, 36, 64]
```

### Generator Expressions:
When working with millions of records, generating all elements into RAM at once can cause Out-Of-Memory errors. Generator expressions evaluate lazily:
```python
# Evaluates one item on demand; O(1) memory!
gen_squares = (x**2 for x in range(1000000) if x % 2 == 0)
print(next(gen_squares)) # 0
```

### Performance Rule:
Use generator expressions for stream processing and pipeline aggregation (`sum(x for x in ...)`).
""",
    {
        "question": "Why use a generator expression over a list comprehension for 10 million items?",
        "options": ["Generators run in C speed", "Generators use O(1) memory by yielding items lazily", "List comprehensions cannot use if statements", "Generators automatically sort numbers"],
        "correct_answer": "Generators use O(1) memory by yielding items lazily",
        "explanation": "Generators compute values on-the-fly rather than allocating the entire list in RAM."
    },
    [
        {"title": "Real Python: Generators and Yield", "url": "https://realpython.com/introduction-to-python-generators/", "type": "Article"},
        {"title": "Python PEP 289: Generator Expressions", "url": "https://peps.python.org/pep-0289/", "type": "PEP Specification"}
    ]
)

create_lesson(
    "Python", "Advanced", "Decorators & Context Managers in Production", 30,
    """# Production Python: Metaprogramming with Decorators & Context Managers

### Understanding Function Decorators:
A decorator is a callable that takes a function as argument and returns an augmented function:
```python
import functools
import time

def timing_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        duration = time.perf_counter() - start
        print(f"{func.__name__} took {duration:.4f}s")
        return result
    return wrapper
```

### Context Managers:
The `with` statement guarantees cleanup even when exceptions occur:
```python
from contextlib import contextmanager

@contextmanager
def db_transaction():
    print("BEGIN TRANSACTION")
    try:
        yield
        print("COMMIT")
    except Exception:
        print("ROLLBACK")
        raise
```
""",
    {
        "question": "Why should you always apply `@functools.wraps(func)` inside a decorator wrapper?",
        "options": ["To compile to bytecode", "To preserve original function metadata (__name__, __doc__)", "To prevent recursion", "To enforce type hints"],
        "correct_answer": "To preserve original function metadata (__name__, __doc__)",
        "explanation": "`@wraps` copies over docstrings, function names, and annotations to the wrapper."
    },
    [
        {"title": "Python Docs: Context Managers", "url": "https://docs.python.org/3/library/contextlib.html", "type": "Documentation"},
        {"title": "Real Python: Primer on Python Decorators", "url": "https://realpython.com/primer-on-python-decorators/", "type": "Article"}
    ]
)

# --- SQL LESSONS ---
create_lesson(
    "SQL", "Beginner", "Relational Query Fundamentals: SELECT, WHERE, and Aggregation", 20,
    """# Essential SQL Query Flow

SQL queries are executed logically in a specific order:
1. `FROM` & `JOIN` (identify target tables)
2. `WHERE` (filter source rows)
3. `GROUP BY` (aggregate subsets)
4. `HAVING` (filter aggregated groups)
5. `SELECT` (project requested columns)
6. `ORDER BY` (sort results)
7. `LIMIT` / `OFFSET` (paginate output)

```sql
SELECT department, COUNT(*) AS employee_count, AVG(salary) AS avg_sal
FROM employees
WHERE is_active = TRUE
GROUP BY department
HAVING COUNT(*) > 5
ORDER BY avg_sal DESC;
```
""",
    {
        "question": "Which SQL clause evaluates filter conditions before grouping rows?",
        "options": ["HAVING", "WHERE", "ORDER BY", "SELECT"],
        "correct_answer": "WHERE",
        "explanation": "WHERE filters raw rows before GROUP BY aggregation occurs."
    },
    [
        {"title": "PostgreSQL Tutorial: SELECT Statement", "url": "https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-select/", "type": "Tutorial"}
    ]
)

create_lesson(
    "SQL", "Intermediate", "Mastering Table Joins & Subqueries", 25,
    """# Relational Joins & Subquery Patterns

### Join Types:
- **INNER JOIN**: Returns rows only when keys match in both tables.
- **LEFT JOIN**: Preserves all rows from the left table, with NULLs for missing right rows.
- **FULL OUTER JOIN**: Preserves all rows from both tables.

```sql
SELECT u.username, o.order_id, o.total_amount
FROM users u
LEFT JOIN orders o ON u.id = o.user_id;
```

### Correlated Subqueries:
A correlated subquery references values from the outer query for each evaluated row.
""",
    {
        "question": "What is returned for an unmatched row in a LEFT JOIN?",
        "options": ["Error", "Zero values", "NULL values for right table columns", "The row is dropped"],
        "correct_answer": "NULL values for right table columns",
        "explanation": "LEFT JOIN keeps all left rows and fills right columns with NULL when no match exists."
    },
    [
        {"title": "Mode Analytics: SQL Joins Guide", "url": "https://mode.com/sql-tutorial/sql-joins/", "type": "Guide"}
    ]
)

create_lesson(
    "SQL", "Advanced", "Window Functions & Analytical Partitioning", 30,
    """# Analytical Window Functions

Window functions perform calculations across a set of table rows that are related to the current row, without collapsing rows like `GROUP BY`:

```sql
SELECT 
    employee_name,
    department,
    salary,
    RANK() OVER (PARTITION BY department ORDER BY salary DESC) as dept_rank,
    AVG(salary) OVER (PARTITION BY department) as dept_avg,
    LAG(salary, 1) OVER (PARTITION BY department ORDER BY salary) as prev_lower_salary
FROM employees;
```

Window functions are essential for technical interviews, running totals, top-N per category, and moving averages.
""",
    {
        "question": "How does a window function differ from GROUP BY?",
        "options": ["Window functions cannot calculate averages", "Window functions preserve individual rows while calculating aggregates", "Window functions only work on strings", "Window functions do not allow ORDER BY"],
        "correct_answer": "Window functions preserve individual rows while calculating aggregates",
        "explanation": "Unlike GROUP BY which collapses rows, window functions retain each row in the output."
    },
    [
        {"title": "PostgreSQL Docs: Window Functions", "url": "https://www.postgresql.org/docs/current/tutorial-window.html", "type": "Documentation"}
    ]
)

# --- DSA LESSONS ---
create_lesson(
    "DSA", "Beginner", "Time & Space Complexity: Asymptotic Big-O Analysis", 20,
    """# Understanding Big-O Complexity

Big-O notation describes the upper bound of runtime or memory as input size `n` grows:
- **O(1)** Constant: Array index access, hash map lookup.
- **O(log n)** Logarithmic: Binary search on sorted array.
- **O(n)** Linear: Single loop through an array.
- **O(n log n)** Linearithmic: Merge sort, Heap sort.
- **O(n^2)** Quadratic: Nested loops, bubble sort.

### Space Complexity:
Always account for auxiliary memory allocated by your algorithm, including call stack frames in recursive algorithms.
""",
    {
        "question": "What is the time complexity of searching a sorted array of size n with Binary Search?",
        "options": ["O(1)", "O(n)", "O(log n)", "O(n^2)"],
        "correct_answer": "O(log n)",
        "explanation": "Binary search halves the search space at each comparison step, achieving O(log n)."
    },
    [
        {"title": "Big-O Cheat Sheet", "url": "https://www.bigocheatsheet.com/", "type": "Cheat Sheet"}
    ]
)

create_lesson(
    "DSA", "Intermediate", "Tree Traversals and Binary Search Tree Properties", 25,
    """# Binary Trees & Depth-First Traversals

### Three Classic DFS Traversals:
1. **Pre-order**: Node -> Left -> Right
2. **In-order**: Left -> Node -> Right *(Yields sorted order in a BST!)*
3. **Post-order**: Left -> Right -> Node *(Useful for subtree deletion or height calculation)*

### Binary Search Tree Invariant:
For every node `P`:
- All values in `P.left` are strictly less than `P.val`.
- All values in `P.right` are strictly greater than `P.val`.
""",
    {
        "question": "Which DFS traversal yields elements of a BST in strictly sorted ascending order?",
        "options": ["Pre-order", "In-order", "Post-order", "Level-order"],
        "correct_answer": "In-order",
        "explanation": "In-order traversal visits left subtree, current node, then right subtree, producing sorted output."
    },
    [
        {"title": "GeeksforGeeks: Tree Traversals", "url": "https://www.geeksforgeeks.org/tree-traversals-inorder-preorder-and-postorder/", "type": "Tutorial"}
    ]
)

create_lesson(
    "DSA", "Advanced", "Dynamic Programming: Memoization vs Tabulation", 30,
    """# Mastering Dynamic Programming

Dynamic programming applies to problems with:
1. **Overlapping Subproblems**: The same subproblems are solved repeatedly.
2. **Optimal Substructure**: The optimal solution to the problem contains optimal solutions to subproblems.

### Two Implementation Strategies:
- **Top-Down (Memoization)**: Natural recursive formulation cached in a hash map or array.
- **Bottom-Up (Tabulation)**: Iterative computation from base cases upwards, allowing state-space memory reduction (e.g. keeping only the last 2 states).
""",
    {
        "question": "What two properties must a problem have to be solvable by Dynamic Programming?",
        "options": ["High CPU speed and low RAM", "Overlapping Subproblems and Optimal Substructure", "Sorting and Searching", "Bit manipulation and Pointers"],
        "correct_answer": "Overlapping Subproblems and Optimal Substructure",
        "explanation": "DP avoids recomputing identical states (overlapping subproblems) while combining optimal sub-solutions."
    },
    [
        {"title": "MIT OpenCourseWare: Dynamic Programming", "url": "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/resources/lecture-19-dynamic-programming-i-fibonacci-shortest-paths/", "type": "Lecture"}
    ]
)

# --- DBMS LESSONS ---
create_lesson(
    "DBMS", "Beginner", "ACID Properties & Relational Data Integrity", 20,
    """# Relational Database Guarantees: ACID

- **Atomicity**: Either all operations in a transaction succeed, or none do (All-or-Nothing).
- **Consistency**: Data transitions only between valid states conforming to schema constraints.
- **Isolation**: Concurrent transactions execute without interfering with each other's uncommitted changes.
- **Durability**: Once committed, changes survive server crashes or power failures.
""",
    {
        "question": "If a transaction fails halfway through, which ACID property ensures incomplete writes are rolled back?",
        "options": ["Durability", "Atomicity", "Isolation", "Scalability"],
        "correct_answer": "Atomicity",
        "explanation": "Atomicity treats the sequence of database operations as a single indivisible unit."
    },
    [{"title": "Database Systems Concepts (Silberschatz)", "url": "https://www.db-book.com/", "type": "Book"}]
)

create_lesson(
    "DBMS", "Intermediate", "Database Normalization: 1NF to BCNF", 25,
    """# Normalization Rules & Anomaly Prevention

Normalization eliminates data redundancy and prevents update, insertion, and deletion anomalies:
- **1NF**: Column values are atomic; no repeating groups.
- **2NF**: In 1NF and no non-key attribute is partially dependent on any candidate key.
- **3NF**: In 2NF and no transitive functional dependency exists between non-key attributes.
- **BCNF**: For every functional dependency `X -> Y`, `X` must be a super key.
""",
    {
        "question": "Which normal form specifically eliminates transitive dependencies?",
        "options": ["1NF", "2NF", "3NF", "4NF"],
        "correct_answer": "3NF",
        "explanation": "3NF requires that no non-prime attribute is transitively dependent on the primary key."
    },
    [{"title": "Stanford DB: Relational Design Theory", "url": "https://web.stanford.edu/class/cs145/", "type": "Course"}]
)

create_lesson(
    "DBMS", "Advanced", "Transaction Isolation Levels & Concurrency Anomalies", 30,
    """# Concurrency Control: The ANSI Isolation Hierarchy

Four ANSI isolation levels manage tradeoffs between concurrency and correctness:
1. **Read Uncommitted**: Suffers from Dirty Reads.
2. **Read Committed**: Prevents Dirty Reads; permits Non-Repeatable Reads.
3. **Repeatable Read**: Prevents Non-Repeatable Reads; permits Phantoms/Write Skew.
4. **Serializable**: Full serial execution guarantee.
""",
    {
        "question": "What is a 'Dirty Read' in database transactions?",
        "options": ["Reading corrupted disk pages", "Reading uncommitted changes written by another concurrent transaction", "Reading outdated indexes", "Reading null values"],
        "correct_answer": "Reading uncommitted changes written by another concurrent transaction",
        "explanation": "A dirty read occurs when a transaction reads rows modified by another transaction before it commits."
    },
    [{"title": "A Critique of ANSI SQL Isolation Levels", "url": "https://arxiv.org/abs/cs/0701157", "type": "Paper"}]
)

# --- OOP LESSONS ---
create_lesson(
    "OOP", "Beginner", "The Four Pillars of Object-Oriented Design", 20,
    """# OOP Pillars in Practice

1. **Encapsulation**: Private state protected behind public interfaces.
2. **Abstraction**: Hiding internal implementation complexity.
3. **Inheritance**: Subclassing shared behaviors from generalized parents.
4. **Polymorphism**: Treating different derived types uniformly via shared methods.
""",
    {
        "question": "Which pillar of OOP is primarily demonstrated by private variables with getter/setter methods?",
        "options": ["Polymorphism", "Encapsulation", "Inheritance", "Compilation"],
        "correct_answer": "Encapsulation",
        "explanation": "Encapsulation binds data and functions together while restricting direct access to internal fields."
    },
    [{"title": "OOP Design Fundamentals", "url": "https://refactoring.guru/design-patterns", "type": "Guide"}]
)

create_lesson(
    "OOP", "Intermediate", "SOLID Principles for Clean Architecture", 25,
    """# The SOLID Principles

- **S**ingle Responsibility: One reason to change.
- **O**pen/Closed: Open for extension, closed for modification.
- **L**iskov Substitution: Subclasses must be substitutable for parent types.
- **I**nterface Segregation: Prefer small, client-specific interfaces.
- **D**ependency Inversion: Depend on abstractions, not concrete classes.
""",
    {
        "question": "What does the Open/Closed Principle state?",
        "options": ["Software entities should be open for extension, but closed for modification", "Files should be closed after opening", "Classes must have open constructors", "Methods should be public"],
        "correct_answer": "Software entities should be open for extension, but closed for modification",
        "explanation": "Classes should be extendable with new behavior (via inheritance or composition) without altering existing code."
    },
    [{"title": "Clean Code Handbook", "url": "https://www.oreilly.com/library/view/clean-code-a/9780136083238/", "type": "Book"}]
)

create_lesson(
    "OOP", "Advanced", "Creational & Behavioral Design Patterns in Practice", 30,
    """# Essential Design Patterns

- **Factory Pattern**: Centralizes complex object instantiation.
- **Strategy Pattern**: Encapsulates interchangeable algorithms and behaviors behind an interface.
- **Observer Pattern**: Implements event-driven pub/sub architecture between loosely coupled objects.
- **Decorator Pattern**: Dynamically attaches new responsibilities to objects without altering structure.
""",
    {
        "question": "Which design pattern enables swapping algorithms at runtime by encapsulating each algorithm in a separate class?",
        "options": ["Singleton", "Strategy", "Adapter", "Builder"],
        "correct_answer": "Strategy",
        "explanation": "The Strategy pattern defines a family of algorithms and makes them interchangeable."
    },
    [{"title": "Refactoring Guru: Design Patterns", "url": "https://refactoring.guru/design-patterns", "type": "Interactive Guide"}]
)

# --- WEB LESSONS ---
create_lesson(
    "Web", "Beginner", "HTTP Protocols, REST Architecture & Status Codes", 20,
    """# Modern Web Communication: HTTP & REST

HTTP verbs convey semantic intent:
- `GET`: Read resource (Idempotent, Safe)
- `POST`: Create resource (Non-idempotent)
- `PUT`: Replace resource completely (Idempotent)
- `PATCH`: Update partial attributes (Non-idempotent or Idempotent)
- `DELETE`: Remove resource (Idempotent)

Status codes communicate outcomes:
- `200 OK`, `201 Created`
- `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`
- `500 Internal Server Error`, `503 Service Unavailable`
""",
    {
        "question": "Which HTTP method should be used to retrieve data without modifying server state?",
        "options": ["POST", "GET", "PUT", "DELETE"],
        "correct_answer": "GET",
        "explanation": "GET is defined by the HTTP specification as a safe, read-only method."
    },
    [{"title": "MDN Web Docs: HTTP Overview", "url": "https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview", "type": "Documentation"}]
)

create_lesson(
    "Web", "Intermediate", "Frontend State Management & React Lifecycle Hooks", 25,
    """# React Architecture: Hooks & Component State

### useState & useEffect:
- `useState`: Declares reactive state variable with setter function.
- `useEffect`: Manages lifecycle subscriptions, API calls, and cleanup routines.

### Best Practices:
1. Keep component state localized to the lowest common parent.
2. Avoid derived state in `useState`; compute it inline during render.
3. Clean up timers and event listeners in the `useEffect` return function.
""",
    {
        "question": "What is the second argument passed to React's useEffect hook?",
        "options": ["A callback function", "A dependency array", "A timeout duration in ms", "A DOM selector"],
        "correct_answer": "A dependency array",
        "explanation": "The dependency array tells React when to re-execute the effect."
    },
    [{"title": "React Official Docs", "url": "https://react.dev/", "type": "Documentation"}]
)

create_lesson(
    "Web", "Advanced", "Web Security: CORS, CSRF, XSS & Secure Cookies", 30,
    """# Securing Web Applications

### Defense-in-Depth Mechanisms:
1. **XSS (Cross-Site Scripting)**: Sanitize user input; enforce Content-Security-Policy (CSP); store auth tokens in `HttpOnly` cookies.
2. **CSRF (Cross-Site Request Forgery)**: Set `SameSite=Lax` or `Strict` on session cookies; validate custom headers.
3. **CORS**: Ensure server whitelist matches only legitimate client origins.
""",
    {
        "question": "Which cookie flag prevents client-side JavaScript from reading sensitive session identifiers?",
        "options": ["Secure", "HttpOnly", "SameSite", "Path"],
        "correct_answer": "HttpOnly",
        "explanation": "HttpOnly blocks `document.cookie` access from JavaScript, protecting against XSS credential theft."
    },
    [{"title": "OWASP Top Ten", "url": "https://owasp.org/www-project-top-ten/", "type": "Security Standard"}]
)

# --- STATISTICS LESSONS ---
create_lesson(
    "Statistics/Data Analysis", "Beginner", "Exploratory Data Analysis with Pandas & Descriptive Statistics", 20,
    """# Foundations of Data Analysis

EDA is the crucial first step in any analytical workflow:
1. Examine distributions (mean, median, standard deviation, interquartile range).
2. Identify missing values (`df.isnull().sum()`) and handle imputations.
3. Detect anomalies and outliers with boxplots and z-scores.
""",
    {
        "question": "Why is the median preferred over the mean for skewed data with extreme outliers?",
        "options": ["Median is faster to calculate", "Median is resistant to extreme values", "Median works on text", "Mean is always zero"],
        "correct_answer": "Median is resistant to extreme values",
        "explanation": "The median represents the central 50% point and is not dragged by distant outliers."
    },
    [{"title": "Pandas User Guide", "url": "https://pandas.pydata.org/docs/user_guide/index.html", "type": "Documentation"}]
)

create_lesson(
    "Statistics/Data Analysis", "Intermediate", "Hypothesis Testing & A/B Experimentation", 25,
    """# Statistical Inference & Hypothesis Testing

### The 4-Step Testing Framework:
1. Formulate Null Hypothesis ($H_0$) and Alternative Hypothesis ($H_a$).
2. Choose significance level $\\alpha$ (typically 0.05).
3. Compute test statistic (t-test, z-test, or chi-square).
4. Calculate p-value: if $p < \\alpha$, reject $H_0$.
""",
    {
        "question": "What decision is made when the calculated p-value is less than alpha (0.05)?",
        "options": ["Accept null hypothesis", "Reject null hypothesis in favor of alternative", "Declare test inconclusive", "Discard data"],
        "correct_answer": "Reject null hypothesis in favor of alternative",
        "explanation": "A p-value below alpha demonstrates statistically significant evidence against the null hypothesis."
    },
    [{"title": "NIST Engineering Statistics Handbook", "url": "https://www.itl.nist.gov/div898/handbook/", "type": "Reference"}]
)

create_lesson(
    "Statistics/Data Analysis", "Advanced", "Multiple Linear Regression & Causal Modeling", 30,
    """# Predictive Modeling: Multiple Linear Regression

Linear regression estimates target $Y$ from features $X$:
$$Y = \\beta_0 + \\beta_1 X_1 + \\dots + \\beta_p X_p + \\epsilon$$

### Key Diagnostics:
- Check for multicollinearity using Variance Inflation Factor (VIF < 5).
- Verify homoscedasticity of residuals via residual vs fitted plots.
- Use Adjusted $R^2$ to evaluate model fit while penalizing superfluous features.
""",
    {
        "question": "What problem does a high Variance Inflation Factor (VIF > 10) indicate?",
        "options": ["High model accuracy", "Severe multicollinearity among predictor variables", "Underfitting", "Lack of data"],
        "correct_answer": "Severe multicollinearity among predictor variables",
        "explanation": "High VIF indicates independent variables are strongly correlated with each other, inflating coefficient variance."
    },
    [{"title": "An Introduction to Statistical Learning", "url": "https://www.statlearning.com/", "type": "Textbook"}]
)

# --- PROBLEM SOLVING LESSONS ---
create_lesson(
    "Problem Solving", "Beginner", "Structured Algorithmic Problem Solving Frameworks", 20,
    """# The 5-Step Problem Solving Framework

1. **Understand**: Clarify inputs, outputs, edge cases (empty lists, negative numbers, overflow).
2. **Explore Examples**: Walk through typical and boundary inputs manually.
3. **Break Down**: Formulate brute-force approach first before premature optimization.
4. **Optimize**: Identify bottlenecks using Big-O time and space tradeoffs.
5. **Code & Verify**: Write clean modular code and trace with edge inputs.
""",
    {
        "question": "What should you clarify before writing code in a technical interview?",
        "options": ["Salary expectations", "Input formats, constraints, and edge cases", "Company stock price", "Nothing, start typing immediately"],
        "correct_answer": "Input formats, constraints, and edge cases",
        "explanation": "Clarifying constraints prevents false assumptions and wasted engineering time."
    },
    [{"title": "Cracking the Coding Interview Guide", "url": "https://www.crackingthecodinginterview.com/", "type": "Guide"}]
)

create_lesson(
    "Problem Solving", "Intermediate", "Two Pointers, Sliding Window & Frequency Maps", 25,
    """# High-Frequency Interview Patterns

### 1. Two Pointers:
Used on sorted arrays or palindromes to reduce $O(n^2)$ nested loops to $O(n)$:
```python
def is_palindrome(s):
    l, r = 0, len(s) - 1
    while l < r:
        if s[l] != s[r]: return False
        l += 1; r -= 1
    return True
```

### 2. Sliding Window:
Maintains a dynamic window `[start, end]` across continuous subarrays (e.g. longest substring without repeating characters).
""",
    {
        "question": "What time complexity does the Two Pointers pattern achieve for sorted array pair searches?",
        "options": ["O(n^2)", "O(n)", "O(n log n)", "O(1)"],
        "correct_answer": "O(n)",
        "explanation": "Pointers traverse the array inward at most once, running in linear O(n) time."
    },
    [{"title": "LeetCode Pattern Guide", "url": "https://leetcode.com/explore/", "type": "Platform"}]
)

create_lesson(
    "Problem Solving", "Advanced", "Greedy Strategies vs Dynamic Programming", 30,
    """# Greedy Choice Property vs Global Optimization

- **Greedy Algorithms**: Make the locally optimal choice at each step without backtracking (e.g. Dijkstra, Huffman Coding, Fractional Knapsack).
- **Dynamic Programming**: Required when local greedy choices do not guarantee the global optimum (e.g. 0/1 Knapsack, Coin Change with arbitrary denominations).

### Verification Technique:
To prove a greedy strategy is valid, use an exchange argument showing any other optimal solution can be transformed into the greedy solution without loss of value.
""",
    {
        "question": "Why fails a greedy approach for the 0/1 Knapsack problem?",
        "options": ["Items cannot be divided into fractions, so taking highest value-to-weight may block a better total combination", "Greedy is too fast", "Sorting is impossible", "Math does not allow it"],
        "correct_answer": "Items cannot be divided into fractions, so taking highest value-to-weight may block a better total combination",
        "explanation": "In 0/1 Knapsack, leaving unused capacity may produce a lower total value than taking a different combination of items."
    },
    [{"title": "Introduction to Algorithms (CLRS)", "url": "https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/", "type": "Textbook"}]
)

with open(DATA_DIR / "lessons.json", "w", encoding="utf-8") as f:
    json.dump(LESSONS, f, indent=2)

print(f"Generated {len(LESSONS)} lessons across {len(CATEGORIES)} categories in lessons.json")
