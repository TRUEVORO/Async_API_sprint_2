from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, Query

from models import PersonFull, Persons
from services import PersonService, get_person_service

router = APIRouter(
    prefix='/api/v1/persons',
    tags=['persons'],
)


class PersonAPI(PersonFull):
    """API model for person."""

    pass


class PersonsAPI(Persons):
    """API model for list of persons."""

    total: int


@router.get(
    '/<{person_id}:UUID>/',
    response_model=PersonAPI,
    summary='Search person',
    description='Search person by id',
    response_description='Full person details',
)
async def person_details(
    person_id: Annotated[UUID, Path(title='person id', description='parameter - person id')],
    person_service: PersonService = Depends(get_person_service),
) -> PersonAPI | HTTPException:
    person = await person_service.get_by_id(person_id)
    return PersonAPI(**person.dict(by_alias=True))


@router.get(
    '',
    response_model=PersonsAPI,
    summary='Popular persons',
    description='Popular genres with sorting',
    response_description='Summary of persons',
)
async def persons_main(
    sort: Annotated[
        Literal['full_name', '-full_name'] | None, Query(title='sort', description='optional parameter - sort')
    ] = None,
    page: Annotated[int | None, Query(title='page number', description='optional parameter - page number', ge=1)] = 1,
    page_size: Annotated[int | None, Query(title='page size', description='optional parameter - page size', ge=1)] = 50,
    person_service: PersonService = Depends(get_person_service),
) -> PersonsAPI | HTTPException:
    persons, total = await person_service.search(sort_by=sort, page=page, page_size=page_size)
    return PersonsAPI(persons=persons, total=total)


@router.get(
    '/search',
    response_model=PersonsAPI,
    summary='Search persons',
    description='Full-text search of persons',
    response_description='Short info of the person with similar ones',
)
async def persons_search(
    query: Annotated[str | None, Query(title='query', description='optional parameter - query')] = None,
    sort: Annotated[
        Literal['full_name', '-full_name'] | None, Query(title='sort', description='optional parameter - sort')
    ] = None,
    page: Annotated[int | None, Query(title='page number', description='optional parameter - page number', ge=1)] = 1,
    page_size: Annotated[int | None, Query(title='page size', description='optional parameter - page size', ge=1)] = 50,
    person_service: PersonService = Depends(get_person_service),
) -> PersonsAPI | HTTPException:
    persons, total = await person_service.search(query=query, sort_by=sort, page=page, page_size=page_size)
    return PersonsAPI(persons=persons, total=total)
