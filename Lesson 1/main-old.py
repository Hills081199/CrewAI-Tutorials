"""
CrewAI: Research and Write an Article
======================================
Ứng dụng sử dụng CrewAI để tạo hệ thống multi-agent tự động nghiên cứu và viết bài báo.
Gồm 3 agents: Planner (Lập kế hoạch), Writer (Viết bài), và Editor (Biên tập).
"""

# Import các thư viện cần thiết
import warnings
import os
from crewai import Agent, Task, Crew
from utils import get_openai_api_key

# Tắt các cảnh báo không cần thiết
warnings.filterwarnings('ignore')

# ================================================================================
# CẤU HÌNH OPENAI API
# ================================================================================

# Lấy OpenAI API key từ file utils
openai_api_key = get_openai_api_key()

# Cấu hình model OpenAI sẽ sử dụng
os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'


# ================================================================================
# TẠO CÁC AGENTS
# ================================================================================

# Agent 1: PLANNER (Người lập kế hoạch nội dung)
# Nhiệm vụ: Lập kế hoạch và thu thập thông tin về chủ đề
planner = Agent(
    role="Content Planner",  # Vai trò: Người lập kế hoạch nội dung
    goal="Plan engaging and factually accurate content on {topic}",  # Mục tiêu: Lập kế hoạch nội dung hấp dẫn và chính xác
    backstory="You're working on planning a blog article "
              "about the topic: {topic}."
              "You collect information that helps the "
              "audience learn something "
              "and make informed decisions. "
              "Your work is the basis for "
              "the Content Writer to write an article on this topic.",
    # Câu chuyện nền: Bạn đang lập kế hoạch cho một bài viết blog về chủ đề được chỉ định
    # Thu thập thông tin giúp độc giả học hỏi và đưa ra quyết định sáng suốt
    allow_delegation=False,  # Không cho phép ủy quyền công việc
    verbose=True  # Hiển thị chi tiết quá trình thực thi
)

# Agent 2: WRITER (Người viết nội dung)
# Nhiệm vụ: Viết bài dựa trên kế hoạch của Planner
writer = Agent(
    role="Content Writer",  # Vai trò: Người viết nội dung
    goal="Write insightful and factually accurate "
         "opinion piece about the topic: {topic}",  # Mục tiêu: Viết bài có sâu sắc và chính xác
    backstory="You're working on a writing "
              "a new opinion piece about the topic: {topic}. "
              "You base your writing on the work of "
              "the Content Planner, who provides an outline "
              "and relevant context about the topic. "
              "You follow the main objectives and "
              "direction of the outline, "
              "as provide by the Content Planner. "
              "You also provide objective and impartial insights "
              "and back them up with information "
              "provide by the Content Planner. "
              "You acknowledge in your opinion piece "
              "when your statements are opinions "
              "as opposed to objective statements.",
    # Câu chuyện nền: Bạn đang viết một bài báo dựa trên đề cương của Content Planner
    # Cung cấp góc nhìn khách quan và công bằng, phân biệt rõ ý kiến và sự thật
    allow_delegation=False,  # Không cho phép ủy quyền công việc
    verbose=True  # Hiển thị chi tiết quá trình thực thi
)

# Agent 3: EDITOR (Biên tập viên)
# Nhiệm vụ: Kiểm tra và chỉnh sửa bài viết
editor = Agent(
    role="Editor",  # Vai trò: Biên tập viên
    goal="Edit a given blog post to align with "
         "the writing style of the organization. ",  # Mục tiêu: Chỉnh sửa bài viết phù hợp phong cách tổ chức
    backstory="You are an editor who receives a blog post "
              "from the Content Writer. "
              "Your goal is to review the blog post "
              "to ensure that it follows journalistic best practices,"
              "provides balanced viewpoints "
              "when providing opinions or assertions, "
              "and also avoids major controversial topics "
              "or opinions when possible.",
    # Câu chuyện nền: Bạn là biên tập viên nhận bài từ Content Writer
    # Đảm bảo bài viết tuân thủ các nguyên tắc báo chí, cân bằng quan điểm
    # Tránh các chủ đề gây tranh cãi khi có thể
    allow_delegation=False,  # Không cho phép ủy quyền công việc
    verbose=True  # Hiển thị chi tiết quá trình thực thi
)


# ================================================================================
# TẠO CÁC TASKS (NHIỆM VỤ)
# ================================================================================

# Task 1: LẬP KẾ HOẠCH (PLAN)
# Nhiệm vụ của Planner agent
plan = Task(
    description=(
        "1. Prioritize the latest trends, key players, "
            "and noteworthy news on {topic}.\n"
        "2. Identify the target audience, considering "
            "their interests and pain points.\n"
        "3. Develop a detailed content outline including "
            "an introduction, key points, and a call to action.\n"
        "4. Include SEO keywords and relevant data or sources."
    ),
    # Mô tả nhiệm vụ:
    # 1. Ưu tiên xu hướng mới nhất, các nhân vật chủ chốt và tin tức đáng chú ý
    # 2. Xác định đối tượng mục tiêu, xem xét sở thích và vấn đề họ quan tâm
    # 3. Phát triển đề cương chi tiết bao gồm phần giới thiệu, điểm chính và lời kêu gọi hành động
    # 4. Bao gồm từ khóa SEO và dữ liệu/nguồn tham khảo có liên quan
    expected_output="A comprehensive content plan document "
        "with an outline, audience analysis, "
        "SEO keywords, and resources.",
    # Kết quả mong đợi: Tài liệu kế hoạch nội dung toàn diện với đề cương, phân tích đối tượng,
    # từ khóa SEO và tài nguyên tham khảo
    agent=planner,  # Agent thực hiện: planner
)

# Task 2: VIẾT BÀI (WRITE)
# Nhiệm vụ của Writer agent
write = Task(
    description=(
        "1. Use the content plan to craft a compelling "
            "blog post on {topic}.\n"
        "2. Incorporate SEO keywords naturally.\n"
        "3. Sections/Subtitles are properly named "
            "in an engaging manner.\n"
        "4. Ensure the post is structured with an "
            "engaging introduction, insightful body, "
            "and a summarizing conclusion.\n"
        "5. Proofread for grammatical errors and "
            "alignment with the brand's voice.\n"
    ),
    # Mô tả nhiệm vụ:
    # 1. Sử dụng kế hoạch nội dung để tạo bài viết blog hấp dẫn
    # 2. Tích hợp từ khóa SEO một cách tự nhiên
    # 3. Đặt tên các phần/tiêu đề phụ một cách hấp dẫn
    # 4. Đảm bảo bài viết có cấu trúc với phần giới thiệu hấp dẫn, nội dung sâu sắc và kết luận tóm tắt
    # 5. Kiểm tra lỗi ngữ pháp và phù hợp với giọng văn của thương hiệu
    expected_output="A well-written blog post "
        "in markdown format, ready for publication, "
        "each section should have 2 or 3 paragraphs.",
    # Kết quả mong đợi: Bài viết blog được viết tốt ở định dạng markdown,
    # sẵn sàng xuất bản, mỗi phần có 2-3 đoạn văn
    agent=writer,  # Agent thực hiện: writer
)

# Task 3: BIÊN TẬP (EDIT)
# Nhiệm vụ của Editor agent
edit = Task(
    description=("Proofread the given blog post for "
                 "grammatical errors and "
                 "alignment with the brand's voice."),
    # Mô tả nhiệm vụ: Kiểm tra bài viết blog xem có lỗi ngữ pháp không
    # và đảm bảo phù hợp với giọng văn của thương hiệu
    expected_output="A well-written blog post in markdown format, "
                    "ready for publication, "
                    "each section should have 2 or 3 paragraphs.",
    # Kết quả mong đợi: Bài viết blog hoàn chỉnh ở định dạng markdown,
    # sẵn sàng xuất bản, mỗi phần có 2-3 đoạn văn
    agent=editor  # Agent thực hiện: editor
)


# ================================================================================
# TẠO CREW (ĐỘI NHÓM)
# ================================================================================

# Tạo crew với 3 agents và 3 tasks
# Các task sẽ được thực hiện tuần tự theo thứ tự trong danh sách
crew = Crew(
    agents=[planner, writer, editor],  # Danh sách các agents
    tasks=[plan, write, edit],  # Danh sách các tasks (thực hiện tuần tự)
    verbose=2  # Hiển thị tất cả logs chi tiết của quá trình thực thi
)


# ================================================================================
# CHẠY CHƯƠNG TRÌNH
# ================================================================================

def main():
    """
    Hàm chính để chạy chương trình
    """
    # Bạn có thể thay đổi topic theo ý muốn
    topic = "Artificial Intelligence"
    
    print("=" * 80)
    print(f"BẮT ĐẦU TẠO BÀI VIẾT VỀ: {topic}")
    print("=" * 80)
    print()
    
    # Khởi chạy crew với topic được chỉ định
    result = crew.kickoff(inputs={"topic": topic})
    
    print()
    print("=" * 80)
    print("KẾT QUẢ CUỐI CÙNG")
    print("=" * 80)
    print(result)
    
    # Lưu kết quả vào file
    output_file = f"output_{topic.replace(' ', '_').lower()}.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result)
    
    print()
    print(f"Kết quả đã được lưu vào file: {output_file}")


# Chạy chương trình khi file được thực thi trực tiếp
if __name__ == "__main__":
    main()
