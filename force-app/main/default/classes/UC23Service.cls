public with sharing class UC23Service {
 public class Request { @InvocableVariable(required=true) public String operationKey; }
 public class Result { @InvocableVariable public String decision; @InvocableVariable public Id reservationId; @InvocableVariable public String errorCode; }
 @InvocableMethod(label='Reserve durable operation identity')
 public static List<Result> reserve(List<Request> requests) {
  List<UC23_Operation__c> rows=new List<UC23_Operation__c>(); List<Integer> positions=new List<Integer>();List<Result> out=new List<Result>();
  for(Integer i=0;i<requests.size();i++) { Result x=new Result();x.decision='HOLD_INVALID_KEY';out.add(x);String key=requests[i].operationKey;
   if(!String.isBlank(key)&&key.length()<=120) { rows.add(new UC23_Operation__c(Operation_Key__c=key,State__c='RESERVED_UNCERTAIN'));positions.add(i); } }
  if(!rows.isEmpty()) { Database.SaveResult[] saved=Database.insert(rows,false,AccessLevel.USER_MODE);
   for(Integer i=0;i<saved.size();i++){Result x=out[positions[i]];x.decision=saved[i].isSuccess()?'RESERVATION_CREATED_NO_EXECUTION':'HOLD_DUPLICATE_OR_DENIED'; if(saved[i].isSuccess()) x.reservationId=saved[i].getId(); else x.errorCode=String.valueOf(saved[i].getErrors()[0].getStatusCode());} }
  return out;
 }
}