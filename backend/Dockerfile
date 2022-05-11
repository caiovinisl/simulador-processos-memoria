
#For single Docker file use:
# docker build -t test_fastapi_image . builds the image[dont forget the dot]
# docker run -d --name fastapi_test_container -p 8000:8000 test_fastapi_image run the Container


FROM python:3.9

# for the alembic 
WORKDIR /backend

#
COPY . /backend

# 

# 
RUN pip install --no-cache-dir --upgrade -r requirements.txt


WORKDIR /backend/app

# 
COPY ./app /app

# 
CMD ["ls"]
