# 2.145.0 (build fdf53ba) #
FROM public.ecr.aws/forensicir/getpublicip:latest AS layer
FROM public.ecr.aws/lambda/python:latest
### layer code ###
WORKDIR /opt
COPY --from=layer /opt/ .
### function code ###
WORKDIR /var/task
COPY parquet.py requirements.txt .
RUN pip --no-cache-dir install -r requirements.txt --upgrade
CMD ["parquet.handler"]