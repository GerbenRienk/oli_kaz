'''
Created November and December 2018

@author: GerbenRienk
'''
import time
import datetime
import json
import base64
from utils.logmailer import MailThisLogFile
from utils.dictfile import readDictFile
from utils.fam_est import compose_odm
from utils.limesurveyrc2api import LimeSurveyRemoteControl2API
from utils.ocwebservices import dataWS
from utils.pg_api import ConnToOliDB, PGSubject
from utils.reporter import Reporter

def cycle_through_syncs():
    my_report = Reporter()
    
    start_time = datetime.datetime.now()
    my_report.append_to_report('INFO: cycle started at ' + str(start_time))
    # read configuration file for usernames and passwords and other parameters
    config=readDictFile('oli.config')
    # set from this config the survey id, sid, because it used everywhere
    sid = int(config['sid'])
    
    # create a connection to the postgresql database
    conn = ConnToOliDB()
    my_report.append_to_report(conn.init_result)

    # initialize the oc-webservice
    myDataWS = dataWS(config['userName'], config['password'], config['baseUrl'])
    
    tokens={}
    tokens_list = read_ls_tokens(config, 0, 10)
    for token in tokens_list:
        tokens[token['token']]=token['participant_info']['firstname']
    tokens_list = read_ls_tokens(config, 10, 10)
    for token in tokens_list:
        tokens[token['token']]=token['participant_info']['firstname']
    print(tokens)
    
    # close the file so we can send it
    my_report.close_file()
    MailThisLogFile('logs/report.txt')
    
def read_ls_responses(config):
    """
    function to use the ls api and read all responses into a dictionary
    parameters
    config is the dictionary with all configuration elements
    """
    # collecting LimeSurvey data
    # Make a session, which is a bit of overhead, but the script will be running for hours.
    # get the survey id of the one survey we're interested in and cast it into an integer
    sid = int(config['sid'])
    api = LimeSurveyRemoteControl2API(config['lsUrl'])
    session_req = api.sessions.get_session_key(config['lsUser'], config['lsPassword'])
    session_key = session_req.get('result')
    # now get all responses of our survey
    api_response2 = api.responses.export_responses(session_key, sid)
    responses_b64 = base64.b64decode(api_response2['result'])
    responses_dict = json.loads(responses_b64)   #this is a dictionary
    return responses_dict['responses']

def read_ls_tokens(config, start=0, limit=10000 ):
    """
    function to use the ls api and read all tokens into a dictionary
    parameters
    config is the dictionary with all configuration elements
    """
    # collecting LimeSurvey data
    # Make a session, which is a bit of overhead, but the script will be running for hours.
    # get the survey id of the one survey we're interested in and cast it into an integer
    sid = int(config['sid'])
    api = LimeSurveyRemoteControl2API(config['lsUrl'])
    session_req = api.sessions.get_session_key(config['lsUser'], config['lsPassword'])
    session_key = session_req.get('result')
    # now get all responses of our survey
    tokens = api.tokens.list_participants(session_key, sid, start, limit)
    return tokens['result']
    
if __name__ == '__main__':
    cycle_through_syncs()
