from typing import Dict, List, Optional

from app.api import GenericException, ItemAlreadyExist, NoItemFoundException
from app.db.cruds import (
    create_device,
    delete_device,
    get_device,
    get_devices,
    update_device,
)
from app.db.schema import DeviceSchema, get_db_generator
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import DataError, IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

device_router = APIRouter()


@device_router.post("/devices", response_model=DeviceSchema)
def create_device_item(
    device_information: DeviceSchema,
    db: Session = Depends(get_db_generator),
):
    """
    Create device.

    Arguments:
        device_information {DeviceSchema} -- New device information.
        db {Session} -- Database session.

    Returns:
        Union[DeviceSchema, ItemAlreadyExist] -- Device instance that was added
        to the database or an error in case the device already exists.
    """
    try:
        device_information = jsonable_encoder(device_information)
        return create_device(
            db_session=db, device_information=device_information
        )
    except IntegrityError:
        raise ItemAlreadyExist()


@device_router.get("/devices/{device_id}", response_model=DeviceSchema)
def get_device_item(
    device_id: str,
    db: Session = Depends(get_db_generator),
):
    """
    Get existing device.

    Arguments:
        device_id {str} -- Device id.
        db {Session} -- Database session.

    Returns:
        Union[DeviceSchema, NoItemFoundException] -- Device instance which id is device_id
        or an exception in case there's no matching device.

    """
    try:
        return get_device(db_session=db, device_id=device_id)
    except NoResultFound:
        raise NoItemFoundException()


@device_router.get(
    "/devices",
    response_model=List[DeviceSchema],
    response_model_include={"id", "description"},
)
def get_devices_items(db: Session = Depends(get_db_generator)):
    """
    Get all existing devices.

    Arguments:
        db {Session} -- Database session.

    Returns:
        List[DeviceSchema] -- All device instances present in the database.
    """
    return get_devices(db_session=db)


@device_router.put("/devices/{device_id}", response_model=DeviceSchema)
def update_device_item(
    device_id: str,
    new_device_information: Dict = {},
    db: Session = Depends(get_db_generator),
):
    """
    Modify a device.

    Arguments:
        device_id {str} -- Device id.
        new_device_information {Dict} -- New device information.
        db {Session} -- Database session.

    Returns:
        Union[DeviceSchema, NoItemFoundException, GenericException] -- Device instance
        which id is device_id or an exception in case there's no matching device.
    """
    try:
        return update_device(
            db_session=db,
            device_id=device_id,
            new_device_information=new_device_information,
        )
    except NoResultFound:
        raise NoItemFoundException()
    except DataError as e:
        raise GenericException(e)


@device_router.delete("/devices/{device_id}", response_model=DeviceSchema)
def delete_device_item(
    device_id: str,
    db: Session = Depends(get_db_generator),
):
    """
    Delete a device.

    Arguments:
        device_id {str} -- Device id.
        db {Session} -- Database session.

    Returns:
        Union[DeviceSchema, NoItemFoundException, GenericException] -- Device instance that
        was deleted or an exception in case there's no matching device.
    """
    try:
        return delete_device(db_session=db, device_id=device_id)
    except NoResultFound:
        raise NoItemFoundException()
    except DataError as e:
        raise GenericException(e)