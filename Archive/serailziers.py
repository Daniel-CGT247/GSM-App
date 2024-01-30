    # def get_last_update(self, your_list):
    #     operation_last_update = your_list.operationlistitem_set.aggregate(
    #         last_update=Max("last_update")
    #     )["last_update"]

    #     if operation_last_update is None and your_list.last_update is None:
    #         return None
    #     elif your_list.last_update is None:
    #         return self.format_timestamp(operation_last_update)
    #     elif operation_last_update is None:
    #         return self.format_timestamp(your_list.last_update)
    #     else:
    #         return self.format_timestamp(
    #             max(operation_last_update, your_list.last_update)
    #         )
    
    
        # element_last_update = operation_list.elementlistitem_set.aggregate(
        #     last_update=Max("last_update")
        # )["last_update"]
        # if element_last_update is None and operation_list.last_update is None:
        #     return None
        # elif operation_list.last_update is None:
        #     return element_last_update
        # elif element_last_update is None:
        #     return operation_list.last_update
        # else:
        #     return max(element_last_update, operation_list.last_update)

