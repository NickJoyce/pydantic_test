from pydantic import BaseModel, ValidationError, Field, validator


class Tag(BaseModel):
    id: int
    tag: str


class City(BaseModel):
    city_id: int
    name: str = Field(alias="cityFullName")
    tags: list[Tag]

    @validator('name')
    def name_should_be_spb(cls, value: str) -> str:
        if 'spb' not in value.lower():
            raise ValueError("Work with SPB")
        else:
            return value


class UserWithoutPassword(BaseModel):
    name: str
    email: str


class User(UserWithoutPassword):
    password: str


if __name__ == "__main__":
    input_json = """
    {   
        "city_id": 123,
        "cityFullName": "Moscow",
        "tags": [{
            "id": 1, "tag": "capital"
        },
        {
            "id": 2, "tag": "big city"
        }]
    }
    """
    try:
        city = City.parse_raw(input_json)
    except ValidationError as e:
        print(e.json())
    else:
        print(city)
        print(city.json(by_alias=True, exclude={"city_id"}))
        tag = city.tags[0]
        print(tag.json())
