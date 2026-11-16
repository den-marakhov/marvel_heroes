from src.application.dtos.user import CreateUserDTO
from src.application.mappers.user import UserDtoEntityMapper
from src.domain.constants import ADMIN_ROLE


def test_to_entity_from_create_dto() -> None:
    mapper = UserDtoEntityMapper()
    dto = CreateUserDTO(
        email="admin@marvel.local",
        name="Admin",
        role=ADMIN_ROLE,
        password_hash="hashed-password",
    )

    entity = mapper.to_entity_from_create_dto(dto)

    assert entity.email.value == dto.email
    assert entity.name.value == dto.name
    assert entity.role.value == dto.role
    assert entity.password_hash == dto.password_hash
    assert mapper.to_dto(entity).email == dto.email
