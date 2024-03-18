import csv
import sys
import typing as t

### Utility Functions ###

#loading data
# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass

def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]

# breath first implementation

class Node:
    
    def __init__(self, state: str, parent, action: str):
        self.parent = parent
        self.action = action
        self.state = state

class Queue:

    def __init__(self):
        self.q: t.List[Node] = []

    def length(self):
        return len(self.q)
    
    def is_empty(self):
        return self.length == 0
    
    def is_state_present(self, state: str):
        return any(state == node.state for node in self.q)

    def add(self, node: Node):
        self.q.append(node)

    def remove(self) -> t.Union[Node, None]:
        if self.is_empty():
            return None
        return self.q.pop(0)

class Degree:

    def __init__(self):
        self.frontier = Queue()

    def get_neighbours(self, node: Node):
        neighbors = set()
        for movie_id in people[node.state]["movies"]:
            for person_id in movies[movie_id]["stars"]:
                if not self.frontier.is_state_present(person_id):
                    neighbors.add(Node(state=person_id, action=movie_id, parent=node))

        return neighbors
        

    def solve(self, start: str, goal: str):
        #initialising the queue frontier
        start_person_id = person_id_for_name(name=start)
        goal_person_id = person_id_for_name(name=goal)
        start_node = Node(state=start_person_id, parent=None, action=None)
        self.frontier.add(start_node)

        while (node := self.frontier.remove()):
            if node.state == goal_person_id:
                path = []
                while node.parent is not None:
                    path.append((node.state, node.action))
                    node = node.parent
                path.append((node.state, node.action))
                return path

            # explore other nodes
            if (neighbors := self.get_neighbours(node)):
                for neighbor in neighbors:
                    self.frontier.add(neighbor)
        return None




        





    




