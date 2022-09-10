from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, models, oauth2
from ..database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])

# Get all posts
# * Response has to be a list of PostResponse
@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(
    db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)
):
    # // cursor.execute("SELECT * FROM posts")
    # // posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts


# Create a new post
@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse
)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):
    # // cursor.execute(
    # //     # ! This is vulnerable to SQL injection, so can't use F Strings
    # //     "INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING *",
    # //     (post.title, post.content, post.published),
    # // )
    # // new_post = cursor.fetchone()
    # // # Commit changes to DB (required for INSERT)
    # // conn.commit()

    print(current_user.email)

    # * Unpacking the dictionary to retrieve all fields automatically
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    # SQLAlchemy way to return the new post
    db.refresh(new_post)
    return new_post


# Get a post by id
@router.get("/{post_id}", response_model=schemas.PostResponse)
def get_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):
    # // Requires to be parsed as string so it works with SQL (but can't change due to validation)
    # // ! Comma is needed, as second argument MUST be a tuple or list
    # // cursor.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
    # // post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID: {post_id} was not found",
        )
    return post


# Delete a post
@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):
    # // cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (post_id,))
    # // deleted_post = cursor.fetchone()
    # // # Commit changes to DB (required for DELETE)
    # // conn.commit()
    deleted_post = db.query(models.Post).filter(models.Post.id == post_id)
    if deleted_post.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID: {post_id} was not found",
        )
    deleted_post.delete(synchronize_session=False)
    db.commit()
    # * not sending data at all, as 204 specification requires no data to be sent back
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update a post
@router.put("/{post_id}", response_model=schemas.PostResponse)
def update_post(
    post_id: int,
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):
    # // cursor.execute(
    # //     "UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s",
    # //     (post.title, post.content, post.published, str(post_id)),
    # // )
    # // # Commit changes to DB (required for UPDATE)
    # // conn.commit()
    # // # * It seems no returning is allowed after UPDATE so selecting from rows again
    # // cursor.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
    # // updated_post = cursor.fetchone()
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    found_post = post_query.first()

    if found_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID: {post_id} was not found",
        )

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
