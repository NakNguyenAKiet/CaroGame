**Hướng dẫn cài đặt game Caro**

Cách 1: Tải từ GitHub

Bước 1:
Truy cập đường dẫn sau để đến file trên GitHub: https://github.com/NakNguyenAKiet/CaroGame.git

Bước 2:
Copy đường dẫn trên hoặc tham khảo hình dưới.

![image](https://github.com/NakNguyenAKiet/CaroGame/assets/93853392/e864f9bb-1591-4e72-9221-3ec7d1f97846)

Bước 3:
Chọn thư mục mà bạn muốn đặt game vào.

Bước 4: Trong thư mục đó bấm chuột phải, chọn open in Terminal.

Bước 5: Trong Terminal bấm lệnh sau git init

Bước 6: Tiếp theo bấm lệnh git clone và thêm đường dẫn

Cách 2:

Bước 1: Tương tự như trên

Bước 2: Chọn download file .zip

Bước 3: Tải hoàn thành, giải nén.

**Chỉnh để chơi game:**

Do game có cơ chế chơi online nên chúng ta cần thay đổi một bài thông số trong
game để có thể sử dụng hết tính năng của game.

- Vào Python và mở thư mục chứa game
  
- Mở Terminal nhấn ipconfig

- Copy địa chỉ IPv4 và thay đổi vào biến server ở file server.py và network.py
  
- Để 2 thiết bị có thể chơi online được với nhau cần thay đổi địa chỉ server
trên máy khách bằng địa chỉ server của máy chủ đang mở server và máy chủ
sẽ là người chơi trước
