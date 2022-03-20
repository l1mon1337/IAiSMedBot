from validator import validate_age

units = ['-1','101','a','/','$']

def test_val():
    for n in range(len(units)):
        status = validate_age(units[n])
        if status == False:
            print('Ok')
        else: print('There is mistake with: ' + units[n])