@IsTest private class UC23ServiceTest {
 @TestSetup static void evaluatorPermissions() {
  User evaluator=new User(Alias='uc23test',LastName='UC23Evaluator',Email='uc23@example.invalid',
   Username='uc23.'+UserInfo.getOrganizationId()+'.'+Datetime.now().getTime()+'@example.invalid',
   ProfileId=UserInfo.getProfileId(),TimeZoneSidKey='America/Los_Angeles',LocaleSidKey='en_US',EmailEncodingKey='UTF-8',LanguageLocaleKey='en_US');
  insert evaluator;
  PermissionSet p=[SELECT Id FROM PermissionSet WHERE Name='UC23_Operator' LIMIT 1];
  insert new PermissionSetAssignment(AssigneeId=evaluator.Id,PermissionSetId=p.Id);
 }

 @IsTest static void emptyBatch() {
 User evaluator=[SELECT Id FROM User WHERE LastName='UC23Evaluator' LIMIT 1]; System.runAs(evaluator) {
  Test.startTest(); List<UC23Service.Result> results=UC23Service.reserve(new List<UC23Service.Request>()); Test.stopTest();
  System.assertEquals(0,results.size());
 }
 }

 @IsTest static void syntheticControl() { User evaluator=[SELECT Id FROM User WHERE LastName='UC23Evaluator' LIMIT 1]; System.runAs(evaluator) { UC23Service.Request r=new UC23Service.Request();r.operationKey='synthetic-idempotency-001';List<UC23Service.Result> first=UC23Service.reserve(new List<UC23Service.Request>{r});System.assertEquals('RESERVATION_CREATED_NO_EXECUTION',first[0].decision,first[0].errorCode == null ? 'No DML error reported' : first[0].errorCode);System.assertEquals('HOLD_DUPLICATE_OR_DENIED',UC23Service.reserve(new List<UC23Service.Request>{r})[0].decision);System.assertEquals(1,[SELECT COUNT() FROM UC23_Operation__c]); } }
}
