from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import time
import replicate  # type: ignore
import openai
import os

# 🔐 환경 변수 로드
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
replicate_client = replicate.Client(api_token=os.getenv("REPLICATE_API_TOKEN"))

# 📁 폴더 설정
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 🌐 Flask 앱 초기화
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# 🏠 메인 페이지
@app.route("/")
def index():
    return render_template("index.html")

# 🎨 OpenAI 이미지 생성 API
@app.route("/generate", methods=["POST"])
def generate_image():
    data = request.get_json()
    prompt = data.get("prompt", "")
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="512x512"
        )
        image_url = response["data"][0]["url"]
        return jsonify({"image_url": image_url})
    except Exception as e:
        return jsonify({"error": str(e)})

# 🌸 지브리풍 변환 함수 (재시도 포함)
def upload_image_with_retry(image_path, retries=3, delay=5):
    for i in range(retries):
        try:
            output = replicate_client.run(
                "fofr/sdxl-ghibli:7be3d27912ab275ca1a5b0839d5d28a7b8dd6dc8fbbad86c1054550f4bc97c20",
                input={"image": open(image_path, "rb")}
            )
            return output
        except Exception as e:
            print(f"Error on attempt {i+1}: {e}")
            if i < retries - 1:
                time.sleep(delay)
            else:
                return {"error": "Max retries reached, still failed"}

# 🌸 이미지 업로드 및 지브리풍 변환 API
@app.route("/upload", methods=["POST"])
def upload_image():
    image = request.files['image']
    filename = secure_filename(image.filename)
    image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    image.save(image_path)

    try:
        result_url = upload_image_with_retry(image_path)
        if 'error' in result_url:
            return jsonify(result_url)
        return jsonify({"result_url": result_url})
    except Exception as e:
        return jsonify({"error": str(e)})

# 🖥️ 서버 실행
if __name__ == "__main__":
    app.run(debug=True)
