#FROM public.ecr.aws/lambda/python:3.9
#
## Copy function code
#COPY app.py ${LAMBDA_TASK_ROOT}
#
## Install the function's dependencies using file requirements.txt
## from your project folder.
#
#COPY requirements.txt  .
#RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"
#
##Install the runtime interface client
##RUN pip install awslambdaric
#
##RUN yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
##RUN yum install -y nodejs
#
##CMD [ "app.handler" ]

FROM python:3.9

# Install the function's dependencies using file requirements.txt
# from your project folder.
COPY requirements.txt  .
RUN  pip3 install -r requirements.txt 

COPY main.py .

CMD [ "python", "./main.py" ]