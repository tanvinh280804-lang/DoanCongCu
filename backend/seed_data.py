from app.database import SessionLocal, Base, engine
from app.models.room import Room
from app.models.user import User
from app.services.auth_service import hash_password

Base.metadata.create_all(bind=engine)
db = SessionLocal()

# Tạo admin
admin = User(
    full_name="Nhat Quang",
    email="nhatquangle1@gmail.com",
    hashed_password=hash_password("02062004"),
    is_admin=True
)
db.add(admin)

# Thêm phòng mẫ
rooms = [
    Room(name="Phong Deluxe View Bien", description="Phong rong rai voi tam nhin ra bien tuyet dep", price=850000, capacity=2, image_url="https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=800"),
    Room(name="Phong Superior Garden", description="Phong huong vuon yen tinh thich hop nghi duong", price=650000, capacity=2, image_url="https://images.unsplash.com/photo-1618773928121-c32242e63f39?w=800"),
    Room(name="Phong Family Suite", description="Phong rong danh cho gia dinh co 2 phong ngu", price=1200000, capacity=4, image_url="https://images.unsplash.com/photo-1591088398332-8a7791972843?w=800"),
    Room(name="Phong Standard", description="Phong tieu chuan thoai mai day du tien nghi", price=450000, capacity=2, image_url="https://images.unsplash.com/photo-1566665797739-1674de7a421a?w=800"),
    Room(name="Phong VIP Penthouse", description="Phong penthouse sang trong tang cao nhat view toan thanh pho", price=3500000, capacity=2, image_url="https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=800"),
    Room(name="Phong Honeymoon", description="Phong lang man danh cho cap doi trang tri hoa tuoi bon tam rieng", price=1500000, capacity=2, image_url="https://images.unsplash.com/photo-1602002418082-a4443e081dd1?w=800"),
]
for r in rooms:
    db.add(r)

db.commit()
print("Da tao du lieu mau thanh cong!")
db.close()