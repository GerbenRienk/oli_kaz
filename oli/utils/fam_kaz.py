def write_odm_line( oc_item_name, ls_item_value, is_date=False, is_time=False, is_decimal=False, is_integer=False, is_utf8 = False):
    _one_line = ''
    if (not ls_item_value is None):
        _this_value = ls_item_value
        if (is_date):
            _this_value = ls_item_value[0:10]
        if (is_time):
            ''' for kaz we used a dropdown for time, bed and wake up
            '''
            _my_time = _this_value[0:2] + ':' + _this_value[2:]
            _this_value = _my_time
            
            '''
            # time field: check separator
            _this_value = _this_value.strip()
            _this_value = _this_value.replace('.',':')
            _this_value = _this_value.replace(';',':')
            _this_value = _this_value.replace(',',':')
            # if the length is 4, then try adding a zero
            if (len(_this_value) == 4):
                _this_value = '0' + _this_value
            '''
        if (is_decimal):
            _this_value = str(ls_item_value)
        if (is_integer):
            _this_value = str(int(float(ls_item_value)))
        if (is_utf8):
            _this_value = str(_this_value.encode(encoding="ascii",errors="xmlcharrefreplace"))
            # now we have something like b'some text &amp; more' so we want to loose the first two characters and the last one
            # TODO: make this nicer somehow
            _this_value = _this_value[2:]
            _this_value = _this_value[:-1]
              
        _one_line = _one_line + '            <ItemData ItemOID="' + oc_item_name + '" Value="' + _this_value + '"/>\n'
    else:
        _one_line = _one_line + '            <ItemData ItemOID="' + oc_item_name + '" Value=""/>\n'
    #print(_one_line)
    return _one_line

def compose_odm(study_subject_oid, data_ls, verbose=False):
    """
    compose the xml-content to send to the web-service 
    just for this one occasion we write out everything literally
    and we make a big exception for birth-weight, which is given 
    in grams, but must be imported in kilo's and grams 
    """
    
    if (data_ls['q05birthweightgram'] is not None):
        if verbose:
            print('q05birthweightgram: %s' % data_ls['q05birthweightgram'])
        kilograms = int(float(data_ls['q05birthweightgram'])/1000)
        I_KZFAM_BIRTHWEIGHTKG = str(kilograms)
        if (I_KZFAM_BIRTHWEIGHTKG == '0'):
            I_KZFAM_BIRTHWEIGHTKG = ''
        grams = int(float(data_ls['q05birthweightgram']) - kilograms * 1000)
        I_KZFAM_BIRTHWEIGHTGR = str(grams)
        #print(data_ls['q5birthweightgram'], I_KZFAM_BIRTHWEIGHTKG, I_KZFAM_BIRTHWEIGHTGR)
    else:
        I_KZFAM_BIRTHWEIGHTKG = ''
        I_KZFAM_BIRTHWEIGHTGR = ''

    # opening tags
    _odm_data = ''
    _odm_data = _odm_data + '<ODM>\n'
    _odm_data = _odm_data + '  <ClinicalData StudyOID="S_CDKAZ">\n'
    _odm_data = _odm_data + '    <SubjectData SubjectKey="' + study_subject_oid + '">\n'
    _odm_data = _odm_data + '      <StudyEventData StudyEventOID="SE_KAZ_CD">\n'
    _odm_data = _odm_data + '        <FormData FormOID="F_KZFAMILYFORM_V1">\n'
    _odm_data = _odm_data + '          <ItemGroupData ItemGroupOID="IG_KZFAM_UNGROUPED" ItemGroupRepeatKey="1" TransactionType="Insert">\n'
    # data
    _odm_data = _odm_data + write_odm_line('I_KZFAM_RELATIONSHIP', data_ls['q01relationship'])
    _odm_data = _odm_data + write_odm_line('I_KZFAM_RELATIONSHIPOTH', data_ls['q01relationshipother'], is_utf8 = True)
    _odm_data = _odm_data + write_odm_line('I_KZFAM_DATEOFBIRTHCOMPLETE', data_ls['q03birthdatecomplete'], is_date=True)
    _odm_data = _odm_data + write_odm_line('I_KZFAM_GENDER', data_ls['q04sex'])
    
    # begin first exception !
    _odm_data = _odm_data + write_odm_line('I_KZFAM_BIRTHWEIGHTKG', I_KZFAM_BIRTHWEIGHTKG)
    _odm_data = _odm_data + write_odm_line('I_KZFAM_BIRTHWEIGHTGR', I_KZFAM_BIRTHWEIGHTGR)
    # end first exception
   
    # generated from testcosi5
    _odm_data = _odm_data + write_odm_line('I_KZFAM_LATEEARLYBIRTH', data_ls['q06fullterm'])
    _odm_data = _odm_data + write_odm_line('I_KZFAM_BREASTFEDEVER', data_ls['q07breastfed'])
    _odm_data = _odm_data + write_odm_line('I_KZFAM_BREASTFEDHOWLONG', data_ls['q07breastfedmonths'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_KZFAM_BREASTEXCLEVER', data_ls['q08breastfedexclusee'])
    _odm_data = _odm_data + write_odm_line('I_KZFAM_BREASTEXCLUSIVE', data_ls['q08breastexclusive'], is_integer = True)   
        
    _odm_data = _odm_data + write_odm_line('I_KZFAM_DISTANCESCHOOLHOME', data_ls['q9distance'])
    _odm_data = _odm_data + write_odm_line('I_KZFAM_TRANSPSCHOOLFROM', data_ls['q10transpschoolfrom'])
    _odm_data = _odm_data + write_odm_line('I_KZFAM_TRANSPSCHOOLTO', data_ls['q10transpschoolto'])
    _odm_data = _odm_data + write_odm_line('I_KZFAM_REASONMOTORIZED', data_ls['q10areasonmotorized']) 
    _odm_data = _odm_data + write_odm_line('I_KZFAM_REASONMOTORIZEDOTH', data_ls['q10areasonmotorizedo'], is_utf8 = True)
    _odm_data = _odm_data + write_odm_line('I_KZFAM_SAFEROUTESCHOOL', data_ls['q11routesafe']) 
           
    _odm_data = _odm_data + write_odm_line('I_KZFAM_SPORTCLUB', data_ls['q12sportclubs'])
    _odm_data = _odm_data + write_odm_line('I_KZFAM_SPORTCLUBFREQ', data_ls['q13sportclubsfrequen'])
    
    _odm_data = _odm_data + write_odm_line('I_KZFAM_BEDTIME', data_ls['q14bedtime'], is_time = True)
    _odm_data = _odm_data + write_odm_line('I_KZFAM_WAKEUPTIME', data_ls['q15wakeuptime'], is_time = True)
    _odm_data = _odm_data + write_odm_line('I_KZFAM_WDSPLAYINGACTIVE', data_ls['q16playoutweekdays'])
    _odm_data = _odm_data + write_odm_line('I_KZFAM_WEPLAYINGACTIVE', data_ls['q16playouteweekdays'])
    _odm_data = _odm_data + write_odm_line('I_KZFAM_WDREADING', data_ls['q17readingweekdays'])
    _odm_data = _odm_data + write_odm_line('I_KZFAM_WEREADING', data_ls['q17readingweekends'])
    _odm_data = _odm_data + write_odm_line('I_KZFAM_WDELECTRONICSH', data_ls['q18wdelectronicsh'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_KZFAM_WDELECTRONICSM', data_ls['q18wdelectronicsm'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_KZFAM_WEELECTRONICSH', data_ls['q18weelectronicsh'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_KZFAM_WEELECTRONICSM', data_ls['q18weelectronicsm'], is_integer = True)
    
    # begin second exception !
    # these checkboxes can only be Y in ls
    # which corresponds to 1 in oc
    if (data_ls['q18wdelectrnotatall[1]'] == 'Y'):
        q18wdelectrnotatall = '1'
    else:
        q18wdelectrnotatall = ''
    if (data_ls['q18weelectrnotatall[1]'] == 'Y'):
        q18weelectrnotatall = '1'
    else:
        q18weelectrnotatall = ''
        
    _odm_data = _odm_data + write_odm_line('I_KZFAM_WDELECTRNOTATALL', q18wdelectrnotatall)
    _odm_data = _odm_data + write_odm_line('I_KZFAM_WEELECTRNOTATALL', q18weelectrnotatall)
    # end second exception !
    
    _odm_data = _odm_data + write_odm_line('I_KZFAM_BREAKFAST', data_ls['q19breakfast'])
    _odm_data = _odm_data + write_odm_line('I_KZFAM_FREQFRUIT', data_ls['q20[FreshFruit]'])
    _odm_data = _odm_data + write_odm_line('I_KZFAM_FREQVEGETABLES', data_ls['q20[Vegetables]'])
    _odm_data = _odm_data + write_odm_line('I_KZFAM_FREQSOFTDRINKS', data_ls['q20[SoftDrinksSugar]'])
    _odm_data = _odm_data + write_odm_line('I_KZFAM_WEIGHTOPINION', data_ls['q21weightopinion'])

    _odm_data = _odm_data + write_odm_line('I_KZFAM_HOUSEHOLDBLOODPRESSURE', data_ls['q22househouldbloodpr'])
    _odm_data = _odm_data + write_odm_line('I_KZFAM_HOUSEHOLDDIABETES', data_ls['q23householddiabetes'])
    _odm_data = _odm_data + write_odm_line('I_KZFAM_HOUSEHOLDCHOLESTEROL', data_ls['q24householdcholeste'])
    _odm_data = _odm_data + write_odm_line('I_KZFAM_SPOUSEHEIGHT', data_ls['q25spouseheight'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_KZFAM_SPOUSEWEIGHT', data_ls['q25spouseweight'])
    _odm_data = _odm_data + write_odm_line('I_KZFAM_YOUHEIGHT', data_ls['q25youheight'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_KZFAM_YOUWEIGHT', data_ls['q25youweight'])
    _odm_data = _odm_data + write_odm_line('I_KZFAM_YOUAGE', data_ls['q25youage'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_KZFAM_SPOUSEAGE', data_ls['q25spouseage'], is_integer = True)

    _odm_data = _odm_data + write_odm_line('I_KZFAM_HMNRBROTHER', data_ls['q26hmnr[Brother]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_KZFAM_HMNRELSE', data_ls['q26hmnr[Else]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_KZFAM_HMNRELSESPEC', data_ls['q26hmnrelsespec'], is_utf8 = True)
    _odm_data = _odm_data + write_odm_line('I_KZFAM_HMNRFATHER', data_ls['q26hmnr[Father]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_KZFAM_HMNRFOSTER', data_ls['q26hmnr[Foster]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_KZFAM_HMNRGRANDFATHER', data_ls['q26hmnr[Grandfather]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_KZFAM_HMNRGRANDMOTHER', data_ls['q26hmnr[Grandmother]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_KZFAM_HMNRMOTHER', data_ls['q26hmnr[Mother]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_KZFAM_HMNRSISTER', data_ls['q26hmnr[Sister]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_KZFAM_HMNRSTEPFATHER', data_ls['q26hmnr[Stepfather]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_KZFAM_HMNRSTEPMOTHER', data_ls['q26hmnr[Stepmother]'], is_integer = True)

    _odm_data = _odm_data + write_odm_line('I_KZFAM_KZ_CHILDBORN', data_ls['q27achildbornkz'])
    _odm_data = _odm_data + write_odm_line('I_KZFAM_KZ_CHILDBORNOTH', data_ls['q27achildbornother'], is_utf8 = True)
    _odm_data = _odm_data + write_odm_line('I_KZFAM_KZ_MOTHERBORN', data_ls['q28amotherbornkz'])
    _odm_data = _odm_data + write_odm_line('I_KZFAM_KZ_MOTHERBORNOTH', data_ls['q28amotherbornother'], is_utf8 = True)
    _odm_data = _odm_data + write_odm_line('I_KZFAM_KZ_FATHERBORN', data_ls['q29afatherbornkz'])
    _odm_data = _odm_data + write_odm_line('I_KZFAM_KZ_FATHERBORNOTH', data_ls['q29afatherbornother'], is_utf8 = True)

    _odm_data = _odm_data + write_odm_line('I_KZFAM_KZ_LANGUAGE', data_ls['q30language'])
    _odm_data = _odm_data + write_odm_line('I_KZFAM_KZ_LANGUAGEOTH', data_ls['q30languageoth'], is_utf8 = True)
    
    _odm_data = _odm_data + write_odm_line('I_KZFAM_EDUSPOUSE', data_ls['q31eduspouse'])
    _odm_data = _odm_data + write_odm_line('I_KZFAM_EDUYOU', data_ls['q31eduyou'])
    _odm_data = _odm_data + write_odm_line('I_KZFAM_EARNINGS', data_ls['q32earnings'])
    _odm_data = _odm_data + write_odm_line('I_KZFAM_OCCUPSPOUSE', data_ls['q33occupspouse'])
    _odm_data = _odm_data + write_odm_line('I_KZFAM_OCCUPSPOUSEOTH', data_ls['q33occupspouseoth'], is_utf8 = True)
    _odm_data = _odm_data + write_odm_line('I_KZFAM_OCCUPYOU', data_ls['q33occupyou'])
    _odm_data = _odm_data + write_odm_line('I_KZFAM_OCCUPYOUOTH', data_ls['q33occupyouoth'], is_utf8 = True)

    _odm_data = _odm_data + write_odm_line('I_KZFAM_KZ_WASH_HANDS', data_ls['q34washhandskz'])
    _odm_data = _odm_data + write_odm_line('I_KZFAM_KZ_WASH_HANDS_COMM', data_ls['q34washhandscomkz'], is_utf8 = True)
    _odm_data = _odm_data + write_odm_line('I_KZFAM_KZ_NO_WASH_REASON', data_ls['q35nowashreasonkz'])
    _odm_data = _odm_data + write_odm_line('I_KZFAM_KZ_NO_WASH_REASON_OTHER', data_ls['q35nowashreasonothkz'], is_utf8 = True)
    _odm_data = _odm_data + write_odm_line('I_KZFAM_KZ_WATER', data_ls['q36accesswaterkz'])
    _odm_data = _odm_data + write_odm_line('I_KZFAM_KZ_WATER_COMM', data_ls['q36accesswatercommen'], is_utf8 = True)
    _odm_data = _odm_data + write_odm_line('I_KZFAM_KZ_TOILET', data_ls['q37toiletkz'])
    _odm_data = _odm_data + write_odm_line('I_KZFAM_KZ_TIOLET_COMM', data_ls['q37toiletcommentskz'], is_utf8 = True)
    _odm_data = _odm_data + write_odm_line('I_KZFAM_KZ_TOILET_LOCATION', data_ls['q38toiletlocationkz'])
    _odm_data = _odm_data + write_odm_line('I_KZFAM_KZ_TOILET_LOCATION_OTHER', data_ls['q38toiletlocationoth'], is_utf8 = True)
    _odm_data = _odm_data + write_odm_line('I_KZFAM_KZ_NO_TOILET_REASON', data_ls['q39notoiletreasonkz'], is_utf8 = True)


    _odm_data = _odm_data + write_odm_line('I_KZFAM_DATECOMPLETION', data_ls['q34datecompletion'], is_date = True)
    _odm_data = _odm_data + write_odm_line('I_KZFAM_REMARKS', data_ls['q35remarks'], is_utf8 = True)

    # closing tags
    _odm_data = _odm_data + '          </ItemGroupData>'
    _odm_data = _odm_data + '        </FormData>'
    _odm_data = _odm_data + '      </StudyEventData>'
    _odm_data = _odm_data + '    </SubjectData>'
    _odm_data = _odm_data + '  </ClinicalData>'
    _odm_data = _odm_data + '</ODM>'

    return _odm_data
