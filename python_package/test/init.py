from os import path
test_data = path.dirname(__file__)+'/../test_data'
ezScrum_test_data = path.dirname(__file__)+'/../ezSrum_test_data'
def get_instance_from_testData(instanceName, table):
    return next((instance for instance in table if instance.name == instanceName),None)