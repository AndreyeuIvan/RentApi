from pydantic import BaseModel, ValidationError


class City(BaseModel):
    city_id: int
    name: str
    population: int


input_json = """
{
    "city_id":123,
    "name":"Moscow",
    "population":"wow"
}
"""
try:
    city = City.parse_raw(input_json)
except ValidationError as e:
    print(e.json())
print(city)
