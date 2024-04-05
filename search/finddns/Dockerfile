# 2.134.0 (build 265d769) #
FROM public.ecr.aws/forensicir/getpublicip:latest AS layer
FROM public.ecr.aws/lambda/python:latest
### layer code ###
WORKDIR /opt
COPY --from=layer /opt/ .
### function code ###
WORKDIR /var/task
COPY finddns.py requirements.txt .
RUN pip --no-cache-dir install -r requirements.txt --upgrade
CMD ["finddns.handler"]