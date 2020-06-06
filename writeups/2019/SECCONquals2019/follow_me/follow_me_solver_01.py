import json

f = open('calc.trace')
json_data = json.load(f)

inst_addr_list = []
for i in range(len(json_data)):
    try:
        inst_addr_list.append(json_data[i]['inst_addr'])
    except:
        continue

answer = ''
for i in range(len(inst_addr_list)):
    if inst_addr_list[i] == '0x55f6b4d44e87':
        ia = inst_addr_list[i - 1]
        if ia == '0x55f6b4d44c4f':
            answer += '1'
        elif ia == '0x55f6b4d44c13':
            answer += ','
        elif ia == '0x55f6b4d44dab':
            answer += 'm'
        elif ia == '0x55f6b4d44e02':
            answer += 'M'
        elif ia == '0x55f6b4d44cfd':
            answer += '-'
        elif ia == '0x55f6b4d44ca6':
            answer += '+'
        elif ia == '0x55f6b4d44d54':
            answer += '*'

print(answer)
input('[END OF PROGRAM]')
