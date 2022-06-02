from python_client.python_pb_files import employee_pb2 as emp_pb
from python_client.python_pb_files import employee_pb2_grpc as emp_grpc
from google.protobuf import empty_pb2
import logging
import grpc
logging.basicConfig(format='%(asctime)s:%(name)s : %(message)s', level=logging.DEBUG)
log = logging.getLogger(__name__)

socket = 'localhost:50051'
channel = grpc.insecure_channel(socket)
client = emp_grpc.EmployeeManagementStub(channel)
log.info(f"Connected to the Server : {socket}")

log.info("Calling GetEmployee")
try:
    res = client.getEmployee(emp_pb.EmployeeID(id="1"))
    log.info(res)
except grpc.RpcError as e:
    log.error(e)


log.info("Creating employee")

req_pb = emp_pb.Employee(
    id="1",
    first_name="Logesh",
    last_name="Vel",
    role="Software Engineer",
    contact=emp_pb.Contact(home_addr="Some Address", mob_num="1234", mail_id="some@domain.com")
    )
res = client.setEmployee(req_pb)
log.info(res)


log.info("Calling GetEmployee")
res = client.getEmployee(emp_pb.EmployeeID(id="1"))
log.info(res)

log.info("Calling ListEmployee")
res = client.listEmployees(empty_pb2.Empty())
for r in res:
    log.info(r)

log.info("Calling updateEmployee")
req_pb = emp_pb.Employee(
    id="1",
    first_name="Logesh",
    last_name="Vel",
    role="Software Engineer",
    contact=emp_pb.Contact(home_addr="change to Some Address", mob_num="1234", mail_id="some@domain.com")
    )
client.updateEmployee(req_pb)

log.info("Creating employee")

req_pb = emp_pb.Employee(
    id="2",
    first_name="Logesh 2",
    last_name="Vel",
    role="Software Engineer 2",
    contact=emp_pb.Contact(home_addr="Some Address 2", mob_num="1234", mail_id="some@domain.com")
    )
res = client.setEmployee(req_pb)
log.info(res)

log.info("Creating employee")

req_pb = emp_pb.Employee(
    id="3",
    first_name="Logesh 3",
    last_name="Vel",
    role="Software Engineer 3",
    contact=emp_pb.Contact(home_addr="Some Address 3", mob_num="1234", mail_id="some@domain.com")
    )
res = client.setEmployee(req_pb)
log.info(res)

log.info("Calling deleteEmployee")
client.deleteEmployee(emp_pb.EmployeeID(id="3"))

log.info("Calling ListEmployee")
res = client.listEmployees(empty_pb2.Empty())
for r in res:
    log.info(r)

