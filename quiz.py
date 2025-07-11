import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('db/quiz1.db')
cursor = conn.cursor()

# Create 'users' table (re-runnable)
cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
''')

# Create 'scores' table (re-runnable)
cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS scores (
        score_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        score INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
''')

# Create 'questions' table with 'category' and 'difficulty' columns (re-runnable)
cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS questions (
        question_id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_text TEXT NOT NULL,
        option1 TEXT NOT NULL,
        option2 TEXT NOT NULL,
        option3 TEXT NOT NULL,
        option4 TEXT NOT NULL,
        correct_option INTEGER NOT NULL,
        category TEXT NOT NULL,
        difficulty TEXT NOT NULL  -- Add difficulty column
    )
''')

# Insert sample questions into 'questions' table if not already inserted
# To avoid duplicate entries, check if the table already has data
cursor.execute('SELECT COUNT(*) FROM questions')
question_count = cursor.fetchone()[0]

if question_count == 0:
    sample_questions = [
    # Geography
    # Beginner
    ("What is the capital of India?", "Delhi", "London", "Berlin", "Madrid", 1, "Geography", "beginner"),
    ("What is the capital of France?", "Paris", "Rome", "Berlin", "Madrid", 1, "Geography", "beginner"),
    ("Which continent is the Sahara Desert located on?", "Asia", "Africa", "South America", "Australia", 2, "Geography", "beginner"),
    ("Which European city is known as the City of Canals?", "Venice", "Amsterdam", "Bruges", "Copenhagen", 1, "Geography", "beginner"),
    ("What is the largest ocean on Earth?", "Atlantic", "Indian", "Arctic", "Pacific", 4, "Geography", "beginner"),

    # Intermediate
    ("Which river is the longest in the world?", "Amazon", "Nile", "Yangtze", "Mississippi", 2, "Geography", "intermediate"),
    ("Mount Everest is located in which country?", "India", "Nepal", "China", "Bhutan", 2, "Geography", "intermediate"),
    ("Which country has the most natural lakes?", "USA", "Canada", "Russia", "Brazil", 2, "Geography", "intermediate"),
    ("What is the capital of Australia?", "Sydney", "Melbourne", "Canberra", "Perth", 3, "Geography", "intermediate"),
    ("Which country is known as the Land of the Rising Sun?", "China", "South Korea", "Japan", "Thailand", 3, "Geography", "intermediate"),
    ("Which continent is home to the Amazon Rainforest?", "Africa", "Asia", "South America", "Australia", 3, "Geography", "intermediate"),
    ("What is the largest desert in the world?", "Sahara", "Gobi", "Kalahari", "Atacama", 1, "Geography", "intermediate"),
    ("Which country is the Great Barrier Reef located in?", "USA", "Australia", "Mexico", "Thailand", 2, "Geography", "intermediate"),
    ("What is the capital of Japan?", "Beijing", "Seoul", "Tokyo", "Manila", 3, "Geography", "intermediate"),
    ("Which country has the longest coastline?", "Canada", "Russia", "Australia", "USA", 1, "Geography", "intermediate"),

    # Advanced
    ("What is the smallest country in the world?", "Monaco", "San Marino", "Vatican City", "Liechtenstein", 3, "Geography", "advanced"),
    ("Which country has the largest population?", "India", "USA", "China", "Indonesia", 3, "Geography", "advanced"),
    ("Which mountain range is home to Mount Everest?", "Rockies", "Andes", "Alps", "Himalayas", 4, "Geography", "advanced"),
    ("What is the deepest part of the ocean?", "Mariana Trench", "Challenger Deep", "Puerto Rico Trench", "Java Trench", 2, "Geography", "advanced"),
    ("Which is the largest island in the world?", "Greenland", "Australia", "New Guinea", "Borneo", 1, "Geography", "advanced"),
    ("Which country has the largest number of volcanoes?", "Indonesia", "Japan", "USA", "Iceland", 2, "Geography", "advanced"),
    ("Which river is considered the longest in Europe?", "Volga", "Danube", "Rhine", "Elbe", 1, "Geography", "advanced"),
    ("Which desert is the largest cold desert in the world?", "Gobi", "Karakum", "Karakol", "Atacama", 1, "Geography", "advanced"),
    ("What is the official language of Brazil?", "Spanish", "Portuguese", "French", "English", 2, "Geography", "advanced"),
    ("Which country is home to the ancient city of Petra?", "Jordan", "Israel", "Egypt", "Iraq", 1, "Geography", "advanced"),

    # Literature
    # Beginner
    ("Who wrote 'Hamlet'?", "Charles Dickens", "William Shakespeare", "J.K. Rowling", "Mark Twain", 2, "Literature", "beginner"),
    ("Who wrote 'Pride and Prejudice'?", "Jane Austen", "Charlotte Brontë", "Emily Brontë", "Louisa May Alcott", 1, "Literature", "beginner"),
    ("Who wrote 'To Kill a Mockingbird'?", "Harper Lee", "Mark Twain", "Ernest Hemingway", "John Steinbeck", 1, "Literature", "beginner"),
    ("What is the title of the first Harry Potter book?", "The Philosopher's Stone", "The Chamber of Secrets", "The Prisoner of Azkaban", "The Goblet of Fire", 1, "Literature", "beginner"),
    ("Who wrote 'The Catcher in the Rye'?", "J.D. Salinger", "F. Scott Fitzgerald", "Ernest Hemingway", "Jack Kerouac", 1, "Literature", "beginner"),

    # Intermediate
    ("Which book series features the character Katniss Everdeen?", "Divergent", "Twilight", "The Hunger Games", "Harry Potter", 3, "Literature", "intermediate"),
    ("Who wrote 'The Great Gatsby'?", "Ernest Hemingway", "F. Scott Fitzgerald", "John Steinbeck", "William Faulkner", 2, "Literature", "intermediate"),
    ("Which author wrote '1984'?", "George Orwell", "Aldous Huxley", "Ray Bradbury", "H.G. Wells", 1, "Literature", "intermediate"),
    ("Who wrote 'Brave New World'?", "Aldous Huxley", "George Orwell", "Ray Bradbury", "J.K. Rowling", 1, "Literature", "intermediate"),
    ("What is the name of Sherlock Holmes' loyal companion?", "Dr. Watson", "Inspector Lestrade", "Mrs. Hudson", "Mycroft Holmes", 1, "Literature", "intermediate"),
    ("Who wrote 'The Picture of Dorian Gray'?", "Oscar Wilde", "H.G. Wells", "J.R.R. Tolkien", "Charles Dickens", 1, "Literature", "intermediate"),
    ("Who wrote 'Wuthering Heights'?", "Charlotte Brontë", "Emily Brontë", "Jane Austen", "Mary Shelley", 2, "Literature", "intermediate"),
    ("Which Shakespeare play features the characters Romeo and Juliet?", "Macbeth", "Hamlet", "Othello", "Romeo and Juliet", 4, "Literature", "intermediate"),
    ("Who wrote 'Moby-Dick'?", "Herman Melville", "Nathaniel Hawthorne", "Jules Verne", "Charles Dickens", 1, "Literature", "intermediate"),
    ("Who wrote 'The Odyssey'?", "Virgil", "Homer", "Sophocles", "Aristotle", 2, "Literature", "intermediate"),

    # Advanced
    ("Which author wrote 'War and Peace'?", "Fyodor Dostoevsky", "Leo Tolstoy", "Anton Chekhov", "Vladimir Nabokov", 2, "Literature", "advanced"),
    ("Who wrote 'The Divine Comedy'?", "Homer", "Virgil", "Dante Alighieri", "William Blake", 3, "Literature", "advanced"),
    ("Which poet wrote 'The Raven'?", "Emily Dickinson", "Edgar Allan Poe", "Robert Frost", "Walt Whitman", 2, "Literature", "advanced"),
    ("Which novel begins with the line, 'Call me Ishmael'?", "Moby-Dick", "The Great Gatsby", "War and Peace", "1984", 1, "Literature", "advanced"),
    ("Who wrote 'Don Quixote'?", "Miguel de Cervantes", "Homer", "Virgil", "James Joyce", 1, "Literature", "advanced"),
    ("Who wrote 'The Brothers Karamazov'?", "Fyodor Dostoevsky", "Leo Tolstoy", "Anton Chekhov", "Vladimir Nabokov", 1, "Literature", "advanced"),
    ("Who wrote 'Ulysses'?", "James Joyce", "Virgil", "Homer", "William Faulkner", 1, "Literature", "advanced"),
    ("Who wrote 'The Iliad'?", "Homer", "Virgil", "Sophocles", "Aristotle", 1, "Literature", "advanced"),
    ("Who is the author of 'The Catcher in the Rye'?", "J.D. Salinger", "F. Scott Fitzgerald", "Ernest Hemingway", "Jack Kerouac", 1, "Literature", "advanced"),
    ("Who wrote 'The Old Man and the Sea'?", "Ernest Hemingway", "Mark Twain", "John Steinbeck", "F. Scott Fitzgerald", 1, "Literature", "advanced"),

    # Science
    # Beginner
    ("What is the chemical symbol for water?", "H2O", "O2", "CO2", "NaCl", 1, "Science", "beginner"),
    ("What is the primary gas found in Earth's atmosphere?", "Oxygen", "Nitrogen", "Carbon Dioxide", "Hydrogen", 2, "Science", "beginner"),
    ("What does DNA stand for?", "Deoxyribonucleic Acid", "Ribonucleic Acid", "Deoxyribonucleoside Acid", "Dioxygen Acid", 1, "Science", "beginner"),
    ("What is the speed of light?", "300,000 km/s", "150,000 km/s", "1,000 km/s", "1,500 km/s", 1, "Science", "beginner"),
    ("What is the study of plants called?", "Botany", "Zoology", "Geology", "Ecology", 1, "Science", "beginner"),

    # Intermediate
    ("Which planet is known as the Red Planet?", "Earth", "Mars", "Venus", "Jupiter", 2, "Science", "intermediate"),
    ("What is the hardest natural substance on Earth?", "Gold", "Iron", "Diamond", "Graphite", 3, "Science", "intermediate"),
    ("Which planet has the most moons?", "Mars", "Jupiter", "Saturn", "Uranus", 2, "Science", "intermediate"),
    ("What is the boiling point of water in Celsius?", "50", "100", "150", "200", 2, "Science", "intermediate"),
    ("What is the name of the largest internal organ in the human body?", "Heart", "Liver", "Lungs", "Kidneys", 2, "Science", "intermediate"),
    ("What is the chemical symbol for gold?", "Au", "Ag", "Pb", "Fe", 1, "Science", "intermediate"),
    ("What gas do plants absorb for photosynthesis?", "Oxygen", "Nitrogen", "Carbon Dioxide", "Hydrogen", 3, "Science", "intermediate"),
    ("What is the process by which plants make their own food?", "Respiration", "Photosynthesis", "Fermentation", "Digestion", 2, "Science", "intermediate"),
    ("What is the most common gas in Earth's atmosphere?", "Oxygen", "Carbon Dioxide", "Nitrogen", "Hydrogen", 3, "Science", "intermediate"),
    ("Which planet is the closest to the Sun?", "Earth", "Venus", "Mercury", "Mars", 3, "Science", "intermediate"),

    # Advanced
    ("What is the atomic number of carbon?", "12", "6", "8", "14", 2, "Science", "advanced"),
    ("What is the most abundant element in the Earth's crust?", "Iron", "Aluminum", "Oxygen", "Silicon", 3, "Science", "advanced"),
    ("What is the process by which an atom loses or gains electrons?", "Fusion", "Fission", "Ionization", "Electromagnetism", 3, "Science", "advanced"),
    ("What is the unit of electrical resistance?", "Ampere", "Volt", "Ohm", "Watt", 3, "Science", "advanced"),
    ("What is the study of the universe called?", "Astronomy", "Astrophysics", "Cosmology", "Geophysics", 1, "Science", "advanced"),
    ("What element is the basis of all organic life?", "Oxygen", "Hydrogen", "Carbon", "Nitrogen", 3, "Science", "advanced"),
    ("What is the smallest unit of life?", "Cell", "Atom", "Molecule", "Organism", 1, "Science", "advanced"),
    ("What is the most common type of star in the universe?", "Red Giant", "White Dwarf", "Main Sequence", "Supernova", 3, "Science", "advanced"),
    ("What is the process by which cells divide?", "Meiosis", "Mitosis", "Cytokinesis", "Transcription", 2, "Science", "advanced"),
    ("What is the name of the first synthetic element?", "Uranium", "Plutonium", "Neptunium", "Technetium", 2, "Science", "advanced"),

    # History
    # Beginner
    ("What year was the Declaration of Independence signed?", "1776", "1789", "1800", "1812", 1, "History", "beginner"),
    ("Who was the first President of the United States?", "Abraham Lincoln", "George Washington", "John Adams", "Thomas Jefferson", 2, "History", "beginner"),
    ("Who discovered America in 1492?", "Marco Polo", "Christopher Columbus", "Ferdinand Magellan", "Amerigo Vespucci", 2, "History", "beginner"),
    ("What is the name of the first manned mission to land on the moon?", "Apollo 11", "Apollo 13", "Gemini 7", "Voyager 1", 1, "History", "beginner"),
    ("Who was known as the Iron Lady?", "Margaret Thatcher", "Angela Merkel", "Indira Gandhi", "Queen Elizabeth I", 1, "History", "beginner"),

    # Intermediate
    ("What year did the Titanic sink?", "1910", "1912", "1914", "1916", 2, "History", "intermediate"),
    ("In which year did World War II end?", "1940", "1942", "1945", "1950", 3, "History", "intermediate"),
    ("What was the name of the ship on which the Pilgrims traveled to America?", "Santa Maria", "Mayflower", "Endeavour", "Victoria", 2, "History", "intermediate"),
    ("Which empire was ruled by Julius Caesar?", "Ottoman Empire", "Roman Empire", "Byzantine Empire", "Mongol Empire", 2, "History", "intermediate"),
    ("Who was the leader of the Soviet Union during World War II?", "Stalin", "Lenin", "Trotsky", "Khrushchev", 1, "History", "intermediate"),
    ("Which country was formerly known as Persia?", "Iraq", "Afghanistan", "Iran", "Turkey", 3, "History", "intermediate"),
    ("Who was the famous queen of ancient Egypt?", "Cleopatra", "Nefertiti", "Hatshepsut", "Marie Antoinette", 2, "History", "intermediate"),
    ("Who was the first man to step on the moon?", "Neil Armstrong", "Buzz Aldrin", "Yuri Gagarin", "Alan Shepard", 1, "History", "intermediate"),
    ("When did the Berlin Wall fall?", "1985", "1987", "1989", "1991", 3, "History", "intermediate"),
    ("Who invented the telephone?", "Thomas Edison", "Alexander Graham Bell", "Nikola Tesla", "Guglielmo Marconi", 2, "History", "intermediate"),

    # Advanced
    ("In which year did the French Revolution begin?", "1789", "1776", "1800", "1812", 1, "History", "advanced"),
    ("Who was the first emperor of China?", "Shihuangdi", "Kublai Khan", "Sun Yat-sen", "Mao Zedong", 1, "History", "advanced"),
    ("What was the name of the first artificial satellite?", "Vostok 1", "Sputnik 1", "Explorer 1", "Apollo 11", 2, "History", "advanced"),
    ("Who was the first emperor of Rome?", "Julius Caesar", "Augustus", "Nero", "Caligula", 2, "History", "advanced"),
    ("What year did the Cold War officially end?", "1989", "1991", "1987", "1993", 2, "History", "advanced"),
    ("Who was the leader of the Mongol Empire?", "Kublai Khan", "Genghis Khan", "Tamerlane", "Attila the Hun", 2, "History", "advanced"),
    ("In which year did the United States enter World War I?", "1914", "1917", "1920", "1939", 2, "History", "advanced"),
    ("What was the name of the ship that brought the first Africans to the American colonies?", "Mayflower", "White Lion", "Endeavour", "Santa Maria", 2, "History", "advanced"),
    ("Who was the first woman to fly solo across the Atlantic?", "Amelia Earhart", "Bessie Coleman", "Harriet Quimby", "Jacqueline Cochran", 1, "History", "advanced"),
    ("In which year was the Magna Carta signed?", "1215", "1300", "1350", "1400", 1, "History", "advanced"),

    # Daily Challenge - Beginner
("What is the capital city of France?", "Paris", "London", "Rome", "Berlin", 1, "Daily Challenge", "beginner"),
("Which planet is known as the Red Planet?", "Mars", "Venus", "Earth", "Jupiter", 1, "Daily Challenge", "beginner"),
("What is the largest ocean on Earth?", "Atlantic Ocean", "Indian Ocean", "Southern Ocean", "Pacific Ocean", 4, "Daily Challenge", "beginner"),
("Who painted the Mona Lisa?", "Vincent van Gogh", "Leonardo da Vinci", "Pablo Picasso", "Claude Monet", 2, "Daily Challenge", "beginner"),
("Which animal is known as the King of the Jungle?", "Lion", "Tiger", "Elephant", "Gorilla", 1, "Daily Challenge", "beginner"),

# Daily Challenge - Intermediate
("Who invented the light bulb?", "Nikola Tesla", "Thomas Edison", "Alexander Graham Bell", "Benjamin Franklin", 2, "Daily Challenge", "intermediate"),
("Which country is known as the Land of the Rising Sun?", "China", "South Korea", "Japan", "Thailand", 3, "Daily Challenge", "intermediate"),
("What is the largest continent by land area?", "Africa", "Europe", "Asia", "North America", 3, "Daily Challenge", "intermediate"),
("What is the longest river in the world?", "Amazon River", "Nile River", "Yangtze River", "Mississippi River", 2, "Daily Challenge", "intermediate"),
("In what year did the Titanic sink?", "1910", "1912", "1914", "1916", 2, "Daily Challenge", "intermediate"),

# Daily Challenge - Advanced
("Who developed the theory of relativity?", "Isaac Newton", "Albert Einstein", "Galileo Galilei", "Niels Bohr", 2, "Daily Challenge", "advanced"),
("What is the capital city of Canada?", "Toronto", "Ottawa", "Vancouver", "Montreal", 2, "Daily Challenge", "advanced"),
("Who wrote the play 'Romeo and Juliet'?", "William Shakespeare", "Charles Dickens", "Mark Twain", "Jane Austen", 1, "Daily Challenge", "advanced"),
("Which country was the first to land a man on the moon?", "Soviet Union", "United States", "China", "India", 2, "Daily Challenge", "advanced"),
("In what year did World War I begin?", "1900", "1914", "1917", "1920", 2, "Daily Challenge", "advanced"),







    
]


    cursor.executemany(''' 
        INSERT INTO questions (question_text, option1, option2, option3, option4, correct_option, category, difficulty) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', sample_questions)

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database setup completed successfully!")
