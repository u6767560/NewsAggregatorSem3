This folder contains everything that currently working on the server, including extraction in either RSS or Goose way.

1. Australia_vocb.txt: key_words to filter Australia news from all Global news.

2. CatchNewsList.py & Upload_v0.py : Goose extraction.

3. RSSTextualExtraction.py: RSS extraction.

4. NewsEntity.py: the step of the whole news as the entity to the MongoDB

5. RepeatUpload.py: repeat call Goose and RSS extraction every one hour.

6. UpdateTimeRank.py: Update timerank according to time difference from news publish time and current time.

7. utility.py:contains some general functions for reuse



The thing used to set up mongodb:


use Configure

db.config.remove({})

db.config.insert({id:'config',
A_Stylish_MomentLastTime:0,
TidbinbillaLastTime:0,
Canberra_Museum_and_GalleryLastTime:0,
ABC_News_CanberraLastTime:0,
ACT_Civil_and_Administrative_TribunalLastTime:0,
ACT_Apple_Users_GroupLastTime:0,
ACT_Deafness_Resource_CentreLastTime:0,
ACT_Emergency_Service_AgencyLastTime:0,
Chief_Minister_Treasury_and_Economic_Development_DirectorateLastTime:0,
ACT_Legislative_Assembly_CalendarLastTime:0,
ACT_Legislative_Assembly_Daily_ProgramLastTime:0,
ACT_Legislative_Assembly_Matters_Of_Public_ImportanceLastTime:0,
ACT_Legislative_Assembly_Minutes_Of_ProceedingsLastTime:0,
ACT_Legislative_Assembly_Notice_PapersLastTime:0,
ACT_Magistrates_Court_JudgementsLastTime:0,
ACT_Magistrates_Court_PublicationsLastTime:0,
ACT_Minister_Media_ReleaseLastTime:0,
ACT_Police_BlogLastTime:0,
ACT_Police_Community_NewsLastTime:0,
ACT_Police_Media_ReleasesLastTime:0,
ACT_ShelterLastTime:0,
ACT_Supreme_Court_JudgmentsLastTime:0,
ACT_Supreme_Court_PublicationsLastTime:0,
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
Ainslie_and_Gorman_Arts_CentresLastTime:0,
Band_of_BrothersLastTime:0,
Beaver_GalleriesLastTime:0,
CBR_CanberraLastTime:0,
CIT_Student_AssociationLastTime:0,
Canberra_Choral_SocietyLastTime:0,
Canberra_Critics_CircleLastTime:0,
Canberra_Film_BlogLastTime:0,
Canberra_Foodies_AdventuresLastTime:0,
Canberra_Gay_and_Lesbian_QwireLastTime:0,
CINLastTime:0,
CITLastTime:0,
Canberra_Jazz_BlogspotLastTime:0,
Canberra_LiberalsLastTime:0,
Canberra_Philharmonic_SocietyLastTime:0,
Canberra_Quilters_IncLastTime:0,
Canberra_Symphony_OrchestraLastTime:0,
Canberra_Theatre_CentreLastTime:0,
Capital_FootballLastTime:0,
City_NewsLastTime:0,
Cross_Fit_CanberraLastTime:0,
Eat_CanberraLastTime:0,
Eelighten_FestivalLastTime:0,
FloriadeLastTime:0,
Griffin_AcceleratorLastTime:0,
Her_CanberraLastTime:0,
Kanga_CupLastTime:0,
Life_In_CanberraLastTime:0,
National_Museum_AustraliaLastTime:0,
National_ZooLastTime:0,
Outin_CanberraLastTime:0,
SO_FrankLastTime:0,
Spilt_MilkLastTime:0,
Tennis_CanberraLastTime:0,
The_Basement_CanberraLastTime:0,
Healing_FoundationLastTime:0,
The_Queanbeyan_Performing_Arts_CentreLastTime:0,
The_Queanbeyan_AgeLastTime:0,
Riot_ACTLastTime:0,
The_Style_SideLastTime:0,
Tourism_ACTLastTime:0,
Traveland_BeyondLastTime:0,
Uni_HouseLastTime:0,
UCLastTime:0,
Who_ShootsLastTime:0,
Woodland_and_WetlandsLastTime:0,
WoroniLastTime:0,
Young_Music_SocietyLastTime:0,
ABCLastTime:0,
SBSLastTime:0, 
Canberra_TimesLastTime:0, 
Her_CanberraLastTime:0,
UC_LastTime:0, 
newsId:0})

use NewsAggregator

db.news.remove({})