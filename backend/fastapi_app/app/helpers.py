from uuid import UUID
class Get_info:
    def __init__(self, id: str):  # Konstruktor to'g'ri nomlanishi kerak: __init__
        self.id = id

    def __str__(self) -> str:  # Ob'ektni stringga aylantiruvchi metod
        return f"Get_post obyekti: {self.id}"

    def get_first_part(self):
        data = str(self.id).split("-")[1]
        result = data[-3:]
        return result

    def get_from_id(self, from_database):
        result = ''.join(map(lambda part: part[-3:], str(self.id).split("-")))
        print(from_database, self.id, result)
        if self.id == from_database:
            return "successfully"
        return "Moslik yo'q"  # Hech qaysi element mos kelmasa, tsikldan keyin qaytaradi
    # return "Moslik yo'q"  # Hech qaysi element mos kelmasa, tsikldan keyin qaytaradi


# id = "19dea53b-686a-48c5-963c-d5c44dd39804"
#
# check_user = ["19dea53b-686a-48c5-963c-d5c44dd39805", "19dea53b-686a-48c5-963c-d5c44dd39806", "19dea53b-686a-48c5-963c-d5c44dd39807", "19dea53b-686a-48c5-963c-d5c44dd39804"]
# furniture_id = UUID(id)
# print((furniture_id))
# check_id = Get_info(furniture_id)
# print("ssssssssssssssssssss", check_id)
#
# print("fffffffffffffffffffffffffff", check_id.get_from_id(check_user))
