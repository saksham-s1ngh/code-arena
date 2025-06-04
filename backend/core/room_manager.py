import uuid

class RoomManager:
    def __init__(self):
        self.rooms = {} # room_id -> {host, question_url, users}

    def create_room(self, host_user, question_url):
        room_id = str(uuid.uuid4())
        self.rooms[room_id] = {
            "host": host_user.username,
            "question_url": question_url, 
            "users": [host_user.username]
        }
        return room_id
    
    def join_room(self, room_id, user):
        room = self.rooms.get(room_id)
        if room and user.username not in room["users"]:
            room["users"].append(user.username)
            return True # joined successfully
        return False
    
    def get_room(self, room_id):
        return self.rooms.get(room_id)
    
room_manager = RoomManager()