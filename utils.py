from graphql_relay.node.node import from_global_id

def input_to_dictionary(input):
    '''Method to convert graphene inputs to a dictionary'''

    dict = {}
        
    for key in input:
        #convert graphQL global id to database id
        if key[-2:] == 'id':
            input[key] = from_global_id(input[key])[1]
        dict[key] = input[key]
                
    return dict
