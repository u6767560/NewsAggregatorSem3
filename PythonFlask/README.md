#README FOR WEB PROJECT
This part consists of the code of web (front-end and back-end) and the web crawler

## Front-end: jklExample_brief, static, templates Folder

-Folder jklExample: jklExample using intercooler developed by client.
- Folder static:  
contains the assets of the websites, including the css, js and image files
- Folder templates:  
contains the html file of the web project
- Venv  
the virtual environment of the python Flask

## Web Crawling: Source, Extraction Folder

- CatchNewsList.py  
the step of crawler the news from the news webpage using Python Goose
- Upload.py and NewsEntity.py  
the step of upload the whole news as the entity to the MongoDB
- setup.py  
the init of the project, contains the methods of loading the news and receive the AJAX request
- utility.py
contains some general functions for reuse

## local mongodb config:

db.config.insert({id:'config',ASMLastTime:0,
tidbinbillaLastTime:0,
cmagLastTime:0,
ABCNCLastTime:0,
ACATJLastTime:0,
ACTAUGLastTime:0,
ACTDRCLastTime:0,
ACTESALastTime:0,
ACTGMRLastTime:0,
ACTLACLastTime:0,
ACTLADPLastTime:0,
ACTLAMPILastTime:0,
ACTLAMPLastTime:0,
ACTLANPLastTime:0,
ACTMCJLastTime:0,
ACTMCPLastTime:0,
ACTMMRLastTime:0,
ACTPBLastTime:0,
ACTPCNLastTime:0,
ACTPMRLastTime:0,
ACTSLastTime:0,
ACTSCJLastTime:0,
ACTSCPLastTime:0,
ANU_CHELTLastTime:0,
ANU_CAEPRLastTime:0,
ANU_CASSLastTime:0,
ANU_CAPLastTime:0,
ANU_CECSLastTime:0,
ANU_CSSALastTime:0,
ANU_ECILastTime:0,
ANU_LSSLastTime:0,
ANU_MSILastTime:0,
ANU_MSLastTime:0,
ANU_MSSLastTime:0,
ANU_OLastTime:0,
ANU_PLastTime:0,
ANU_RSESLastTime:0,
ANU_SAALastTime:0,
ANU_SADLastTime:0,
ANU_SMLastTime:0,
ANU_SALastTime:0,
ANU_ULastTime:0,
AGACLastTime:0,
BBSNLastTime:0,
BGLastTime:0,
CBRCLastTime:0,
CITSALastTime:0,
CCSLastTime:0,
CCCLastTime:0,
CFBLastTime:0,
CFALastTime:0,
CGLQLastTime:0,
CINLastTime:0,
CITLastTime:0,
CJBLastTime:0,
CLLastTime:0,
CPSLastTime:0,
CQILastTime:0,
CSOLastTime:0,
CTCLastTime:0,
CFLastTime:0,
CNLastTime:0,
CFCLastTime:0,
ECLastTime:0,
EFLastTime:0,
FloriadeLastTime:0,
GALastTime:0,
HCLastTime:0,
KCLastTime:0,
LCLastTime:0,
NMALastTime:0,
NZALastTime:0,
OCLastTime:0,
SFLastTime:0,
SMLastTime:0,
TCLastTime:0,
TBCLastTime:0,
THFLastTime:0,
TQLastTime:0,
TQALastTime:0,
TRACTLastTime:0,
TSSCLastTime:0,
TACTLastTime:0,
TBLastTime:0,
UHLastTime:0,
UCLastTime:0,
WSLastTime:0,
WWTLastTime:0,
WoroniLastTime:0,
YMSLastTime:0,
abcLastTime:0,
sbsLastTime:0, 
cbr_timesLastTime:0, 
hercbrLastTime:0,
UC_LastTime:0, 
newsId:0})