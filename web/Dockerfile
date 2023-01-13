FROM python

RUN mkdir /app
COPY protobufs/ /app/protobufs/
COPY web/ /app/web/
WORKDIR /app/web/
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt
RUN python -m grpc_tools.protoc -I ../protobufs --python_out=./src/infrastructure \
           --grpc_python_out=./src/infrastructure ../protobufs/pps.proto

EXPOSE 5000
ENTRYPOINT [ "python", "main.py" ]