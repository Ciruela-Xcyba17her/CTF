cmp -l kitters.jpg cattos.jpg | awk '{print $3}' > tmp.txt
number_list=`perl -pe 's/\n/ /g' tmp.txt`
for number in $number_list
do
	printf '%b' "\\${number}"
done
rm tmp.txt