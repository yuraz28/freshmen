from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Response, UploadFile, File
from fastapi.responses import FileResponse
import jwt
from managers.users import authenticate_user, get_user_current
from models import User, Review, Paths_file
import asyncpg
from schemas import UserAllInfo, UserGet, UserAuth, CheckEmail, \
    CheckAnswer, AddReview, AddFile, DownloadFile
from passlib.hash import bcrypt
import ormar
import aiofiles
import os

JWT_SECRET = 'myjwtsecret'

router = APIRouter(
    prefix=""
)


@router.post('/')
async def auth(data: UserAuth):
    user = await authenticate_user(data.email, data.password_hash)
    if not user:
        return {'error': 'invaid credentials'}
    user = UserGet(
        id=str(user.id),
        email=user.email,
        password_hash=user.password_hash
    )

    token = jwt.encode(user.dict(), JWT_SECRET)
    return {'access_token': token, 'token_type': 'bearer'}


@router.post('/reg')
async def register(user: UserAllInfo):
    try:
        user.password_hash = bcrypt.hash(user.password_hash)
        user_dict = user.dict()
        await User.objects.create(**user_dict)
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(status_code=400, detail="User already exists")
    return Response(status_code=200, content="User created")


@router.post('/check_email')
async def check_email(email: CheckEmail):
    try:
        await User.objects.get(email=email.email)
        return CheckAnswer(answer=True)
    except ormar.exceptions.NoMatch:
        return CheckAnswer(answer=False)


@router.get('/me')
async def get_me(user=Depends(get_user_current)):
    user_get = await User.objects.get(id=user.id)
    return user_get


@router.post('/private/upload')
async def private_file_save(file_in: UploadFile = File(...), user=Depends(get_user_current)):
    file_add = AddFile(
        is_private=True,
        author_id=user.id,
        place_study=user.place_study,
        branch=user.branch,
        course=user.course,
        name=file_in.filename
    )

    await Paths_file.objects.create(**file_add.dict())
    async with aiofiles.open(f'data/private/{file_in.filename}', 'wb') as out_file:
        content = await file_in.read()
        await out_file.write(content)

    return Response(status_code=200, content="File caved")


@router.post('/upload')
async def file_save(file_in: UploadFile = File(...), user=Depends(get_user_current)):
    file_add = AddFile(
        is_private=False,
        author_id=user.id,
        place_study=user.place_study,
        branch=user.branch,
        course=user.course,
        name=file_in.filename
    )

    await Paths_file.objects.create(**file_add.dict())
    async with aiofiles.open(f'data/all/{file_in.filename}', 'wb') as out_file:
        content = await file_in.read()
        await out_file.write(content)

    return Response(status_code=200, content="File caved")


@router.get('/download_private')
async def download_private(user=Depends(get_user_current)):
    courses = await Paths_file.objects.filter(author_id=user.id).filter(is_private=True).all()
    return courses


@router.get('/download_all')
async def download_place_study(user=Depends(get_user_current)):
    courses_place_study = await Paths_file.objects.filter(place_study=user.place_study) \
        .filter(is_private=False).all()
    courses_branch = await Paths_file.objects.filter(branch=user.branch) \
        .filter(is_private=False).all()
    courses_branch_place_study = await Paths_file.objects.filter(branch=user.branch) \
        .filter(place_study=user.place_study).filter(is_private=False).all()
    place_study_branch_course = await Paths_file.objects.filter(branch=user.branch) \
        .filter(place_study=user.place_study).filter(is_private=False).filter(course=user.course).all()
    return DownloadFile(
        place_study=courses_place_study,
        branch=courses_branch,
        place_study_branch=courses_branch_place_study,
        place_study_branch_course=place_study_branch_course
    )


@router.get('/download/{file_id}')
async def download_file_id(file_id: UUID):
    file_out = await Paths_file.objects.get(id=file_id)
    if not file_out.is_private:
        return FileResponse(
            f"data/all/{file_out.name}",
            filename=file_out.name,
            media_type="application/octet-stream"
        )
    if file_out.author_id == user.id:
        return FileResponse(
            f"data/private/{file_out.name}",
            filename=file_out.name,
            media_type="application/octet-stream"
        )
    return Response(status_code=404, content="The user does not have access to the file")


@router.post('/reviews')
async def add_review(review: AddReview, user=Depends(get_user_current)):
    review.author_id = user.id
    review.branch = user.branch
    await Review.objects.create(**review.dict())
    return Response(status_code=200, content="Review created")


@router.get('/reviews')
async def get_reviews(user=Depends(get_user_current)):
    reviews_get = await Review.objects.filter(branch=user.branch).all()
    return reviews_get


@router.delete('/delete/{file_id}')
async def delete_courses(file_id: UUID, user=Depends(get_user_current)):
    file_out = await Paths_file.objects.get(id=file_id)
    if file_out.author_id == user.id:
        if file_out.is_private:
            os.remove(f'data/private/{file_out.name}')
        else:
            os.remove(f'data/all/{file_out.name}')
        await file_out.delete()
        return Response(status_code=200, content="File deleted")
    return Response(status_code=404, content="User is not author")
