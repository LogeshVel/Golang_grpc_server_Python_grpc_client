from python_client.python_pb_files import employee_pb2 as emp_pb
from python_client.python_pb_files import employee_pb2_grpc as emp_grpc
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2
import logging
import grpc
logging.basicConfig(format='%(asctime)s:%(name)s : %(message)s', level=logging.DEBUG)
log = logging.getLogger(__name__)

socket = 'localhost:50051'
channel = grpc.insecure_channel(socket)
client = emp_grpc.EmployeeManagementStub(channel)
log.info(f"Connected to the Server : {socket}")


def call_get_employee(emp_id : str):
    log.info(f"Calling GetEmployee with the employee id {emp_id}")
    try:
        res = client.getEmployee(emp_pb.EmployeeID(id=emp_id))
        log.info("Response")
        log.info(res)
    except grpc.RpcError as e:
        log.error(f"Errored while getting the employee of ID {emp_id}")
        log.error(e)


def call_create_employee(emp_id: str, first_name: str, last_name: str, role: str, home_addrs: str, mob_numbr: str, mailid : str):
    log.info(f"Creating employee with the employee id {emp_id}")

    req_pb = emp_pb.Employee(
        id=emp_id,
        first_name=first_name,
        last_name=last_name,
        role=role,
        contact=emp_pb.Contact(home_addr=home_addrs, mob_num=mob_numbr, mail_id=mailid)
        )
    try:
        res = client.setEmployee(req_pb)
        log.info(f"Successfully created the Employee with the ID {res.id}")
    except grpc.RpcError as e:
        log.error(f"Errored while creating the employye of ID {emp_id}")
        log.error(e)

def call_list_employee():
    log.info("Calling ListEmployee")
    res = client.listEmployees(empty_pb2.Empty())
    log.info("ListEmployee Results")
    for r in res:
        log.info(r)


def call_update_employee(emp_id: str, first_name: str, last_name: str, role: str, home_addrs: str, mob_numbr: str, mailid : str):
    log.info(f"Calling updateEmployee with the employee id {emp_id}")
    req_pb = emp_pb.Employee(
        id=emp_id,
        first_name=first_name,
        last_name=last_name,
        role=role,
        contact=emp_pb.Contact(home_addr=home_addrs, mob_num=mob_numbr, mail_id=mailid)
        )
    try:
        client.updateEmployee(req_pb)
        log.info("Successfully updated")
    except grpc.RpcError as e:
        log.error(f"Errored while updating the employee of ID {emp_id}")
        log.error(e)

def call_delete_employee(emp_id: str):
    log.info(f"Calling deleteEmployee with the employee id {emp_id}")
    try:
        client.deleteEmployee(emp_pb.EmployeeID(id=emp_id))
        log.info(f"Successfully deleted the employee of id {emp_id}")
    except grpc.RpcError as e:
        log.error(f"Errored while deleting the employee of ID {emp_id}")
        log.error(e)

def call_partial_update_employee(request_pb, mask_path_list: list):
    log.info(f"Calling partialUpdate with the employee id {request_pb.id}")
    log.info(f"Request message {request_pb}")
    log.info(f"Fieldmask Paths list {mask_path_list}")
    mask = field_mask_pb2.FieldMask(paths=mask_path_list)
    # tells which fields to be updated from the given request payload
    try:
        client.partialUpdate(emp_pb.UpdateEmpRequest(emp=request_pb,update_mask=mask))
        log.info("Successfully done partial update")
    except grpc.RpcError as e:
        log.error(f"Errored while partial updating the employee of ID")
        log.error(e)

# should return error
call_get_employee("1")

# success create
call_create_employee(emp_id="1",first_name="Logesh",last_name="Vel",role="ASE",home_addrs="Some addr",mob_numbr="123456",mailid="some@domain.com")

# success get
call_get_employee("1")

# success create
call_create_employee(emp_id="2",first_name="log",last_name="esh",role="SSE",home_addrs="address",mob_numbr="98765",mailid="sse@domain.com")

# success list
call_list_employee()

# should error. the emp id is already present
call_create_employee(emp_id="2",first_name="log",last_name="esh",role="SSE",home_addrs="address",mob_numbr="98765",mailid="sse@domain.com")

# success update
call_update_employee(emp_id="2",first_name="log",last_name="esh",role="updated role Engineer",home_addrs="address",mob_numbr="98765",mailid="sse@domain.com")

# success list
call_list_employee()

# success delete
call_delete_employee(emp_id="2")

# should error in update. the emp id is deleted so can't update
call_update_employee(emp_id="2",first_name="log",last_name="esh",role="updated role Engineer",home_addrs="address",mob_numbr="98765",mailid="sse@domain.com")

# should error delete. since the emp is already deleted
call_delete_employee(emp_id="2")

# sample fields
# emp_pb.Employee(
#         id="1",
#         first_name="first_name",
#         last_name=last_name,
#         role=role,
#         contact=emp_pb.Contact(home_addr=home_addrs, mob_num=mob_numbr, mail_id=mailid)
#         )

call_get_employee("1")

log.info("\nWorking with Partial updates\n")

p_req_pb = emp_pb.Employee(
        id="1",
        first_name="partial update first_name",
        )

mask_list = ["emp.first_name",] # updates only the first_name
call_partial_update_employee(p_req_pb, mask_list)

call_get_employee("1")

p_req_pb = emp_pb.Employee(
        id="1",
        contact=emp_pb.Contact(home_addr="through partialupdate")
        )

mask_list = ["emp.contact.home_addr",] # updates only the home_addr
call_partial_update_employee(p_req_pb, mask_list)

call_get_employee("1")

# calling partialUpdate with the request message and paths
# where the paths gives the fields to update that doesn't exists in the request msg
# Ex: I tried to update the mob_num field, I have provided that in the request message but
# in the path field I have specified the mob_num field but accidently specified the home_addr field
# What will happen is the home_addr field is set to the zero value of its type 
# as we specified to change the home_addr in path but we haven't given that field in the request msg.
# We can neglect this type of accidental updates by implementing the server in the protper way.
# Like making the client to check whether the field specified in the path list is present in the request msg before updating
p_req_pb = emp_pb.Employee(
        id="1",
        contact=emp_pb.Contact(mob_num="mob number update")
        )

mask_list = ["emp.contact.home_addr",] # updates only the home_addr
call_partial_update_employee(p_req_pb, mask_list)

call_get_employee("1")
