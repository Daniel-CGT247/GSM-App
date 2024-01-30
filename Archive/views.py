# @api_view(["GET"])
# def collection_list(request):
#     queryset = YourList.objects.select_related("item").all()
#     serializer = YourListSerializer(queryset, many=True)
#     return Response(serializer.data)


# @api_view(["GET"])
# def bundle_group_list(request):
#     queryset = BundleGroup.objects.select_related("job_group").all()
#     serializer = BundleGroupSerializer(queryset, many=True)
#     return Response(serializer.data)


# @api_view(["GET"])
# def bundle_group_detail(request, pk):
#     queryset = BundleGroup.objects.select_related("job_group").get(id=pk)
#     serializer = BundleGroupSerializer(queryset, many=False)
#     return Response(serializer.data)


# @api_view(["GET", "POST"])
# def operation_lib_list(request):
#     if request.method == "GET":
#         queryset = OperationLib.objects.all()
#         serializer = OperationLibSerializer(queryset, many=True)
#         return Response(serializer.data)
#     if request.method == "POST":
#         serializer = OperationLibSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


# @api_view(["GET", "PUT", "DELETE"])
# def operation_lib_detail(request, pk):
#     operation = get_object_or_404(OperationLib, id=pk)
#     if request.method == "GET":
#         serializer = OperationLibSerializer(operation, many=False)
#         return Response(serializer.data)
#     if request.method == "PUT":
#         serializer = OperationLibSerializer(instance=operation, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
#     if request.method == "DELETE":
#         operation.delete()
#         return Response("Item deleted successfully", status=status.HTTP_204_NO_CONTENT)


# @api_view(["GET"])
# def element_lib_list(request):
#     queryset = ElementLib.objects.select_related("operation").all()
#     serializer = ElementLibSerializer(queryset, many=True)
#     return Response(serializer.data)


# @api_view(["GET"])
# def variable_list(request):
#     queryset = Variables.objects.all()
#     serializer = VariableSerializer(queryset, many=True)
#     return Response(serializer.data)
