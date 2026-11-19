# Field Notes · kế hoạch biên tập profile

**Mục tiêu:** trong một lượt cuộn, người đọc hiểu lab làm gì, chọn được một dự án và kiểm tra được nguồn dữ liệu. Giữ cả 16 ý tưởng dưới đây, nhưng chọn vị trí theo nhu cầu: phần đầu để khám phá, phần giữa để đọc số liệu, phần cuối để tìm người hoặc cách dựng lại trang.

| # | Hạng mục đã chọn | Vị trí / nhịp thay đổi |
|---|---|---|
| 01 | Bìa đánh số theo tháng UTC | Đầu trang · tự động |
| 02 | Màu nhấn theo chuyên mục | Bìa · cùng đổi với dự án tiêu điểm |
| 03 | Danh tính tập thể và người dẫn dắt | Lời chào · biên tập |
| 04 | Giới thiệu tiếng Việt | Khối mở rộng · biên tập |
| 05 | Điều hướng ngắn | Ngay dưới lời chào |
| 06 | Bản đồ dự án theo lĩnh vực | Atlas · biên tập |
| 07 | Điểm vào mã nguồn cụ thể | Atlas · đối chiếu khi đổi cấu trúc repo |
| 08 | Dự án tiêu điểm | Lab Pulse · luân phiên theo tháng, không phải xếp hạng |
| 09 | Vòng hoạt động 30 ngày | Lab Pulse · hằng ngày |
| 10 | Phân bố ngôn ngữ dự án | Lab Pulse · hằng ngày, có chú thích ngoại lệ Zig |
| 11 | Tổng repo, sao và fork | Lab Pulse · cùng phạm vi với biểu đồ |
| 12 | Năm repo cập nhật gần nhất | Lab Pulse · hằng ngày |
| 13 | Workbench của Raven | People · biên tập từ profile công khai |
| 14 | Thẻ cá nhân sáng/tối | People · theo asset gốc của NggKhaiz |
| 15 | Nguồn và pipeline | Under the hood · thu gọn |
| 16 | Đường liên hệ và danh bạ công khai | Cuối trang · không suy đoán thành viên |

**Quy trình:** (1) đối chiếu README và đường dẫn mã nguồn; (2) chọn dự án trong `scripts/edition.py`; (3) render bìa, biểu đồ và Markdown cùng ngày UTC; (4) kiểm tra liên kết, tháng kế tiếp và khả năng chạy lặp; (5) review bằng PR trước khi xuất bản. Không đổi màu mỗi lần tải, không dùng số đóng góp cá nhân để chấm điểm nhóm.

**Bảo trì:** workflow hiện có chạy mỗi ngày. Bìa, màu nhấn và tiêu điểm chỉ đổi khi sang tháng; các số liệu đổi khi nguồn thay đổi. Khi thêm dự án vào vòng luân phiên, kiểm tra đường dẫn, nội dung và độ dài nhãn trên bìa. Mẫu bìa là `scripts/masthead.svg.in`; đừng sửa trực tiếp SVG đã sinh.
