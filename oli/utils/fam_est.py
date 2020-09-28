def write_odm_line( oc_item_name, ls_item_value, is_date=False, is_time=False, is_decimal=False, is_integer=False, is_utf8 = False):
    _one_line = ''
    if (ls_item_value):
        _this_value = ls_item_value
        if (is_date):
            _this_value = ls_item_value[0:10]
        if (is_time):
            # time field: check separator
            _this_value = _this_value.strip()
            _this_value = _this_value.replace('.',':')
            _this_value = _this_value.replace(';',':')
            _this_value = _this_value.replace(',',':')
            # if the length is 4, then try adding a zero
            if (len(_this_value) == 4):
                _this_value = '0' + _this_value
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
              
        _one_line = _one_line + '            <ItemData ItemOID="' + oc_item_name + '" Value="' + _this_value + '"/>'
    else:
        _one_line = _one_line + '            <ItemData ItemOID="' + oc_item_name + '" Value=""/>'
    #print(_one_line)
    return _one_line

def compose_odm(study_subject_oid, data_ls):
    """
    compose the xml-content to send to the web-service 
    just for this one occasion we write out everything literally
    and we make a big exception for birth-weight, which is given 
    in grams, but must be imported in kilo's and grams 
    """
    
    if (data_ls['q5birthweightgram'] is not None):
        kilograms = int(float(data_ls['q5birthweightgram'])/1000)
        I_EEFAM_BIRTHWEIGHTKG = str(kilograms)
        if (I_EEFAM_BIRTHWEIGHTKG == '0'):
            I_EEFAM_BIRTHWEIGHTKG = ''
        grams = int(float(data_ls['q5birthweightgram']) - kilograms * 1000)
        I_EEFAM_BIRTHWEIGHTGR = str(grams)
        #print(data_ls['q5birthweightgram'], I_EEFAM_BIRTHWEIGHTKG, I_EEFAM_BIRTHWEIGHTGR)
    else:
        I_EEFAM_BIRTHWEIGHTKG = ''
        I_EEFAM_BIRTHWEIGHTGR = ''

    # now repeat it all for the approximate birth weight
    if (data_ls['q05birthweightapp'] is not None):
        kilograms = int(float(data_ls['q05birthweightapp'])/1000)
        I_EEFAM_EE_BIRTHWEIGHT_APP_KG = str(kilograms)
        if (I_EEFAM_EE_BIRTHWEIGHT_APP_KG == '0'):
            I_EEFAM_EE_BIRTHWEIGHT_APP_KG = ''
        grams = int(float(data_ls['q05birthweightapp']) - kilograms * 1000)
        I_EEFAM_EE_BIRTHWEIGHT_APP_GR = str(grams)
        #print(data_ls['q05birthweightapp'], I_EEFAM_EE_BIRTHWEIGHT_APP_KG, I_EEFAM_EE_BIRTHWEIGHT_APP_GR)
    else:
        I_EEFAM_EE_BIRTHWEIGHT_APP_KG = ''
        I_EEFAM_EE_BIRTHWEIGHT_APP_GR = ''
    
    
    # opening tags
    _odm_data = ''
    _odm_data = _odm_data + '<ODM>'
    _odm_data = _odm_data + '  <ClinicalData StudyOID="S_CPEST">'
    _odm_data = _odm_data + '    <SubjectData SubjectKey="' + study_subject_oid + '">'
    _odm_data = _odm_data + '      <StudyEventData StudyEventOID="SE_EST_CP">'
    _odm_data = _odm_data + '        <FormData FormOID="F_EEFAMILYFORM_V4">'
    _odm_data = _odm_data + '          <ItemGroupData ItemGroupOID="IG_EEFAM_UNGROUPED" ItemGroupRepeatKey="1" TransactionType="Insert">'
    # data
    _odm_data = _odm_data + write_odm_line('I_EEFAM_RELATIONSHIP', data_ls['q1relationship'])
    _odm_data = _odm_data + write_odm_line('I_EEFAM_RELATIONSHIPOTH', data_ls['q1relationshipother'], is_utf8 = True)
    _odm_data = _odm_data + write_odm_line('I_EEFAM_DATEOFBIRTHCOMPLETE', data_ls['q3birthdatecomplete'], is_date=True)
    _odm_data = _odm_data + write_odm_line('I_EEFAM_GENDER', data_ls['q4sex'])
    # begin first exception !
    _odm_data = _odm_data + write_odm_line('I_EEFAM_BIRTHWEIGHTKG', I_EEFAM_BIRTHWEIGHTKG)
    _odm_data = _odm_data + write_odm_line('I_EEFAM_BIRTHWEIGHTGR', I_EEFAM_BIRTHWEIGHTGR)
    

    _odm_data = _odm_data + write_odm_line('I_EEFAM_EE_BIRTHWEIGHT_APP_KG', I_EEFAM_EE_BIRTHWEIGHT_APP_KG)
    _odm_data = _odm_data + write_odm_line('I_EEFAM_EE_BIRTHWEIGHT_APP_GR', I_EEFAM_EE_BIRTHWEIGHT_APP_GR)
    if (data_ls['q05birthweightunkn[1]'] == 'Y'):
        q05birthweightunkn = '1'
    else:
        q05birthweightunkn = ''

    _odm_data = _odm_data + write_odm_line('I_EEFAM_EE_BIRTHWEIGHT_UNKNOWN', q05birthweightunkn)
    # end first exception
   
    # generated from testcosi5
    _odm_data = _odm_data + write_odm_line('I_EEFAM_LATEEARLYBIRTH', data_ls['q6fullterm'])
    _odm_data = _odm_data + write_odm_line('I_EEFAM_BREASTFEDEVER', data_ls['q7breastfed'])
    _odm_data = _odm_data + write_odm_line('I_EEFAM_BREASTFEDHOWLONG', data_ls['q7breastfedmonths'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_EEFAM_EE_BREASTEXCLEVER', data_ls['q8breastfedexclusee'])

    _odm_data = _odm_data + write_odm_line('I_EEFAM_BREASTEXCLUSIVE', data_ls['q8breastexclusive'], is_integer = True)   
    _odm_data = _odm_data + write_odm_line('I_EEFAM_EE_BREASTEXCL_APP', data_ls['q8breastexclappee'], is_integer = True)   
    
    _odm_data = _odm_data + write_odm_line('I_EEFAM_DISTANCESCHOOLHOME', data_ls['q9distance'])
    _odm_data = _odm_data + write_odm_line('I_EEFAM_TRANSPSCHOOLFROM', data_ls['q10transpschoolfrom'])
    _odm_data = _odm_data + write_odm_line('I_EEFAM_TRANSPSCHOOLTO', data_ls['q10transpschoolto'])
    _odm_data = _odm_data + write_odm_line('I_EEFAM_REASONMOTORIZED', data_ls['q10areasonmotorized']) 
    _odm_data = _odm_data + write_odm_line('I_EEFAM_REASONMOTORIZEDOTH', data_ls['q10areasonmotorizedo'], is_utf8 = True)
    _odm_data = _odm_data + write_odm_line('I_EEFAM_SAFEROUTESCHOOL', data_ls['q11routesafe']) 
           
    _odm_data = _odm_data + write_odm_line('I_EEFAM_SPORTCLUB', data_ls['q12sportclubs'])
    _odm_data = _odm_data + write_odm_line('I_EEFAM_SPORTCLUBFREQ', data_ls['q13sportclubsfrequen'])
    
    _odm_data = _odm_data + write_odm_line('I_EEFAM_BEDTIME', data_ls['q14bedtime'], is_time = True)
    _odm_data = _odm_data + write_odm_line('I_EEFAM_WAKEUPTIME', data_ls['q15wakeuptime'], is_time = True)
    _odm_data = _odm_data + write_odm_line('I_EEFAM_WDSPLAYINGACTIVE', data_ls['q16playoutweekdays'])
    _odm_data = _odm_data + write_odm_line('I_EEFAM_WEPLAYINGACTIVE', data_ls['q16playouteweekdays'])
    
    _odm_data = _odm_data + write_odm_line('I_EEFAM_EE_WDSPORT', data_ls['q16asportweekdays'])
    _odm_data = _odm_data + write_odm_line('I_EEFAM_EE_WESPORT', data_ls['q16asportweekends'])
    
    _odm_data = _odm_data + write_odm_line('I_EEFAM_WDREADING', data_ls['q17readingweekdays'])
    _odm_data = _odm_data + write_odm_line('I_EEFAM_WEREADING', data_ls['q17readingweekends'])
    _odm_data = _odm_data + write_odm_line('I_EEFAM_WDELECTRONICSH', data_ls['q18wdelectronicsh'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_EEFAM_WDELECTRONICSM', data_ls['q18wdelectronicsm'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_EEFAM_WEELECTRONICSH', data_ls['q18weelectronicsh'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_EEFAM_WEELECTRONICSM', data_ls['q18weelectronicsm'], is_integer = True)
    
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
        
    _odm_data = _odm_data + write_odm_line('I_EEFAM_WDELECTRNOTATALL', q18wdelectrnotatall)
    _odm_data = _odm_data + write_odm_line('I_EEFAM_WEELECTRNOTATALL', q18weelectrnotatall)
    # end second exception !
    
    _odm_data = _odm_data + write_odm_line('I_EEFAM_BREAKFAST', data_ls['q19breakfast'])

    _odm_data = _odm_data + write_odm_line('I_EEFAM_FREQVEGETABLES', data_ls['q20[Vegetables]'])
    _odm_data = _odm_data + write_odm_line('I_EEFAM_FREQLEGUMES', data_ls['q20[Legumes]'])
    _odm_data = _odm_data + write_odm_line('I_EEFAM_FREQFRUIT', data_ls['q20[FreshFruit]'])
    _odm_data = _odm_data + write_odm_line('I_EEFAM_EE_FREQDRIEDFRUIT', data_ls['q20[DriedFruit]'])
    _odm_data = _odm_data + write_odm_line('I_EEFAM_FREQFRUITJUICE', data_ls['q20[FruitJuice]'])
    _odm_data = _odm_data + write_odm_line('I_EEFAM_EE_FREQNECTAR', data_ls['q20[Nectar]'])
    _odm_data = _odm_data + write_odm_line('I_EEFAM_EE_FREQWHOLEGRAIN', data_ls['q20[WholeGrain]'])
    _odm_data = _odm_data + write_odm_line('I_EEFAM_EE_FREQPORRIDGE', data_ls['q20[Porridge]'])
    _odm_data = _odm_data + write_odm_line('I_EEFAM_FREQCEREALS', data_ls['q20[Cereals]'])
    
    _odm_data = _odm_data + write_odm_line('I_EEFAM_CEREALSSUGAR', data_ls['q20cerealssugar'], is_integer = True)
    
    _odm_data = _odm_data + write_odm_line('I_EEFAM_EE_FREQMEAT_FRESH', data_ls['q20[MeatFresh]'])
    _odm_data = _odm_data + write_odm_line('I_EEFAM_EE_FREQMEAT_PROD', data_ls['q20[MeatProd]'])
    _odm_data = _odm_data + write_odm_line('I_EEFAM_EE_FREQFISH_FRESH', data_ls['q20[FishFresh]'])
    _odm_data = _odm_data + write_odm_line('I_EEFAM_EE_FREQFISH_PROD', data_ls['q20[FishProd]'])
    _odm_data = _odm_data + write_odm_line('I_EEFAM_FREQEGG', data_ls['q20[Egg]'])
    
    _odm_data = _odm_data + write_odm_line('I_EEFAM_FREQLOWFATMILK', data_ls['q20[LowFatMilk]'])
    _odm_data = _odm_data + write_odm_line('I_EEFAM_FREQWHOLEFATMILK', data_ls['q20[WholeFatMilk]'])
    _odm_data = _odm_data + write_odm_line('I_EEFAM_FREQDAIRY', data_ls['q20[Dairy]'])
    _odm_data = _odm_data + write_odm_line('I_EEFAM_FREQCHEESE', data_ls['q20[Cheese]'])
    _odm_data = _odm_data + write_odm_line('I_EEFAM_FREQFLAVOUREDMILK', data_ls['q20[FlavouredMilk]'])
    
    _odm_data = _odm_data + write_odm_line('I_EEFAM_EE_FREQNUTS_SEEDS', data_ls['q20[Nuts]'])
    _odm_data = _odm_data + write_odm_line('I_EEFAM_FREQCHIPS', data_ls['q20[Chips]'])
    _odm_data = _odm_data + write_odm_line('I_EEFAM_EE_FREQPIES', data_ls['q20[Pies]'])
    
    _odm_data = _odm_data + write_odm_line('I_EEFAM_FREQCANDY', data_ls['q20[Candy]'])
    _odm_data = _odm_data + write_odm_line('I_EEFAM_FREQSOFTDRINKS', data_ls['q20[SoftDrinksSugar]'])
    _odm_data = _odm_data + write_odm_line('I_EEFAM_FREQDIET', data_ls['q20[DietSoftDrinks]'])
    
    _odm_data = _odm_data + write_odm_line('I_EEFAM_WEIGHTOPINION', data_ls['q21weightopinion'])
    _odm_data = _odm_data + write_odm_line('I_EEFAM_HOUSEHOLDBLOODPRESSURE_2', data_ls['q22househouldbloodpr'])
    _odm_data = _odm_data + write_odm_line('I_EEFAM_HOUSEHOLDDIABETES', data_ls['q23householddiabetes'])
    _odm_data = _odm_data + write_odm_line('I_EEFAM_HOUSEHOLDCHOLESTEROL_2', data_ls['q24householdcholeste'])
    _odm_data = _odm_data + write_odm_line('I_EEFAM_SPOUSEHEIGHT', data_ls['q25spouseheight'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_EEFAM_SPOUSEWEIGHT', data_ls['q25spouseweight'])
    _odm_data = _odm_data + write_odm_line('I_EEFAM_YOUHEIGHT', data_ls['q25youheight'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_EEFAM_YOUWEIGHT', data_ls['q25youweight'])
    
    _odm_data = _odm_data + write_odm_line('I_EEFAM_YOUAGE', data_ls['q25youage'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_EEFAM_SPOUSEAGE', data_ls['q25spouseage'], is_integer = True)

    _odm_data = _odm_data + write_odm_line('I_EEFAM_HMNRBROTHER', data_ls['q26hmnr[Brother]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_EEFAM_HMNRELSE', data_ls['q26hmnr[Else]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_EEFAM_HMNRELSESPEC', data_ls['q26hmnrelsespec'], is_utf8 = True)
    _odm_data = _odm_data + write_odm_line('I_EEFAM_HMNRFATHER', data_ls['q26hmnr[Father]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_EEFAM_HMNRFOSTER', data_ls['q26hmnr[Foster]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_EEFAM_HMNRGRANDFATHER', data_ls['q26hmnr[Grandfather]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_EEFAM_HMNRGRANDMOTHER', data_ls['q26hmnr[Grandmother]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_EEFAM_HMNRMOTHER', data_ls['q26hmnr[Mother]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_EEFAM_HMNRSISTER', data_ls['q26hmnr[Sister]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_EEFAM_HMNRSTEPFATHER', data_ls['q26hmnr[Stepfather]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_EEFAM_HMNRSTEPMOTHER', data_ls['q26hmnr[Stepmother]'], is_integer = True)
     
    _odm_data = _odm_data + write_odm_line('I_EEFAM_EE_LANGUAGE', data_ls['q30language'])
    _odm_data = _odm_data + write_odm_line('I_EEFAM_EE_LANGUAGEOTH', data_ls['q30languageoth'], is_utf8 = True)
    
    _odm_data = _odm_data + write_odm_line('I_EEFAM_EDUSPOUSE', data_ls['q31eduspouse'])
    _odm_data = _odm_data + write_odm_line('I_EEFAM_EDUYOU', data_ls['q31eduyou'])
    _odm_data = _odm_data + write_odm_line('I_EEFAM_EARNINGS', data_ls['q32earnings'])
    _odm_data = _odm_data + write_odm_line('I_EEFAM_OCCUPSPOUSE', data_ls['q33occupspouse'])
    _odm_data = _odm_data + write_odm_line('I_EEFAM_OCCUPSPOUSEOTH', data_ls['q33occupspouseoth'], is_utf8 = True)
    _odm_data = _odm_data + write_odm_line('I_EEFAM_OCCUPYOU', data_ls['q33occupyou'])
    _odm_data = _odm_data + write_odm_line('I_EEFAM_OCCUPYOUOTH', data_ls['q33occupyouoth'], is_utf8 = True)
    
    _odm_data = _odm_data + write_odm_line('I_EEFAM_REMARKS', data_ls['q35remarks'], is_utf8 = True)

    # closing tags
    _odm_data = _odm_data + '          </ItemGroupData>'
    _odm_data = _odm_data + '        </FormData>'
    _odm_data = _odm_data + '      </StudyEventData>'
    _odm_data = _odm_data + '    </SubjectData>'
    _odm_data = _odm_data + '  </ClinicalData>'
    _odm_data = _odm_data + '</ODM>'

    return _odm_data
