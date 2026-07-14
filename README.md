Homestay Manager
Cài đặt và chạy
1. Clone project
git clone https://github.com/tanvinh280804-lang/CS-434.git cd Duan_CS434\homestay-project

2. Cài thư viện
cd Duan_CS434\homestay-project\backend python -m venv venv venv\Scripts\activate pip install -r requirements.txt

3. Tạo file .env
Tạo file backend/.env với nội dung: DATABASE_URL=sqlite:///./homestay.db SECRET_KEY=homestay-super-secret-key-2024 ALGORITHM=HS256 ACCESS_TOKEN_EXPIRE_MINUTES=30 GROQ_API_KEY=your_groq_api_key APP_NAME=Homestay Manager DEBUG=True

4. Tạo dữ liệu mẫu
python seed_data.py

5. Chạy backend
uvicorn app.main:app --reload --port 8000

6. Chạy frontend
Mở file frontend/index.html bằng Live Server
