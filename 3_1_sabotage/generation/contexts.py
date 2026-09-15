"""Name, word, and task pools used by build_prompts.py; no API calls."""

NAMES = [
    # Gender-neutral / Ambiguous
    "Jordan", "Sam", "Morgan", "Casey", "Riley", "Quinn", "Avery", "Taylor", "Jamie", "Drew",
    "Skyler", "Reese", "Finley", "Rowan", "Sage", "Parker", "Cameron", "Charlie", "Dakota",
    "Devon", "Emerson", "Harper", "Hayden", "Jesse", "Kai", "Kendall", "Lane", "Lee", "Marley",
    "Micah", "Noel", "Phoenix", "River", "Robin", "Shawn", "Sidney", "Terry", "Tristan", "Wren",

    # Traditional English - Male-leaning
    "Mike", "Danny", "Chris", "Matt", "Jake", "Ryan", "Brian", "Kevin", "Tom", "Ben", "Nick",
    "Steve", "Eric", "Jason", "Mark", "David", "Adam", "Andrew", "Brad", "Brandon", "Caleb",
    "Cody", "Daniel", "Ethan", "Frank", "George", "Greg", "Henry", "Jack", "James", "Jeff", "John",
    "Josh", "Justin", "Kyle", "Luke", "Nathan", "Noah", "Paul", "Peter", "Robert", "Scott", "Sean",
    "Tim", "Tyler", "Will", "Zach",

    # Traditional English - Female-leaning
    "Sarah", "Emily", "Jessica", "Rachel", "Lauren", "Amanda", "Megan", "Katie", "Lisa", "Jenny",
    "Nicole", "Ashley", "Heather", "Stephanie", "Becky", "Tina", "Abigail", "Allison", "Anna",
    "Brittany", "Chloe", "Courtney", "Danielle", "Elizabeth", "Emma", "Erin", "Gabrielle", "Grace",
    "Hannah", "Jillian", "Julia", "Kelly", "Kim", "Kristen", "Laura", "Madison", "Molly",
    "Natalie", "Olivia", "Samantha", "Vanessa", "Victoria", "Zoe",

    # Indian
    "Priya", "Raj", "Ananya", "Vikram", "Neha", "Arjun", "Kavita", "Sanjay", "Deepa", "Amit",
    "Sunita", "Rohan", "Meera", "Aditya", "Pooja", "Nikhil", "Asha", "Rahul", "Kiran", "Divya",
    "Isha", "Shreya", "Varun", "Siddharth", "Gaurav", "Pranav", "Shruti", "Sneha", "Manish",
    "Suresh", "Jaya", "Mahesh", "Payal", "Tanvi", "Anil", "Ritu",

    # Chinese
    "Wei", "Ming", "Jing", "Chen", "Lin", "Hui", "Xin", "Lei", "Yan", "Feng", "Hong", "Ping",
    "Ling", "Jun", "Mei", "Tao", "Li", "Xiao", "Ying", "Lan", "Bo", "Rui", "Yao", "Qiang", "Shu",
    "Zhi", "Zhen", "Ting", "Guo", "Shan",

    # Japanese
    "Yuki", "Kenji", "Sakura", "Haruto", "Aiko", "Takeshi", "Naomi", "Ryo", "Akira", "Hiroshi",
    "Hana", "Kaito", "Emi", "Satoshi", "Yoko", "Ren", "Mika", "Shin", "Aya", "Daichi", "Mai",
    "Ryota",

    # Hispanic/Latino
    "Carlos", "Maria", "Diego", "Sofia", "Miguel", "Isabella", "Javier", "Lucia", "Rosa", "Marco",
    "Elena", "Luis", "Carmen", "Pedro", "Ana", "Rafael", "Juan", "Jose", "Andres", "Fernando",
    "Gabriel", "Alejandro", "Francisco", "Ricardo", "Manuel", "Pablo", "Roberto", "Daniela",
    "Gabriela", "Valeria", "Camila", "Mariana", "Natalia", "Patricia", "Veronica", "Luisa",

    # Italian
    "Luca", "Giulia", "Francesca", "Alessandro", "Chiara", "Matteo", "Valentina", "Giovanni",
    "Paolo", "Stefano", "Federico", "Giorgio", "Filippo", "Alberto", "Claudia", "Silvia",
    "Martina", "Elisa", "Giovanna", "Davide", "Simone",

    # Middle Eastern / Persian
    "Fatima", "Omar", "Layla", "Hassan", "Zahra", "Karim", "Nadia", "Amir", "Ali", "Reza",
    "Yasmin", "Samira", "Farah", "Noor", "Amina", "Khalid", "Hadi", "Samir", "Salma", "Maryam",
    "Zain", "Rami",

    # Korean
    "Jin", "Soo", "Minji", "Hyun", "Jae", "Yuna", "Jisoo", "Jihoon", "Seojun", "Eunji", "Sumin",
    "Taehyun", "Hyejin", "Seungmin", "Joon", "Jiwoo",

    # Eastern European
    "Oleksandr", "Katya", "Dmitri", "Anya", "Ivan", "Natasha", "Andrei", "Nikolai", "Sergei",
    "Mikhail", "Viktor", "Olga", "Irina", "Anastasia", "Yulia", "Svetlana", "Pavel", "Boris",
    "Mila",

    # African
    "Kwame", "Amara", "Kofi", "Zara", "Nia", "Malik", "Imani", "Jabari", "Adewale", "Chidi",
    "Chioma", "Ngozi", "Nnamdi", "Lerato", "Thandi", "Zanele",

    # French / Francophone
    "Remy", "Camille", "Julien", "Pierre", "Luc", "Hugo", "Celine", "Amelie", "Sophie", "Andre",
    "Marcel", "Nina",

    # German / Scandinavian
    "Lars", "Sven", "Ingrid", "Greta", "Anja", "Heidi", "Klaus", "Hans", "Lea", "Nils",

    # Southeast Asian
    "Anh", "Thuy", "Trang", "Huy", "Tuan", "Phuong", "Lan", "Minh", "Bao", "Aria", "Narin",
    "Somchai", "Priyom", "Lani", "Mariel",
]

WORDS_COMMON = [
    # Time
    "tomorrow", "yesterday", "weekend", "morning", "afternoon", "evening", "midnight", "deadline",
    "schedule", "calendar", "hourly", "weekly", "monthly", "later", "earlier",

    # Objects
    "coffee", "laptop", "phone", "notebook", "window", "desk", "chair", "keyboard", "screen",
    "folder", "charger", "headphones", "printer", "bottle", "blanket",

    # Actions
    "remember", "forget", "check", "update", "review", "confirm", "finish", "start", "pause",
    "continue", "adjust", "organize", "compare", "arrange", "submit",

    # Descriptors
    "quick", "simple", "perfect", "great", "excellent", "solid", "smooth", "clean", "fresh",
    "ready", "basic", "obvious", "tricky", "urgent", "flexible",

    # Places
    "office", "home", "building", "floor", "room", "hallway", "parking", "elevator", "lobby",
    "kitchen", "garage", "bedroom", "bathroom", "garden", "basement",

    # People
    "manager", "colleague", "teammate", "intern", "boss", "client", "vendor", "partner",
    "assistant", "director", "neighbor", "cousin", "landlord", "stranger", "guest",

    # Feelings/States
    "busy", "tired", "relieved", "frustrated", "excited", "confused", "confident", "nervous",
    "curious", "satisfied", "overwhelmed", "relaxed", "impatient", "grateful", "skeptical",

    # Misc
    "email", "message", "meeting", "lunch", "break", "project", "report", "document", "version",
    "draft", "budget", "recipe", "password", "reminder", "backup",
]

CONTEXT_CATEGORIES = {
    "trip_planning": {
        "description": "Two people planning a trip together",
        "subcategories": [
            "choosing a destination from a shortlist",
            "setting a travel budget",
            "picking between hotel, Airbnb, or hostel",
            "creating a daily itinerary",
            "finding restaurants and food spots to try",
            "prioritizing activities and sightseeing",
            "figuring out transportation logistics",
            "finding travel dates that work",
            "deciding whether to rent a car or use transit",
            "making a packing list for the trip",
        ],
    },
    "cooking_together": {
        "description": "Two people planning or preparing a meal together",
        "subcategories": [
            "choosing a menu for a dinner party",
            "splitting up cooking tasks",
            "picking a cuisine for the evening",
            "weekly meal prep planning",
            "ingredient substitutions for a recipe",
            "figuring out what to make with limited pantry items",
            "planning a holiday feast menu",
            "choosing between two competing recipes",
            "handling dietary restrictions for guests",
            "potluck dish selection",
        ],
    },
    "entertainment_choices": {
        "description": "Two people deciding on entertainment or discussing media",
        "subcategories": [
            "picking a movie for the evening",
            "choosing a new TV series to start",
            "a book they recently read",
            "selecting a board game for game night",
            "thoughts on a recent movie",
            "building a road trip playlist",
            "finding a video game to play",
            "choosing a podcast for a long drive",
            "picking a concert or show to attend",
            "ranking entries in a movie or book franchise",
        ],
    },
    "event_organizing": {
        "description": "Two people co-organizing a social event",
        "subcategories": [
            "planning a surprise birthday party",
            "organizing a housewarming party",
            "putting together a group outing",
            "planning a holiday gathering",
            "organizing a going-away party",
            "setting up a game night or trivia event",
            "planning a baby shower",
            "choosing decorations and a theme for a party",
            "managing a guest list and RSVPs",
            "planning activities for a reunion",
        ],
    },
    "home_project": {
        "description": "Two people tackling a home project together",
        "subcategories": [
            "redecorating a living room",
            "planning a garden or balcony setup",
            "organizing a garage or storage space",
            "choosing paint colors for a room",
            "assembling new furniture",
            "setting up a home office",
            "planning a backyard barbecue area",
            "rearranging a kitchen layout",
            "building shelves or storage solutions",
            "choosing plants for a garden",
        ],
    },
    "fitness_together": {
        "description": "Two people discussing exercise or health goals",
        "subcategories": [
            "designing a workout routine",
            "choosing a gym or fitness class",
            "tracking progress on fitness goals",
            "diet approaches for training",
            "picking a race or event to sign up for",
            "planning outdoor activities for the weekend",
            "choosing a hiking or cycling route",
            "recovery and rest day strategies",
            "trying a new sport",
            "setting up a fitness challenge",
        ],
    },
    "shopping_decisions": {
        "description": "Two people making a purchase decision",
        "subcategories": [
            "choosing a gift for someone",
            "picking a household appliance",
            "selecting furniture for a room",
            "choosing a subscription service",
            "picking outfits for an event",
            "choosing between phone or laptop options",
            "selecting a streaming service",
            "picking supplies for a hobby",
            "choosing where to do grocery shopping",
            "finding the best deals on a purchase",
        ],
    },
    "pet_decisions": {
        "description": "Two people making decisions about a pet",
        "subcategories": [
            "choosing what breed or type of pet to adopt",
            "picking a vet",
            "choosing a pet food brand and diet",
            "dividing pet care responsibilities",
            "choosing a training approach for a new puppy",
            "selecting a pet sitter or boarding option",
            "whether to get a second pet",
            "planning a pet-friendly vacation",
            "grooming at home vs professional groomer",
            "choosing pet insurance",
        ],
    },
    "career_peers": {
        "description": "Two people discussing career and professional situations",
        "subcategories": [
            "dealing with a difficult coworker",
            "whether to attend a networking event",
            "the value of a certification or course",
            "a recent company policy change",
            "side project or freelance ideas",
            "managing work-life balance",
            "applying for an internal role",
            "handling a team conflict",
            "strategies for meeting a deadline",
            "evaluating job offers or career moves",
        ],
    },
    "parenting_peers": {
        "description": "Two people discussing parenting approaches and decisions about kids",
        "subcategories": [
            "screen time rules for kids",
            "planning a family outing or playdate",
            "school choice for children",
            "allowance and chore systems",
            "handling toddler tantrums",
            "carpool logistics",
            "extracurricular activity options for kids",
            "bedtime routine strategies",
            "planning a kids' birthday party",
            "handling a conflict between kids",
        ],
    },
    "weekend_plans": {
        "description": "Two people deciding what to do over the weekend",
        "subcategories": [
            "choosing between outdoor and indoor activities",
            "picking a day trip destination",
            "planning a relaxing vs active weekend",
            "choosing a new restaurant to try",
            "whether to host people or go out",
            "planning a spontaneous road trip",
            "what to do on a rainy day",
            "choosing between a market, museum, or park",
            "planning a beach or lake day",
            "picking a brunch spot",
        ],
    },
    "roommate_logistics": {
        "description": "Two people coordinating household matters",
        "subcategories": [
            "a fair chore division system",
            "setting quiet hours and noise rules",
            "grocery shopping responsibilities",
            "use of common areas",
            "thermostat and utility settings",
            "handling a maintenance request",
            "organizing a food and grocery system",
            "guest and overnight visitor policies",
            "bathroom and morning schedules",
            "managing subscriptions and bills",
        ],
    },
    "hobby_collaboration": {
        "description": "Two people collaborating on a hobby or creative project",
        "subcategories": [
            "planning a photography outing",
            "a creative writing project",
            "choosing a DIY craft project",
            "an art or painting session",
            "a woodworking project idea",
            "learning a new cooking technique",
            "planning a music jam session",
            "building something in a video game",
            "a podcast or video idea",
            "a coding side project",
        ],
    },
    "opinion_exchange": {
        "description": "Two people casually exchanging opinions",
        "subcategories": [
            "the best pizza toppings",
            "the greatest sports team of all time",
            "a controversial movie ending",
            "morning routines and productivity",
            "favorite travel destinations",
            "the best way to make coffee",
            "remote vs office work",
            "the best decade for music",
            "unusual food preferences",
            "which hobbies are worth picking up",
        ],
    },
}
