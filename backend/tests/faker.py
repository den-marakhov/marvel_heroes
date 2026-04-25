from faker import Faker
from datetime import UTC, datetime
from uuid import UUID, uuid4

from src.domain.constants import ALLOWED_NAMES

_faker = Faker()


def get_faker() -> Faker:
	return _faker

def uuid4() -> UUID:
	return _faker.uuid4(cast_to=None)

def text() -> str:
	return _faker.text(max_nb_chars=500)

def datetime_current_century() -> datetime:
	return _faker.date_time_this_century(tzinfo=UTC)

def random_int() -> int:
	return _faker.random_int(min=1)

def full_name() -> str:
	return _faker.name()

def hero_name() -> str:
	return _faker.random.choice(ALLOWED_NAMES)

def image_url() -> str:
	return f"/uploads/heroes/{uuid4()}.webp"