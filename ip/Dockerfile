# 2.133.0 (build dcc1e75) # DEV
FROM public.ecr.aws/forensicir/getpublicip:latest AS layer
FROM public.ecr.aws/lambda/python:latest
### layer code ###
WORKDIR /opt
COPY --from=layer /opt/ .
### function code ###
WORKDIR /var/task
COPY ip.py requirements.txt .
RUN pip --no-cache-dir install -r requirements.txt --upgrade
CMD ["ip.handler"]