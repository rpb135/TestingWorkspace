function confirm() {
  var cnf = SpreadsheetApp.getActiveSheet();
  //var cnfer = SpreadsheetApp.getActiveSheet().getSheetName();
 // var cn = SpreadsheetApp.getUi();    // 얼럿 알림 시 사용 cn.alert("Hello")
  
  var c1='C', c2='H', res1=' ', res2=' ';
  var StartCell=7, endCellNum =' ', tmp=' ', cha=' ';
  
  var cellarr=[['C'],['D'],['E'],['F'],['G'],['H']];
  
  var protection, range;
  
  var protections = cnf.getProtections(SpreadsheetApp.ProtectionType.RANGE);
  
  for (var i = 0; i < protections.length; i++) {
    var protection = protections[i];
    if (protection.canEdit()) {
      protection.remove();
    }
  }
  
  // 셀 값이 비어있을때 예외 처리 필요
  // 실행 후 재 탐색 시 중복하여 생성하지 않게 하는 것 필요
  
  // def 반복 70개로 수정 필요
  for(var i=8; i<70; i++) {
    var bl=1;
    c1='C', c2='H';
    
    c1 += i.toString();   // C'n' c8
    c2 += i.toString();   // H'n' h8
    
    cnf.getRange(c1);     // c8
    
    for( t=0; t<6; t++) {
      cha = cellarr[t];
      cha += i.toString();
      Logger.log( '###########조합 : ' + cha);
      
      var rule = cnf.getRange(cha).getValue(); // 해당 셀에 값이 있는가
      
      if (rule != 0) {
      // 셀에 데이터가 있음
      //Logger.log( 'rule 데이터 : ' + rule);
      //Logger.log( '셀 데이터 : ' + c2);
      //SpreadsheetApp.getActiveSheet().getRange('a1').setValue('data');
      //res1 = c1;
        if(t < 5) {
          var tmper ='';
          tmper = i-1;
          cha = 'H';
          cha += tmper.toString();
          
          endCellNum = tmper;
        }else {
          endCellNum = i;
        }
      res2 = cha;
      } else {
        Logger.log('데이터 없음 @@');
        bl = 0;
        break;
      }
    }
    if(bl == 0) break;
  }
  Logger.log( '결과 값 endCellNum : ' + endCellNum);
  Logger.log( '결과 값 2 : ' + res2);
  
  if(res2 != 0) {
    res1 = "C8:" + res2;
    tmp = endCellNum - StartCell;
    Logger.log( '결과 : ' + res1);
    Logger.log( 'tmp 결과 : ' + tmp);
    
    range = cnf.getRange(8,3,tmp,6);
    protection = range.protect().setWarningOnly(true);
    
    //var users = Session.getEffectiveUser();
    //protection.addEditor(users);
    //Logger.log("사용자 : " + protection.getEditors());
    
    
    //Logger.log("asdfadf = " + protection.canDomainEdit().toString());
    //var me = Session.getEffectiveUser();
    //protection.addEditor('goldbug9933@gmail.com');
    //Logger.log("사용자2 : " + protection.getEditors());
    //protection.removeEditors(protection.getEditors());
    
   
    //protection.setDomainEdit(true);
    //if (protection.canDomainEdit()) {
   //   protection.setDomainEdit(true);
    //}
  }
}

//////////////////////////////////////////////////////////////////////////////
// 셀 잠금해제
function disProtect() {
  var me = Session.getEffectiveUser();
  var email = Session.getActiveUser().getEmail();
Logger.log(email);
  var cnf = SpreadsheetApp.getActiveSheet();
  var protections = cnf.getProtections(SpreadsheetApp.ProtectionType.RANGE);
  var protection;
  
  for (var i = 0; i < protections.length; i++) {
    protection = protections[i];
    protection.addEditor(me);
      protection.remove();
  }
}
//////////////////////////////////////////////////////////////////////////////
// 잠금 상관 없이 정렬
function alerts() {
  
  var sheet = SpreadsheetApp.getActiveSheet();
  var protection = sheet.protect().setDescription('셀 보호 예제');
  
  // Ensure the current user is an editor before removing others. Otherwise, if the user's edit
  // permission comes from a group, the script throws an exception upon removing the group.
  var me = Session.getEffectiveUser();
  protection.addEditor('jamzam725@gmail.com');
  protection.removeEditors(protection.getEditors());
  if (protection.canDomainEdit()) {
    protection.setDomainEdit(false);
  }
  
}
