class User:
    def __init__ (self, user_id=None, username=None, first_name=None,
                  last_name=None, about=None, phone=None):
        if user_id:
            self._id = user_id
        if username:
            self._username = username
        if first_name:
            self._first_name = first_name
        if last_name:
            self._last_name = last_name
        if about:
            self._about = about
        if phone:
            self._phone = phone
