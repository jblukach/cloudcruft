# 2.136.0 (build 94fd33b) #
FROM public.ecr.aws/forensicir/getpublicip:latest AS layer
FROM public.ecr.aws/lambda/python:latest
### layer code ###
WORKDIR /opt
COPY --from=layer /opt/ .
### function code ###
WORKDIR /var/task
COPY dns.py requirements.txt .
RUN pip --no-cache-dir install -r requirements.txt --upgrade
CMD ["dns.handler"]