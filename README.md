# **SẢN PHẨM KHÓA LUẬN TỐT NGHIỆP: HỖ TRỢ QUÁ TRÌNH VIẾT NỘI DUNG SEO BẰNG HỆ THỐNG ĐA TÁC NHÂN MÔ HÌNH NGÔN NGỮ LỚN**

**Author**: Đỗ Hữu Kiệt

## **1. Hướng dẫn cài đặt**

### **1.1. Requirements**

- Để chạy sản phẩm, máy tính cần cài đặt Python phiên bản **3.11.1** trở lên.

- Tải môi trường ảo trong thư mục qua câu lệnh trong Terminal/Command Prompt/Powershell

```{cmd}
py -m venv .env
```

- Sau khi cài đặt thư mục môi trường ảo, cần đảm bảo các thư viện tải về sẽ được lưu trong thư mục qua câu lệnh:

```{cmd}
.venv\Scripts\activate
```

- Tải các thư viện cần thiết được liệt kê trong file **requirements.txt**:

```{cmd}
pip install -r requirements.txt
```

Sản phẩm này có sử dụng một số dịch vụ API bên ngoài (có yêu cầu đăng ký và trả phí để sử dụng):

- **OpenAI** (Tìm hiểu thêm tại: https://help.openai.com/en/articles/4936850-where-do-i-find-my-openai-api-key)
- **Tavily** (Tìm hiểu thêm tại: https://tavily.com/)
- **Unstructured** (Tìm hiểu thêm tại: https://unstructured.io/developers)

Các khóa API cần được viết trong file ".env" theo cấu trúc:

```
OPENAI_API_KEY="..."
TAVILY_API_KEY="..."
UNSTRUCTURED_API_KEY="..."
```

### **2.2. Cấu trúc thư mục**

```
├───backend
│   ├───app
│   │   ├───auth
│   │   ├───database
│   │   └───schemas
│   └───writer_agent
│       ├───agents
│       ├───graphs
│       ├───models
│       ├───schemas
│       └───tools
├───evaluations
│   ├───Agentic
│   │   ├───gpt-4o
│   │   └───gpt-4o-mini
│   ├───Base
│   │   ├───gpt-4o
│   │   └───gpt-4o-mini
│   ├───Best
│   │   └───gpt-4o-mini
│   ├───eval_reports
│   │   ├───Agentic
│   │   │   ├───gpt-4o
│   │   │   │   ├───Topic_1
│   │   │   │   ├───Topic_2
│   │   │   │   ├───Topic_3
│   │   │   │   ├───Topic_4
│   │   │   │   └───Topic_5
│   │   │   └───gpt-4o-mini
│   │   │       ├───Topic_1
│   │   │       ├───Topic_2
│   │   │       ├───Topic_3
│   │   │       ├───Topic_4
│   │   │       └───Topic_5
│   │   ├───Base
│   │   │   ├───gpt-4o
│   │   │   │   ├───Topic_1
│   │   │   │   ├───Topic_2
│   │   │   │   ├───Topic_3
│   │   │   │   ├───Topic_4
│   │   │   │   └───Topic_5
│   │   │   └───gpt-4o-mini
│   │   │       ├───Topic_1
│   │   │       ├───Topic_2
│   │   │       ├───Topic_3
│   │   │       ├───Topic_4
│   │   │       └───Topic_5
│   │   ├───Best
│   │   │   └───gpt-4o-mini
│   │   │       ├───Topic_1
│   │   │       ├───Topic_2
│   │   │       ├───Topic_3
│   │   │       ├───Topic_4
│   │   │       └───Topic_5
│   │   └───ReAct
│   │       ├───gpt-4o
│   │       │   ├───Topic_1
│   │       │   ├───Topic_2
│   │       │   ├───Topic_3
│   │       │   ├───Topic_4
│   │       │   └───Topic_5
│   │       └───gpt-4o-mini
│   │           ├───Topic_1
│   │           ├───Topic_2
│   │           ├───Topic_3
│   │           ├───Topic_4
│   │           └───Topic_5
│   ├───GroundTruth
│   └───ReAct
│       ├───gpt-4o
│       └───gpt-4o-mini
├───evaluation_playground
├───example
├───frontend
│   └───src
│       └───app
│           ├───components
│           │   └───media
│           │       └───logo
│           ├───dashboard
│           ├───editor
│           ├───fonts
│           └───profile
└───writer_agent
    ├───agents
    ├───graphs
    ├───models
    ├───schemas
    └───tools
```

### **2.3. Chạy thử nghiệm**

Để chạy thử nghiệm sản phẩm, mở file example.ipynb trong thư mục example và làm theo các chỉ dẫn bên trong file.