import logging
import os
import azure.functions as func
from azure.data.tables import TableServiceClient

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    
    connection_string = os.environ['AzureWebJobsStorage']    
    tableName = 'Table1'
    service_client = TableServiceClient.from_connection_string(connection_string) #connect with table storage


    try:
        # Create the table if it does not already exist
        tc = service_client.create_table_if_not_exists(tableName)
      
        # Point to the table that we want to manipulate
        tc= service_client.get_table_client(table_name=tableName) 
        
        #RandomData
        my_entity = {
            'PartitionKey': 'partionkey',
            'RowKey': 'rowkey1',
            'col1': 1,
            'col2': 'string_A',    
        }
        resp = tc.upsert_entity(entity=my_entity)
        my_entity = {
            'PartitionKey': 'partionkey',
            'RowKey': 'rowkey2',
            'col1': 2,
            'col2': 'string_B',    
        }
        resp = tc.upsert_entity(entity=my_entity)
        my_entity = {
            'PartitionKey': 'partionkey',
            'RowKey': 'rowkey3',
            'col1': 2,
            'col2': 'string_C',    
        }
        resp = tc.upsert_entity(entity=my_entity)
        #querying data
        parameters = {
        "col1":2
        }
        query_filter = "col1 eq @col1"
        res= tc.query_entities(query_filter,select=['col2'],parameters = parameters)
        result_List = []
        for entity_chosen in res:
            result_List.append(list(entity_chosen.values()))

        result_List = [item for sublist in result_List for item in sublist]

        logging.info(result_List)

        my_entity = {
            'PartitionKey': 'partionkey',
            'RowKey': 'rowkey2',
            'col1': 20,
            'col2': str(result_List),    
        }
        resp = tc.upsert_entity(entity=my_entity)
        #delete a table  (you can only delete based on partition and row key so first filter the results and then delete)
        parameters = {
        "col1":2
        }
        query_filter = "col1 eq @col1"
        res= tc.query_entities(query_filter,select=['PartitionKey','RowKey'],parameters = parameters)
 
        for entity_chosen in res:
            tc.delete_entity(partition_key=entity_chosen["PartitionKey"],row_key=entity_chosen["RowKey"])


        return func.HttpResponse(
             "completed",
             status_code=200
        )

    except Exception as e:
        logging.info(f"An exception occured {e}")
    