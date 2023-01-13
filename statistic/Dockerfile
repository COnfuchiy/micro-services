FROM python

RUN mkdir /service
COPY protobufs/ /service/protobufs/
COPY statistic/ /service/statistic/
WORKDIR /service/statistic
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt
RUN python -m grpc_tools.protoc -I ../protobufs --python_out=./grpc_api \
           --grpc_python_out=./grpc_api ../protobufs/pps.proto

EXPOSE 50051
ENTRYPOINT [ "python", "init.py" ]