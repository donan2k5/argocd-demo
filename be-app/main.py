import os, random
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator

ERROR_RATE = float(os.getenv("ERROR_RATE", "0"))
VERSION = os.getenv("VERSION", "v1")

app = FastAPI(title="Da Nang Places API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

Instrumentator().instrument(app).expose(app)


class Place(BaseModel):
    id: int
    name: str
    description: str
    category: str
    image_url: str


PLACES: List[Place] = [
    Place(
        id=1,
        name="Cầu Vàng - Bà Nà Hills",
        description="Cây cầu nổi tiếng thế giới được đỡ bởi hai bàn tay khổng lồ trên độ cao 1400m.",
        category="Danh lam thắng cảnh",
        image_url="https://images.unsplash.com/photo-1559592413-7cec4d0cae2b?w=800&q=80",
    ),
    Place(
        id=2,
        name="Bãi biển Mỹ Khê",
        description="Một trong những bãi biển đẹp nhất hành tinh theo Forbes, cát trắng mịn trải dài 9km.",
        category="Bãi biển",
        image_url="https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&q=80",
    ),
    Place(
        id=3,
        name="Cầu Rồng",
        description="Cây cầu hình rồng phun lửa và nước vào cuối tuần, biểu tượng của Đà Nẵng hiện đại.",
        category="Kiến trúc",
        image_url="https://images.unsplash.com/photo-1548013146-72479768bada?w=800&q=80",
    ),
    Place(
        id=4,
        name="Ngũ Hành Sơn",
        description="Cụm 5 ngọn núi đá cẩm thạch huyền bí với hang động và chùa chiền linh thiêng.",
        category="Di tích lịch sử",
        image_url="https://images.unsplash.com/photo-1573843981267-be1999ff37cd?w=800&q=80",
    ),
    Place(
        id=5,
        name="Bán đảo Sơn Trà",
        description="Khu bảo tồn thiên nhiên với rừng nguyên sinh, bãi biển hoang sơ và đàn voọc chà vá.",
        category="Thiên nhiên",
        image_url="https://images.unsplash.com/photo-1504893524553-b855bce32c67?w=800&q=80",
    ),
    Place(
        id=6,
        name="Đèo Hải Vân",
        description="Con đèo huyền thoại dài 21km uốn lượn giữa núi và biển, được mệnh danh là đệ nhất hùng quan.",
        category="Thiên nhiên",
        image_url="https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&q=80",
    ),
    Place(
        id=7,
        name="Suối Lương - Hòa Phú Thành",
        description="Khu sinh thái với suối nước trong mát chảy qua rừng nguyên sinh, lý tưởng để picnic và tắm suối.",
        category="Thiên nhiên",
        image_url="https://images.unsplash.com/photo-1432405972618-c60b0225b8f9?w=800&q=80",
    ),
    Place(
        id=8,
        name="Rừng nguyên sinh Sơn Trà",
        description="Tán rừng nhiệt đới xanh mướt che phủ toàn bộ bán đảo, nơi sinh sống của nhiều loài động vật quý hiếm.",
        category="Thiên nhiên",
        image_url="https://images.unsplash.com/photo-1448375240586-882707db888b?w=800&q=80",
    ),
    Place(
        id=9,
        name="Bãi biển Bắc Mỹ An",
        description="Bãi biển yên tĩnh với làn nước xanh ngọc bích, ít người hơn Mỹ Khê nhưng không kém phần đẹp.",
        category="Bãi biển",
        image_url="https://images.unsplash.com/photo-1519046904884-53103b34b206?w=800&q=80",
    ),
    Place(
        id=10,
        name="Chùa Linh Ứng Sơn Trà",
        description="Ngôi chùa với tượng Phật Quan Âm cao 67m nhìn ra biển Đông, linh thiêng và hùng vĩ.",
        category="Tâm linh",
        image_url="https://images.unsplash.com/photo-1540979388789-6cee28a1cdc9?w=800&q=80",
    ),
    Place(
        id=11,
        name="Hồ Hòa Trung",
        description="Hồ nước ngọt nằm giữa thung lũng xanh mát, bao quanh bởi đồi núi phủ rừng thông yên bình.",
        category="Thiên nhiên",
        image_url="https://images.unsplash.com/photo-1501854140801-50d01698950b?w=800&q=80",
    ),
    Place(
        id=12,
        name="Làng chài Nam Ô",
        description="Làng chài cổ hơn 700 năm tuổi với nghề làm mắm truyền thống và bãi biển đẹp.",
        category="Làng nghề",
        image_url="https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800&q=80",
    ),
]


@app.get("/")
def root():
    if random.random() < ERROR_RATE:
        return JSONResponse(status_code=500, content={"error": "injected", "version": VERSION})
    return {"message": "Da Nang Places API is running", "version": VERSION}


@app.get("/healthz")
def healthz():
    return "ok"


@app.get("/places", response_model=List[Place])
def get_places():
    return PLACES


@app.get("/places/{place_id}", response_model=Place)
def get_place(place_id: int):
    for place in PLACES:
        if place.id == place_id:
            return place
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail="Place not found")
