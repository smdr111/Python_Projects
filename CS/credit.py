num = input("Enter you card number: ")
split_num = list(num)[::-1]
beginning = num[:2]
n = len(split_num)

sec_num = [int(split_num[i])  * 2 for i in range(1,n,2)]
second_total = sum(int(i)  for num in sec_num for i in str(num) )
first_total = sum(int(split_num[j]) for j in range(0,n,2))

total = second_total + first_total

print('VALID') if total % 10 == 0 else print('INVALID')

if beginning == '34' or beginning == '37':
    print("American Express")
elif beginning == '51' or beginning == '52' or beginning == '53' or beginning == '54' or beginning == '55':
    print("MasterCard")
elif beginning[:1] == '4':
    print('VISA')
