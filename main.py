from fastapi import FastAPI, HTTPException
from name_model import NameModel
from name_repository import add_name
from tmp_database import tmp_db

app = FastAPI()


@app.post("/createName")
def create_name(input_name: NameModel):
    # 이름이 비어있는 경우
    if not input_name.name or input_name.name.strip() == "":
        raise HTTPException(status_code=400, detail="이름은 비어있을 수 없습니다")

    # 이름이 50자 이상인 경우
    if len(input_name.name) > 50:
        raise HTTPException(status_code=400, detail="이름이 너무 깁니다 (최대 50자)")

    # 이름이 이미 존재하는 경우
    if input_name.name in tmp_db:
        raise HTTPException(status_code=400, detail="이름이 이미 존재합니다")

    # 성공!
    try:
        add_name(input_name.name)
        return {"message": "이름이 추가되었습니다", "name": input_name.name}
    except Exception as e:
        # 예상치 못한 오류가 발생한 경우
        raise HTTPException(
            status_code=500, detail="서버 오류가 발생했습니다 : " + str(e)
        )


@app.get("/getName")
def get_names():
    # 이름을 레포지토리를 사용해서 가져오기
    names = get_names()

    try:
        # 이름이 없는 경우
        if not tmp_db:
            return {"message": "등록된 이름이 없습니다", "names": names}
        # 성공!
        return {"message": "이름 목록을 가져왔습니다", "names": names}
    except Exception as e:
        # 예상치 못한 오류가 발생한 경우
        raise HTTPException(
            status_code=500, detail="서버 오류가 발생했습니다 : " + str(e)
        )
