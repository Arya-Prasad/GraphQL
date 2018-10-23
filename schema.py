import graphene
import datetime
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import db_session, Department as DepartmentModel, Employee as EmployeeModel
import utils

class Department(SQLAlchemyObjectType):
    class Meta:
        model = DepartmentModel
        interfaces = (relay.Node, )


class DepartmentConnection(relay.Connection):
    class Meta:
        node = Department


class Employee(SQLAlchemyObjectType):
    class Meta:
        model = EmployeeModel
        interfaces = (relay.Node, )


class EmployeeConnections(relay.Connection):
    class Meta:
        node = Employee
 

class EmployeeFields:
    name = graphene.String(description="Name of Employee", required = True)
    #hiredOn = graphene.types.datetime.DateTime(description="Hire date")
    department_id = graphene.ID(description = "Global Id of the department of the employee", required = True)


class CreateEmployeeInput(graphene.InputObjectType, EmployeeFields):
    pass


class CreateEmployee(graphene.Mutation):
    '''Mutation to create employee'''

    employee = graphene.Field(lambda: Employee, description="Employee Created")

    class Arguments:
        input = CreateEmployeeInput(required=True)

    def mutate(self, info, input):
        data = utils.input_to_dictionary(input)
        employee = EmployeeModel(**data)
        db_session.add(employee)
        db_session.commit()

        return CreateEmployee(employee = employee)

    
class CountableConnection(graphene.relay.Connection):
    class Meta:
        abstract = True

    total_count = graphene.Int()

    @staticmethod
    def resolve_total_count(root, info, *args, **kwargs):
        return root.length

graphene.relay.connection = CountableConnection


class CustomSQLAlchemyObjectType(SQLAlchemyObjectType):

    class Meta:
        abstract = True

    @classmethod
    def __init_subclass_with_meta__(cls, model=None, registry=None, skip_registry=False,
                                    only_fields=(), exclude_fields=(), connection=None,
                                    use_connection=None, interfaces=(), id=None, **options):
        # Force it to use the countable connection
        countable_conn = connection or CountableConnection.create_type("{}CountableConnection".format(model.__name__), node=cls)

        super(CustomSQLAlchemyObjectType, cls).__init_subclass_with_meta__(
                                                                   model,
                                                                   registry,
                                                                   skip_registry,
                                                                   only_fields,
                                                                   exclude_fields, 
                                                                   countable_conn,
                                                                   use_connection, 
                                                                   interfaces, 
                                                                   id,
                                                                   **options)    


class Mutation(graphene.ObjectType):
    createEmployee = CreateEmployee.Field()

    
class Query(graphene.ObjectType):
    node = relay.Node.Field()
    # Allows sorting over multiple columns, by default over the primary key
    all_employees = SQLAlchemyConnectionField(EmployeeConnections)
    # Disable sorting over this field
    all_departments = SQLAlchemyConnectionField(DepartmentConnection, sort=None)

    employee = graphene.relay.Node.Field(Employee)

    department = graphene.relay.Node.Field(Department)


schema = graphene.Schema(query=Query, mutation=Mutation)
