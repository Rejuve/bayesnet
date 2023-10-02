ARG AWS_ACCOUNT
ARG REGION
ARG REPO
ARG STAGE
FROM ${AWS_ACCOUNT}.dkr.ecr.${REGION}.amazonaws.com/{REPO}:{STAGE}

WORKDIR /workspace
COPY . /workspace
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools
RUN apt update && apt install -y gfortran cmake build-essential
RUN pip3 install -r requirements.txt
WORKDIR /workspace/sn_service

CMD ["python3", "bayes_service.py", "--grpc-port", "7003"]
