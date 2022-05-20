
#For single Docker file use:
# docker-compose -f docker-compose.local.yml up -d


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
