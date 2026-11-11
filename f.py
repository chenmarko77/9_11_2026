from fastapi import FastAPI, Path, Query,  Header, HTTPException, status

app = FastAPI()

users = []


def add_user(username: str) -> None:
    if username in users:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists",
        )
    users.append(username)


@app.post("/users/{username}")
def create_user(username: str):
    add_user(username)
    return {"message": f"User {username} added successfully"}


@app.get("/users")
def get_users():
    return {"users": users}


@app.delete("/users/{username}")
def delete_user(username: str):
    if username not in users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    users.remove(username)
    return {"message": f"User {username} deleted successfully"}


# @app.get("/items/")
# async def read_items(
#     skip: int = Query(0, title="Кількість записів для пропуску"),
#     limit: int = Query(10, title="Максимальна кількість записів"),
#     step: int = Query(1, title="Крок для генерації списку")
# ):
#     # items = get_items_from_db(skip, limit)
#     # return {"items": items}
#     return



@app.get("/range")
async def get_range(
    end: int = Query(..., title="Кінець послідовності"),
    start: int = Query(0, title="Початок послідовності"),
    step: int = Query(1, title="Крок послідовності"),
):
    return list(range(start, end, step))



@app.get("/username/{message}")
def get_message(message: str = Path(..., min_length=3, max_length=100,
                                    title="username RULES!",
                                    description="username minimum 3 characters, maximum 100 characters")):
    return {"message": message}



@app.get("/groups/{group_id}/students/{student_id}")
def get_message(group_id: str = Path(..., min_length=1, max_length=100,
                                     title="Group ID",
                                     description="Group ID minimum 1 character, maximum 100 characters"),
                student_id: str = Path(..., min_length=1, max_length=100,
                                        title="Student ID",
                                        description="Student ID minimum 1 character, maximum 100 characters")):
    return {"student": student_id, "studies in group": group_id}




@app.get("/data/")
async def read_data(
    authorization: str = Header(...),
    x_custom_header: str = Header(None),
):
    if authorization != "Bearer mysecrettoken":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )

    response = {"message": "Authorized"}
    if x_custom_header is not None:
        response["X-Custom-Header"] = x_custom_header
    return response


@app.get("/user-agent/")
async def read_user_agent(user_agent: str = Header(None)):
    if user_agent is None:
        return {"message": "User-Agent header is missing"}
    return {"User-Agent": user_agent}