from typing import List

from fastapi import APIRouter, Depends, HTTPException, File, Body
import os

from starlette.responses import FileResponse
import hashlib
from dependencies import get_current_user
from repository.file_rep import FileRepository
from schemas import FileBase

router = APIRouter(
    prefix="/files",
    tags=["files"],
)



@router.post('/upload')
async def file_upload(file: bytes = File(..., max_length=15000000),
                      file_name: str = Body(...), user: str = Depends(get_current_user),
                      repfile: FileRepository = Depends()):
    hash_content=hashlib.md5(file).hexdigest()
    print(hash_content)
    if repfile.find_by_hash(hash_content):
        raise HTTPException(status_code=400,
                            detail="this file already exist")
    if not os.path.exists(f"./media/{user}"):
        os.mkdir(f"./media/{user}")
    with open(f'./media/{user}/{file_name}', 'wb') as buffer:
        buffer.write(file)

    url = repfile.url_exist(f'./media/{user}/{file_name}')

    if url:
        raise HTTPException(status_code=400,
                            detail="file with the same name already exist")
    repfile.create(f'./media/{user}/{file_name}', user, file_name,hash_content)

    return {'filename': file_name, 'size': len(file)}


@router.get("/{username}/", response_model=List[FileBase])
async def file_list(username: str, user: str = Depends(get_current_user), repfile: FileRepository = Depends()):
    if username != user:
        raise HTTPException(status_code=405,
                            detail="no access", )
    files = repfile.find_user_file(username)
    return files


@router.get("/{username}/{filename}")
async def file_get(username: str, filename: str, user: str = Depends(get_current_user),
                        repfile: FileRepository = Depends()):
    if user != username:
        raise HTTPException(status_code=405,
                            detail="no access", )
    url = f'./media/{user}/{filename}'
    if not (repfile.url_exist(url)):
        raise HTTPException(status_code=405,
                            detail="file not exist", )

    return FileResponse(url)


@router.delete("/{username}/{filename}")
async def file_delete(username: str, filename: str, user: str = Depends(get_current_user), repfile: FileRepository = Depends()):
    if username != user:
        raise HTTPException(status_code=405,
                            detail="no access", )
    url = f'./media/{user}/{filename}'
    if not (repfile.url_exist(url)):
        raise HTTPException(status_code=405,
                            detail="file not exist", )
    repfile.delete_file(url)
    os.remove(url)
    return {'detail':'file was delete'}