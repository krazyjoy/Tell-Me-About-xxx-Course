from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()





stores = {}
items = {
    1:{
        "name": "chair",
        "price": 17.99
    },
    2:{
        "name": "table",
        "price": 45.00
    }

}

courses = {
    1:
        {
            "id": "fdjgrbzyinw",
            "Major": "CSE",
            "Class_Number": "411",
            "Name": "Human and Computer Interaction",
            "Instructor": "Rafem Howard",
            "Difficulty": 3,
            "Time": 6,
            "Usefulness": 1

        }


}

instructors = {
    1: {
	    "name": "Shan xuen chuin"
    },
    # 2:{
    #   "name":"Lee Jian Lone"
    # }
}
