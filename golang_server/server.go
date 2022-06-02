package main

import (
	"context"
	"fmt"
	"log"
	"net"
	pb "proto/emp"

	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
	"google.golang.org/protobuf/types/known/emptypb"
)

const socket string = "localhost:50051"

var employeeList []*pb.Employee

type Server struct {
	pb.EmployeeManagementServer
}

func main() {
	lisn, err := net.Listen("tcp", socket)
	if err != nil {
		log.Fatalln("Errored while Listen to : ", socket, err)
	}
	log.Println("Listening at ", socket)
	s := grpc.NewServer()
	pb.RegisterEmployeeManagementServer(s, &Server{})
	err = s.Serve(lisn)
	if err != nil {
		log.Fatalln("Errored while Serving : ", socket, err)
	}
}

// Implementing all these rpc methods defined in the Proto file.
// These Methods Signatures are found in the compiled output of the Proto file.

// EmployeeManagementServer is the server API for EmployeeManagement service.
// All implementations must embed UnimplementedEmployeeManagementServer
// for forward compatibility
// type EmployeeManagementServer interface {
// 	// get the Employee details by providing the employee ID
// 	// Returns Status.NOT_FOUND if the ID doesn't match any Employee
// 	GetEmployee(context.Context, *EmployeeID) (*Employee, error)
// 	// List all the employees. It taks empty request type
// 	ListEmployees(*emptypb.Empty, EmployeeManagement_ListEmployeesServer) error
// 	// Create an emplyee by providing the Employee Details and returns the Employee ID
// 	// Returns Status.INTERNAL if the Employee is not able to create
// 	SetEmployee(context.Context, *Employee) (*EmployeeID, error)
// 	// Update an Employee by providing all the inforation again and returns empty
// 	// Returns Status.NOT_FOUND if the ID doesn't match any Employee
// 	// Returns Status.INTERNAL if the Employee is not able to update
// 	UpdateEmployee(context.Context, *Employee) (*emptypb.Empty, error)
// 	// Delete the Employee by providing the Employee ID and empty response is returned
// 	// Returns Status.NOT_FOUND if the ID doesn't match any Employee
// 	// Returns Status.INTERNAL if the Employee is not able to delete
// 	DeleteEmployee(context.Context, *EmployeeID) (*emptypb.Empty, error)
// 	mustEmbedUnimplementedEmployeeManagementServer()
// }

func (s *Server) GetEmployee(ctx context.Context, empID *pb.EmployeeID) (*pb.Employee, error) {
	log.Println("Hitted GetEmployee")
	for _, e := range employeeList {
		if e.Id == empID.Id {
			return e, nil
		}
	}
	return nil, status.Errorf(
		codes.NotFound,
		"Given employee ID is not found",
	)
}

func (s *Server) SetEmployee(ctx context.Context, emp *pb.Employee) (*pb.EmployeeID, error) {
	log.Println("Hitted SetEmployee with the emp ID", emp.Id)
	employeeList = append(employeeList, emp)
	empID := pb.EmployeeID{Id: string(emp.Id)}
	return &empID, nil

}

func (s *Server) ListEmployees(emt *emptypb.Empty, stream pb.EmployeeManagement_ListEmployeesServer) error {
	log.Println("Hitted ListEmployees")
	for _, e := range employeeList {
		stream.Send(e)
	}
	return nil
}

func (s *Server) UpdateEmployee(ctx context.Context, emp *pb.Employee) (*emptypb.Empty, error) {
	log.Println("Hitted UpdateEmployee to update the employee ID", emp.Id)
	for i, e := range employeeList {
		if e.Id == emp.Id {
			employeeList[i] = emp
			log.Println("Updated employee\n", emp)
			break
		}
	}
	return &emptypb.Empty{}, nil
}

func (s *Server) DeleteEmployee(ctx context.Context, empID *pb.EmployeeID) (*emptypb.Empty, error) {
	log.Println("Hitted DeleteEmployee to Delete the emp ", empID)
	for i, e := range employeeList {
		if e.Id == empID.Id {
			// slicing won't raise Index out of range error.
			// at this point employeeList[i+1:]  if i is the last index the i+1 return empty slice in slicing.
			// no error
			employeeList = append(employeeList[:i], employeeList[i+1:]...)
			log.Println("Deleted the Employee")
			fmt.Println(employeeList)
			break
		}
	}
	return &emptypb.Empty{}, nil
}
