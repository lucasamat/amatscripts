import Webcom.Configurator.Scripting.Test.TestProduct
#GDLIST = Quote.GetGeneratedDocumentList('AMAT Quote')
GDLIST = Quote.GetGeneratedDocumentList('AMAT_SUBTOTAL_OFFERING')
get_delivery_parts = Quote.GetCustomField('ITEM_DELIVERY_SCHEDULE').Content
get_bill_matrix = Quote.GetCustomField('Billing_Matrix').Content
gets_delivery_parts_z0110 = Quote.GetCustomField('PARTS_DELIVERY_SCHEDULE').Content

if get_delivery_parts == "YES":
	GDLIST = Quote.GetGeneratedDocumentList('AMAT_FPM_QUOTE')
elif gets_delivery_parts_z0110 == "YES":
	GDLIST = Quote.GetGeneratedDocumentList('Amat FPM Z0110')
elif get_bill_matrix == "YES":
	GDLIST = Quote.GetGeneratedDocumentList('AMAT Total Quote')
else:
	GDLIST = Quote.GetGeneratedDocumentList('AMAT_SUBTOTAL_OFFERING')

for gndc in GDLIST:
	docid = gndc.Id
	if docid:
		fileContent = Quote.GetLatestGeneratedDocumentInBytes()
		fileName = Quote.GetLatestGeneratedDocumentFileName()

		responseJson = {"ErrorMsg":None, "File":fileContent, "FileName":fileName}

		ApiResponse = ApiResponseFactory.JsonResponse(responseJson)