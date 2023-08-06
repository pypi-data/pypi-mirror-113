"""model tracking and explainability"""


import os
import base64
from alibi_detect.cd import KSDrift, LSDDDrift, MMDDrift, ChiSquareDrift

def decode_py(message):
    base64_bytes = message.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    return message_bytes.decode('ascii')

def encode_py(message):
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    return base64_bytes.decode('ascii')


# set environment variable
os.environ['MLFLOW_S3_ENDPOINT_URL'] = decode_py(
    'aHR0cDovL21sZmxvdy1taW5pby1zZXJ2aWNlLm1sZmxvdy5zdmMuY2x1c3Rlci5sb2NhbDo5MDAw'
)

os.environ['AWS_ACCESS_KEY_ID'] = decode_py(
    'bWluaW8='
)

os.environ['AWS_SECRET_ACCESS_KEY'] = decode_py(
    'QlM2UHBVS25XXkJrY0AkbCRRQXNZJHAjbA=='
)

os.environ['MLFLOW_BASE_URL'] = decode_py(
    'aHR0cDovL21sZmxvdy1zZXJ2aWNlLm1sZmxvdy5zdmMuY2x1c3Rlci5sb2NhbDo1MDAw'
)

def ksdrift(mlflow, test_data, p_val, current_time):
    with mlflow.start_run(run_name="KSDrift"):
        cd = KSDrift(test_data.values, p_val=p_val)

        mlflow.log_param('timestamp_log',str(current_time))
        
        mlflow.sklearn.log_model(cd, f"KSDrift")


def lsddrift(mlflow, test_data, p_val, current_time):
    with mlflow.start_run(run_name="LSDDDrift"):
        cd = LSDDDrift(test_data.values.astype('float32'), backend='tensorflow', p_val=p_val,)


        mlflow.log_param('timestamp_log',str(current_time))
        mlflow.sklearn.log_model(cd, f"LSDDDrift")


def mmddrift(mlflow, test_data, p_val, current_time):
    with mlflow.start_run(run_name="MMDDrift"):
        cd = MMDDrift(test_data, backend='tensorflow', p_val=p_val,)


        mlflow.log_param('timestamp_log',str(current_time))
        mlflow.sklearn.log_model(cd, f"MMDDrift")


def chisqdrift(mlflow, test_data, p_val, current_time):
    with mlflow.start_run(run_name="ChiSquareDrift"):
        cd = ChiSquareDrift(test_data.values, p_val=p_val)


        mlflow.log_param('timestamp_log',str(current_time))
        mlflow.sklearn.log_model(cd, f"ChiSquareDrift")