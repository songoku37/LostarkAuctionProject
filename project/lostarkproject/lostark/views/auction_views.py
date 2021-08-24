from flask import Blueprint, render_template, request

'''
    함수명 : devideKeysValues
    간　략 : Status 입력값 Dict을 Key와 Value로 분리합니다.
    상　세 : Status 입력값 Dict을 Key(아이템 or 전투특성 or 각인)와 Value(입력란)로 분리해 저장합니다.
    작성자 : 이성재
    날　짜 : 2021 - 08 - 24
    param : staticDic : 입력 사전값
            keys      : 키를 담을 빈 리스트
            values    : 값을 담을 빈 리스트
    why   : 딕셔너리 값을 이용하려면 키와 값을 분리해야 하기 때문입니다.
'''

def devideKeysValues(statusDic, keys, values):
    for key, value in statusDic.items():
        keys.append(key)
        values.append(value)

'''
    함수명 : inputItemName
    간　략 : 아이템 부위와 아이템 이름을 입력받아 저장합니다.
    상　세 : 각 아이템 부위와 아이템 이름을 입력받아 저장합니다.
    작성자 : 이성재
    날　짜 : 2021 - 08 - 24
    param : itemNameList : {아이템 부위 : 아이템이름} 입력받을 빈 리스트
            keys         : 키가 담긴 리스트(여기선 아이템부위) 
            values       : 값이 담긴 리스트 (여기선 아이템이름)
    why   : {아이템 부위 : 아이템이름}으로 나누어 저장하기 위해 만들었습니다. {아이템 : 아이템명} , {전투특성 or 각인 : 값} 의 저장하는 방법이 달라서 나누었습니다.
'''

def inputItemName(itemNamesList, keys, values):
    for itemNo in range(6):
        temp = {}
        temp[keys[itemNo]] = values[itemNo]
        itemNamesList.append(temp)

'''
    함수명 : classifyItemAbility
    간　략 : {전투특성 or 각인 : 값}으로 저장합니다.
    상　세 : {전투특성 or 각인 : 값}으로 저장하기 위해 필요한 분류작업을 합니다.(중복시 원래 있던 값과 더하고 전에 있던 값을 지우고 새로운 값을 저장하기 위해)
    작성자 : 이성재
    날　짜 : 2021 - 08 - 24
    param : itemAbilityDic : {전투특성 or 각인 : 값}으로 저장된 Dict을 키와 값으로 분류해 중복을 확인 하기 위해 사용했습니다.
            itemAbilitys   : {전투특성 or 각인 : 값}이 들어갈 빈 리스트
            values         : 값 리스트(전투특성 or 각인 or 아이템명 or 전투특성값 or 각인값), 
            temp           : {부위 : 전투특성 or 각인} or {부위 전투특성 or 각인값 : 값}, 
            abilityNo      : 전투특성 or 각인의 name 순서
    why   : {전투특성 or 각인 : 값}으로 저장하고 중복 전투특성 or 각인이 있을 때 입력된 값하고 더해서 표시하기 위한 작업이 필요해 만들었습니다.
'''

def classifyItemAbility(itemAbilityDic, itemAbilitys, values, temp, abilityNo):
    for k, v in itemAbilityDic.items():
        # 새로 들어온 값하고 기존 값하고 같을 경우 원래 있던 수치를 더합니다.
        if k == values[abilityNo]:
            removeIndex = 0
            del temp[values[abilityNo]]  # 새로 들어온 값 제거
            for removeResult2_dic in itemAbilitys:
                removeIndex = removeIndex + 1
                # 전에 들어온 값 제거
                for rk, rv in removeResult2_dic.items():
                    if k == rk:
                        del itemAbilitys[removeIndex - 1]
            temp[values[abilityNo]] = str(int(values[abilityNo + 1]) + int(v)) # 값이 str 형태라서 int형으로 변환해 더하고 str로 바꾸기

'''
    함수명 : inputAbilitys
    간　략 : {전투특성 or 각인 : 값}으로 저장합니다.
    상　세 : classifyItemAbility 호출해 {전투특성 or 각인 : 값}으로 분류해 저장합니다. 
    작성자 : 이성재
    날　짜 : 2021 - 08 - 24
    param : itemAbilitys : {전투특성 or 각인 : 값}이 들어갈 빈 리스트
            values       : 값 리스트(전투특성 or 각인 or 아이템명 or 전투특성값 or 각인값), 
            addSwi       : 값이 중복일 때 각각 다른 조취를 취해야하기 위한 구분자로 사용
    why   : 키(전투특성 or 각인)가 중복되면 다른 조취를 취해 저장하기 위해 만들었습니다.
'''

def inputAbilitys(itemAbilitys, values, addSwi):
    for abilityNo in range(5, 66, 2):
        temp = {}
        temp[values[abilityNo]] = values[abilityNo + 1]

        if itemAbilitys:
            addSwi = True
            for itemAbilitys_dic in itemAbilitys:
                classifyItemAbility(itemAbilitys_dic, itemAbilitys, values, temp, abilityNo)
        else:
            itemAbilitys.append(temp)
        if addSwi == True:
            itemAbilitys.append(temp)



# bp 라우트

bp = Blueprint('auction', __name__, url_prefix='/auction')

@bp.route('/',  methods=['GET', 'POST'])
def auction():

    status = None; addSwi = None
    p = 0
    itemNames = []; itemAbilitys = []; keys = []; values = []; itemNames = []
    temp = {}

    # 스테이터스에서 입력한 값을 받아 저장합니다.
    if request.method == 'POST':
        status = request.form

        # 키와 값으로 분류해서 리스트에 담습니다.
        devideKeysValues(status, keys, values)

        # 6개의 항목(아이템명)을 담습니다.
        inputItemName(itemNames, keys, values)

        # 아이템 특성을 담습니다.
        inputAbilitys(itemAbilitys, values, addSwi)

    #else :
        #현재상태를 먼저 입력해주세요
    url = request.full_path
    return render_template('auction/auction.html', url=url, itemNames=itemNames, itemAbilitys=itemAbilitys)

@bp.route('/',  methods=['GET', 'POST'])
def searching():
    return render_template('auction/auction.html')