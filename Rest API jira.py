import requests, json
import requests
import time

from datetime import datetime, timedelta
from bs4 import BeautifulSoup as bs

class ZetVocManager:

    headers = {
        'Accept'            : '*/*',
        'Accept-Encoding'   : 'gzip, deflate, br',
        'Accept-Language'   : 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Authorization'     : 'Bearer aiosydfoashdfalksjhdfoayusodfulasjdhfl',
        'Connection'        : 'keep-alive',
        'Content-Length'    : '71',
        'Content-type'      : 'application/json',
        'Host'              : 'devfms.zetmobility.com',
        'Origin'            : 'https://주소',
        'Referer'           : 'https://주소',
        'Sec-Fetch-Dest'    : 'empty',
        'Sec-Fetch-Mode'    : 'cors',
        'Sec-Fetch-Site'    : 'same-site',
        'User-Agent'        : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    }

    # ZET Operator Web (dev | admin) Account info
    Payload = {
        'email'     : '계정정보',
        'password'  : '비밀번호',
        'token'     : '토큰'
    }
    # 마지막 이슈 데이터 정보
    file_path = "./Automation/issueData.json"
    issueData_json = {}
    Qusetions_Num = 0
    TypeNum = 0

    #사용자 문의 게시판 정보
    User_board_data = {
        'board_id': 0,             # zetID
        'createNum': "",           # 생성된 지라 번호
        'jira_content': "",        # 내용
        'jira_title': "",          # 제목
        'jira_qtype': "",          # 문의 타입
        'jira_phone': ""          # 전화번호
    }
    #관리자 문의 게시판 정보
    Admin_User_board_data = {
        'board_id': 0,             # zetID
        'createNum': "",           # 생성된 지라 번호
        'jira_content': "",        # 내용
        'jira_title': "",          # 제목
        'jira_qtype': "",          # 문의 타입
        'jira_phone': ""          # 전화번호
    }

    # 이미지 정보
    Img_Url = {
        'img_url1': "",            # 이미지 주소
        'img_url2': "",            # 이미지 주소
        'img_url3': "",            # 이미지 주소
        'img_url4': "",            # 이미지 주소
        'img_url5': "",            # 이미지 주소
        'img_url6': ""             # 이미지 주소
    }

    with open(file_path, "r") as json_file:
        issueData_json = json.load(json_file)

    # 고객 문의 게시판
    def ZET_User_BoardSearch(self):

        #print("ZET ID >>> ",self.issueData_json['zetID'])
        #print("JIRA ID >>> ",self.issueData_json['jiraID'])
        
        with requests.Session() as s:

            # 게시판 페이지 넘버
            Board_pageNum = 0
            # 게시판 사이즈 넘버
            Board_sizeNum = 50

            # 고객 문의 게시판 URL (dev .ver)
            #board_list_url = 'URL 주소'+ str(Board_pageNum) + '&size='+ str(Board_sizeNum) +'&recieve=true&complete=true'
            # 고객 문의 게시판 URL (admin .ver)
            board_list_url = 'URL 주소'+ str(Board_pageNum) + '&size='+ str(Board_sizeNum) +'&recieve=true&complete=true'
            
            #print(board_list_url)

            # ZET Operator Web Response JSON data
            borad_list = s.get(board_list_url)
            board_json = json.loads(borad_list.text)

            # 게시판에 글이 없을 때
            if board_json['data']['content'] == []:
                print("문의 내용이 없습니다.")
                return 0
            
            # 저장 된 seq_Num 불러오고 확인하기 ######################################################
            if self.issueData_json['zetID'] == board_json['data']['content'][0]['id']:
                print("[User] JIRA에 등록된 문의사항 입니다.")
            else:
                print("값 1 >> ", board_json['data']['content'][0]['id'])
                print("값 2 >> ", self.issueData_json['zetID'])
                self.Qusetions_Num = board_json['data']['content'][0]['id'] - self.issueData_json['zetID'] -1
                print("JIRA에 등록 중입니다. >> ", self.Qusetions_Num)
            # 저장 된 seq_Num 불러오고 확인하기 ######################################################

            # 게시판에 글이 있을 때
            #elif self.seq_Num == board_json['data']['content'][Qusetions_Num]['id']:
            #    print("해당 내용은 이미 JIRA에 등록된 내용입니다.")

            #elif self.seq_Num != board_json['data']['content'][Qusetions_Num]['id']:
                #print("해당 내용 JIRA 이슈 등록 중")
                self.User_board_data['board_id'] = board_json['data']['content'][self.Qusetions_Num]['id']
                #board_time = board_json['data']['content'][Qusetions_Num]['createdTime']            # 문의 등록 날짜
                self.User_board_data['jira_content'] = board_json['data']['content'][self.Qusetions_Num]['content']              # 내용
                self.User_board_data['jira_title'] = board_json['data']['content'][self.Qusetions_Num]['title']                  # 제목
                self.User_board_data['jira_qtype'] = board_json['data']['content'][self.Qusetions_Num]['questionType']           # 고객 문의 타입
                self.User_board_data['jira_phone'] = board_json['data']['content'][self.Qusetions_Num]['user']['phoneNumber']    # 전화번호 phoneNumber
                self.Img_Url['img_url1'] = board_json['data']['content'][self.Qusetions_Num]['image1']
                self.Img_Url['img_url2'] = board_json['data']['content'][self.Qusetions_Num]['image2']
                self.Img_Url['img_url3'] = board_json['data']['content'][self.Qusetions_Num]['image3']
                self.Img_Url['img_url4'] = board_json['data']['content'][self.Qusetions_Num]['image4']
                self.Img_Url['img_url5'] = board_json['data']['content'][self.Qusetions_Num]['image5']
                self.Img_Url['img_url6'] = board_json['data']['content'][self.Qusetions_Num]['image6']

                print("이슈 제목 >> ",self.User_board_data['jira_title'])

                if self.User_board_data['jira_qtype'] == 'APP': 
                    self.User_board_data['jira_qtype'] = '앱 사용 문의'
                elif self.User_board_data['jira_qtype'] == 'PAY':
                    self.User_board_data['jira_qtype'] = '요금/결제 관련 문의'
                elif self.User_board_data['jira_qtype'] == 'ETC':
                    self.User_board_data['jira_qtype'] = '기타'
                elif self.User_board_data['jira_qtype'] == 'MOBILITY':
                    self.User_board_data['jira_qtype'] = '기기 이용 문의'
                elif self.User_board_data['jira_qtype'] == 'EVENT':
                    self.User_board_data['jira_qtype'] = '이벤트 관련 문의'
            
                self.JIRA_User_Issue_Create()
                self.JIRA_Issue_IMG_Uproad(self.Img_Url, self.User_board_data['createNum'])
                self.JIRA_Issue_Search()       # 이슈 검색 과 Slack 메시지 전송은 같이 이루어 짐

    # JIRA Issue Create 
    def JIRA_User_Issue_Create(self):

        jira_url = 'https://jira 주소'
        auth = ('jira계정', 'jira 토큰')
        ## jira API token : jira 토큰
        headers = {
            'Content-Type': 'application/json'
        }
        
        jira_summary = "[사용자]["+self.User_board_data['jira_qtype']+"]"+self.User_board_data['jira_title']
        jira_description = self.User_board_data['jira_content']

        newIssue = json.dumps({
            "fields": {
                "project":
                {
                    "key": "UUMQ"                       ##이슈 key 값
                    #"key": "VOC"
                },
                "summary": jira_summary,                ## 이슈 제목
                #"environment": "",
                "description": jira_description,        ## 이슈 내용
                "issuetype": {
                    "id": "10009" #10006 #10009 ID값 별 타입
                },
                "customfield_10034": self.User_board_data['jira_qtype'],        #사용자 설정
                "customfield_10031": self.User_board_data['jira_phone'],        #사용자 전화번호
                "labels": [                                                     #레이블
                    "사용자"
                ]
                # "reporter": { "id": "5eec032eb04ccf0aae7a5ac9" }, # 보고자
                # "assignee": { "id": "5eec032eb04ccf0aae7a5ac9" }, # 담당자
            }
        })

        response = requests.post(jira_url,  headers=headers,  data=newIssue,  auth=auth )
        
        ## 요청 결과
        print("[User] 이슈 생성 요청 결과 : " + response.text)

        # 생성된 이슈 번호
        # return json.loads(response.text)['key']
        self.User_board_data['createNum'] = json.loads(response.text)['key']
    
    # 지라 이슈 이미지 등록
    def JIRA_Issue_IMG_Uproad(self, img_url, issueNum):
        print("이미지 등록 >> ")
        self.ZET_User_BoardSearch
        # print(img_url['img_url1'])

        for idx, (key, elem) in enumerate(img_url.items()):
            if elem is None or elem == "":
                print("No img")
                continue
            else:
                res = requests.get(elem)
                files = {'file': res.content}

                jira_url = 'https:/jira 주소/' + issueNum + '/attachments'
                auth = ('jira 계정', 'jira 토큰')
                headers = {
                    "X-Atlassian-Token": "nocheck"
                }
                
                res = requests.post(jira_url,  headers=headers,  files=files,  auth=auth )

    # JIRA Issue Search
    def JIRA_Issue_Search(self):
        print("이슈 검색 >>")
        jira_url = 'https://jira 주소'
        auth = ('jira 계정', 'jira 토큰')
        ## jira API token : jira 토큰
        headers = {
            'Content-Type': 'application/json'
        }
        
        #print("ZET ID 2 >> ", self.issueData_json['zetID'])
        #print("jira ID 2 >> ", self.issueData_json['jiraID'])

        #전송 될 이슈 정보
        send_issueData = {
            'jira_priority': '',       #이슈 중요도
            'jira_issueNum': '',       #이슈 번호
            'jira_summary': '',        #이슈 제목
            'jira_status': '',         #이슈 상태
            'jira_assignee': ''        #이슈 담당자
        }

        # 1분 기준 : 1w > 1m (변경되어야 함)
        #jira_SQL = 'created >= -120m AND reporter in (5eec032eb04ccf0aae7a5ac9, 5eeb25c541f7000abb219dfb, 5eeb25c6e145af0ab497a98f, 5eeb259bdefde70abc753f18)'
        #jira_SQL = 'project = UUMQ AND created >= -1d order by created DESC'
        jira_SQL = 'created >= -1d order by created DESC'
        jql_data = json.dumps({
            "jql": jira_SQL,
            "startAt": 0,
            "maxResults": 5,
            "fields": [
                "summary",    # 이슈 제목
                "status",     # 이슈 상태
                "priority",   # 이슈 중요도
                "assignee"    # 이슈 담당자
            ]
        })

        #issueTmpNum = 0
        response = requests.post(jira_url, headers=headers, data=jql_data, auth=auth)
        jira_res_search_json = json.loads(response.text)

        #print(jira_res_search_json)

        if jira_res_search_json['issues'] == []:
            print("No search results found")
            #time.sleep(60)

        elif self.User_board_data['createNum'] == jira_res_search_json['issues'][0]['key']:
            ## 반복 문 >> 메시지 보냄 | 반복문 >> 필터 후 메시지 보냄
                
            send_issueData['jira_priority'] = jira_res_search_json['issues'][0]['fields']['priority']['name']   #이슈 중요도
            send_issueData['jira_issueNum'] = jira_res_search_json['issues'][0]['key']                          #이슈 번호
            send_issueData['jira_summary'] = jira_res_search_json['issues'][0]['fields']['summary']             #이슈 제목
            send_issueData['jira_status'] = jira_res_search_json['issues'][0]['fields']['status']               #이슈 상태
            #print("검색 결과 이슈 번호 >> ", jira_res_search_json['issues'][0]['key'])

            if jira_res_search_json['issues'][0]['fields']['assignee'] is None or jira_res_search_json['issues'][0]['fields']['assignee'] == "":
                print("담당자 없음")
            else:
                send_issueData['jira_assignee'] = jira_res_search_json['issues'][0]['fields']['assignee']['accountId']  #담당자 계정 ID

            self.JIRA_SendTo_Slack(send_issueData)

            print("값 3 >> ", self.User_board_data['board_id'])

            with open(self.file_path, "w") as json_file:
                self.issueData_json['zetID'] += 1#self.User_board_data['board_id']
                self.issueData_json['jiraID'] = self.User_board_data['createNum']
                json.dump(self.issueData_json, json_file, indent=4)
                #print("After ZET ID >>> ",self.issueData_json['zetID'])
            
            #jira_priority = jira_res_search_json['issues'][5]['fields']['priority']['name']      #이슈 중요도
            #jira_issueNum = jira_res_search_json['issues'][5]['key']                             #이슈 번호
            #jira_summary = jira_res_search_json['issues'][5]['fields']['summary']                #이슈 제목
            #jira_assignee = jira_res_search_json['issues'][5]['fields']['assignee']['accountId'] #담당자 계정 id
            #print(jira_assignee)
            #print(jira_summary)
            #print(jira_issueNum)
            #print(jira_priority)
            #time.sleep(20)

    # JIRA Issue Message Push
    def JIRA_SendTo_Slack(self, send_issueData):
        print("슬랙메시지 보내기 >> ")
        #JIRA Users Account Info
        ################################################################################
        account_url = 'https://jira 주소'
        auth = ('jira 계정', 'jira 토큰')
        ## jira API token : jira 토큰
        headers = {
            'Content-Type': 'application/json'
        }
        query = {
            'accountId': send_issueData['jira_assignee']
        }
        res = requests.get(account_url, headers=headers, params=query, auth=auth)
        account_json = json.loads(res.text)

        print(account_json)

        if send_issueData['jira_assignee'] == "":
            print("담당자이름 없음")
            send_issueData['jira_assignee'] = "임시 담당자"
        else:
            print(account_json['publicName'])   #담당자 이름
            send_issueData['jira_assignee'] = account_json['publicName']
        ################################################################################

        slack_webhook_url = "https://hooks.slack.com/services/슬랙 훅 키"  #wisestone test
        #slack_webhook_url = "https://hooks.slack.com/services/슬랙 훅 키" #Zet devops test

        payload = {
            "channel": "testapi", # wisestone test = testapi / Zet devops test = jira_test
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "* 이슈 번호 : <https://jira주소"+ send_issueData['jira_issueNum'] + "|[" + send_issueData['jira_issueNum'] +"]>* \n *우선 순위 : " + send_issueData['jira_priority'] + "* \n *담당자 : " + send_issueData['jira_assignee'] + "*"
                    }
                },
                {
                    "type": "section",
                    "block_id": "issueMessages",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*이슈 제목 : <https://jira주소/"+ send_issueData['jira_issueNum'] +"|" + send_issueData['jira_summary'] +">*"
                    },
                },
            ]
        }
        requests.post(slack_webhook_url, data=json.dumps(payload), headers=headers)

######################################################################################################################################################################
######################################################################################################################################################################
######################################################################################################################################################################
######################################################################################################################################################################
######################################################################################################################################################################

    def ZET_Admin_BoardSearch(self):
        with requests.Session() as s:
            # 게시판 페이지 넘버
            Board_pageNum = 0
            # 게시판 사이즈 넘버
            Board_sizeNum = 50

            # 관리자 문의 게시판 URL (dev .ver)
            #Admin_board_list_url = 'https://url 주소='+ str(Board_pageNum) + '&size='+ str(Board_sizeNum) +'&recieve=true&complete=true'
            # 관리자 문의 게시판 URL (admin .ver)
            Admin_board_list_url = 'https://url 주소='+ str(Board_pageNum) + '&size='+ str(Board_sizeNum) +'&recieve=true&complete=true'

            # ZET Operator Web Response JSON data
            Admin_borad_list = s.get(Admin_board_list_url)
            Admin_board_json = json.loads(Admin_borad_list.text)
            try:
                if self.issueData_json['AdminZID'] == Admin_board_json['data']['content'][0]['id']:
                    print("[Admin] JIRA에 등록된 문의사항 입니다.")
                else:
                    print("값 1 >> ", Admin_board_json['data']['content'][0]['id'])
                    print("값 2 >> ", self.issueData_json['AdminZID'])
                    self.TypeNum = Admin_board_json['data']['content'][0]['id'] - self.issueData_json['AdminZID']

                    self.Admin_User_board_data['board_id'] = Admin_board_json['data']['content'][self.TypeNum]['id']
                    #board_time = board_json['data']['content'][Qusetions_Num]['createdTime']            # 문의 등록 날짜
                    self.Admin_User_board_data['jira_content'] = Admin_board_json['data']['content'][self.TypeNum]['content']              # 내용
                    self.Admin_User_board_data['jira_title'] = Admin_board_json['data']['content'][self.TypeNum]['title']                  # 제목
                    self.Admin_User_board_data['jira_qtype'] = Admin_board_json['data']['content'][self.TypeNum]['type']                   # 문의 타입
                    self.Img_Url['img_url1'] = Admin_board_json['data']['content'][self.TypeNum]['image1']
                    self.Img_Url['img_url2'] = Admin_board_json['data']['content'][self.TypeNum]['image2']
                    self.Img_Url['img_url3'] = Admin_board_json['data']['content'][self.TypeNum]['image3']
                    self.Img_Url['img_url4'] = Admin_board_json['data']['content'][self.TypeNum]['image4']
                    self.Img_Url['img_url5'] = Admin_board_json['data']['content'][self.TypeNum]['image5']
                    self.Img_Url['img_url6'] = Admin_board_json['data']['content'][self.TypeNum]['image6']
                    print("[Admin] JIRA에 등록 중입니다. >> ", self.TypeNum)

                    if self.Admin_User_board_data['jira_qtype'] == 'APP': 
                        self.Admin_User_board_data['jira_qtype'] = '앱 사용 문의'
                    elif self.Admin_User_board_data['jira_qtype'] == 'FMS':
                        self.Admin_User_board_data['jira_qtype'] = '관제 서버 문의'
                    elif self.Admin_User_board_data['jira_qtype'] == 'HARDWARE':
                        self.Admin_User_board_data['jira_qtype'] = '기기(HW) 문의'
                    elif self.Admin_User_board_data['jira_qtype'] == 'COMM':
                        self.Admin_User_board_data['jira_qtype'] = '통신 장애 문의'
                    elif self.Admin_User_board_data['jira_qtype'] == 'ETC':
                        self.Admin_User_board_data['jira_qtype'] = '기타'
                    #print("존재 하지 않는 번호 입니다.")
                    self.Admin_JIRA_Issue_Create()
                    #self.JIRA_Issue_IMG_Uproad(self.Img_Url, self.Admin_User_board_data['createNum'])
                    self.Admin_Issue_Search()       # 이슈 검색 과 Slack 메시지 전송은 같이 이루어 짐

            except IndexError:
                #print("에러 발생 시 에만 동작")
                with open(self.file_path, "w") as json_file:
                    self.issueData_json['AdminZID'] += 1
                    #self.issueData_json['AdminJID'] = self.Admin_User_board_data['createNum']
                    json.dump(self.issueData_json, json_file, indent=4)


    def Admin_JIRA_Issue_Create(self):
        jira_url = 'https://jira 주소'
        auth = ('jira 계정', 'jira 토큰')
        ## jira API token : jira 토큰
        headers = {
            'Content-Type': 'application/json'
        }
        
        jira_summary = "[관리자]["+self.Admin_User_board_data['jira_qtype']+"]"+self.Admin_User_board_data['jira_title']
        jira_description = self.Admin_User_board_data['jira_content']

        newIssue = json.dumps({
            "fields": {
                "project":
                {
                    "key": "UUMQ"                       ##이슈 key 값
                    #"key": "VOC"
                },
                "summary": jira_summary,                ## 이슈 제목
                #"environment": "",
                "description": jira_description,        ## 이슈 내용
                "issuetype": {
                    "id": "10009" #10006 #10009 
                },
                # "reporter": { "id": "5eec032eb04ccf0aae7a5ac9" }, # 보고자
                # "assignee": { "id": "5eec032eb04ccf0aae7a5ac9" }, # 담당자
            }
        })

        response = requests.post(jira_url,  headers=headers,  data=newIssue,  auth=auth )
        
        ## 요청 결과
        #print("[Admin] 이슈 생성 요청 결과 : " + response.text)

        # 생성된 이슈 번호
        # return json.loads(response.text)['key']

        self.Admin_User_board_data['createNum'] = json.loads(response.text)['key']
        print("관리자 게시판 이슈 등록")

    def Admin_Issue_Search(self):
        print("관리자 이슈 검색")
        jira_url = 'https://jira 주소'
        auth = ('jira 계정', 'jira 토큰')
        ## jira API token : jira 토큰
        headers = {
            'Content-Type': 'application/json'
        }
        
        #전송 될 이슈 정보
        send_issueData = {
            'jira_priority': '',       #이슈 중요도
            'jira_issueNum': '',       #이슈 번호
            'jira_summary': '',        #이슈 제목
            'jira_status': '',         #이슈 상태
            'jira_assignee': ''        #이슈 담당자
        }

        # 1분 기준 : 1w > 1m (변경되어야 함)
        #jira_SQL = 'created >= -120m AND reporter in (5eec032eb04ccf0aae7a5ac9, 5eeb25c541f7000abb219dfb, 5eeb25c6e145af0ab497a98f, 5eeb259bdefde70abc753f18)'
        #jira_SQL = 'project = UUMQ AND created >= -1d order by created DESC'
        jira_SQL = 'created >= -1d order by created DESC'
        jql_data = json.dumps({
            "jql": jira_SQL,
            "startAt": 0,
            "maxResults": 5,
            "fields": [
                "summary",    # 이슈 제목
                "status",     # 이슈 상태
                "priority",   # 이슈 중요도
                "assignee"    # 이슈 담당자
            ]
        })

        #issueTmpNum = 0
        response = requests.post(jira_url, headers=headers, data=jql_data, auth=auth)
        jira_res_search_json = json.loads(response.text)

        #print(jira_res_search_json)

        if jira_res_search_json['issues'] == []:
            print("No search results found")
            #time.sleep(60)

        elif self.Admin_User_board_data['createNum'] == jira_res_search_json['issues'][0]['key']:
            ## 반복 문 >> 메시지 보냄 | 반복문 >> 필터 후 메시지 보냄
                
            send_issueData['jira_priority'] = jira_res_search_json['issues'][0]['fields']['priority']['name']   #이슈 중요도
            send_issueData['jira_issueNum'] = jira_res_search_json['issues'][0]['key']                          #이슈 번호
            send_issueData['jira_summary'] = jira_res_search_json['issues'][0]['fields']['summary']             #이슈 제목
            send_issueData['jira_status'] = jira_res_search_json['issues'][0]['fields']['status']               #이슈 상태
            #print("검색 결과 이슈 번호 >> ", jira_res_search_json['issues'][0]['key'])

            if jira_res_search_json['issues'][0]['fields']['assignee'] is None or jira_res_search_json['issues'][0]['fields']['assignee'] == "":
                print("담당자 없음")
            else:
                send_issueData['jira_assignee'] = jira_res_search_json['issues'][0]['fields']['assignee']['accountId']  #담당자 계정 ID

            self.JIRA_SendTo_Slack(send_issueData)

            print("값 3 >> ", self.Admin_User_board_data['board_id'])

            with open(self.file_path, "w") as json_file:
                self.issueData_json['AdminZID'] += 1
                self.issueData_json['AdminJID'] = self.Admin_User_board_data['createNum']
                json.dump(self.issueData_json, json_file, indent=4)
            
            #jira_priority = jira_res_search_json['issues'][5]['fields']['priority']['name']      #이슈 중요도
            #jira_issueNum = jira_res_search_json['issues'][5]['key']                             #이슈 번호
            #jira_summary = jira_res_search_json['issues'][5]['fields']['summary']                #이슈 제목
            #jira_assignee = jira_res_search_json['issues'][5]['fields']['assignee']['accountId'] #담당자 계정 id
            #print(jira_assignee)
            #print(jira_summary)
            #print(jira_issueNum)
            #print(jira_priority)
            #time.sleep(20)


    def __init__(self):
        print("ZET VOC Classification")
    
