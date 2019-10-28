import addressbook_pb2

person = addressbook_pb2.Person()

person.id = 1234
person.name = "John Doe"
person.email = "jdoe@example.com"

phone = person.phones.add()
phone.number = "555-4321"
phone.type = addressbook_pb2.Person.PhoneType.HOME

serialized_person = person.SerializeToString()
print(serialized_person)

deserialized_person = addressbook_pb2.Person().FromString(serialized_person)
print(deserialized_person)

