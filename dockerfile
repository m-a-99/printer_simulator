FROM python:3.9
WORKDIR /app
COPY . /app
RUN pip install flask fpdf flask_socketio flask_cors python-dotenv pyjwt
CMD python3 src/app.py
