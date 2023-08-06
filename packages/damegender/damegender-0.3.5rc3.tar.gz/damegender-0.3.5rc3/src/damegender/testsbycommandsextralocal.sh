#!/usr/bin/bash
# Copyright (C) 2020  David Arroyo Menéndez (davidam@gmail.com)
# This file is part of Damegender.

#  Author: David Arroyo Menéndez <davidam@gmail.com>
#  Maintainer: David Arroyo Menéndez <davidam@gmail.com>
#  This file is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3, or (at your option)
#  any later version.
#
#  This file is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with damegender; see the file GPL.txt.  If not, write to
#  the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
#  Boston, MA 02110-1301 USA,

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color


cp config.cfg config.cfg.backup

echo "
[DEFAULT]
genderapi = no
genderize = no
nameapi = no
namsor = no
customsearch = no

[FILES]
genderapi = files/apikeys/genderapipass.txt
genderize = files/apikeys/genderizepass.txt
genderguesser = files/apikeys/genderguesserpass.txt
namsor = files/apikeys/namsorpass.txt
nameapi = files/apikeys/nameapipass.txt
" > config.cfg


python3 main.py "Jesús" --total=genderguesser > files/tests/mainjesusgenderguesser-$(date "+%Y-%m-%d-%H").txt

if ! cmp files/tests/mainjesusgenderguesser.txt files/tests/mainjesusgenderguesser-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
	echo -e  "mainjesusgenderguesser test is ${RED}failing${NC}"
else
	echo -e  "mainjesusgenderguesser test is ${GREEN}ok${NC}"
fi

python3 main.py "Sara" --total=genderguesser > files/tests/mainsaragenderguesser-$(date "+%Y-%m-%d-%H").txt

if ! cmp files/tests/mainsaragenderguesser.txt files/tests/mainsaragenderguesser-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
	echo -e  "mainsaragenderguesser test is ${RED}failing${NC}"
else
	echo -e  "mainsaragenderguesser test is ${GREEN}ok${NC}"
fi

python3 main.py sara --total=genderguesser > files/tests/mainsara2genderguesser-$(date "+%Y-%m-%d-%H").txt

if ! cmp files/tests/mainsaragenderguesser.txt files/tests/mainsara2genderguesser-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
	echo -e  "mainsara2genderguesser test is ${RED}failing${NC}"
else
	echo -e  "mainsara2genderguesser test is ${GREEN}ok${NC}"
fi

python3 api2gender.py David --api="genderguesser" > files/tests/api2genderDavidgenderguesser-$(date "+%Y-%m-%d-%H").txt

if ! cmp files/tests/api2genderDavidgenderguesser.txt files/tests/api2genderDavidgenderguesser-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
	echo -e  "api2genderDavidgenderguesser test is ${RED}failing${NC}"
else
	echo -e  "api2genderDavidgenderguesser test is ${GREEN}ok${NC}"
fi


python3 accuracy.py --measure="precision" --csv="files/names/min.csv" --api=genderize --jsondownloaded="files/names/genderizefiles_names_min.csv.json" > files/tests/accuracygenderizeminjsonprecision-$(date "+%Y-%m-%d-%H").txt

if ! cmp files/tests/accuracygenderizeminjsonprecision.txt files/tests/accuracygenderizeminjsonprecision-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
	echo -e  "accuracygenderizeminjsonprecision test is ${RED}failing${NC}"
else
	echo -e  "accuracygenderizeminjsonprecision test is ${GREEN}ok${NC}"
fi


python3 accuracy.py --api="genderguesser" --csv=files/names/min.csv --jsondownloaded=files/names/min.csv.json > files/tests/accuracygenderguesser-$(date "+%Y-%m-%d-%H").txt

if ! cmp files/tests/accuracygenderguesser.txt files/tests/accuracygenderguesser-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
	echo -e  "accuracygenderguesser test is ${RED}failing${NC}"
else
	echo -e  "accuracygenderguesser test is ${GREEN}ok${NC}"
fi

python3 accuracy.py --api="genderguesser" --measure="precision" --csv=files/names/partialnoundefined.csv --jsondownloaded=files/names/partialnoundefined.csv.json > files/tests/accuracygenderguesserpartialnoundefinedjsonprecision-$(date "+%Y-%m-%d-%H").txt

if ! cmp files/tests/accuracygenderguesserpartialnoundefinedjsonprecision.txt files/tests/accuracygenderguesserpartialnoundefinedjsonprecision-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
	echo -e  "accuracypartialprecisiongenderguesser test is ${RED}failing${NC}"
else
	echo -e  "accuracypartialprecisiongenderguesser test is ${GREEN}ok${NC}"
fi

python3 accuracy.py --api="genderguesser" --measure="f1score" --csv=files/names/partialnoundefined.csv --jsondownloaded=files/names/partialnoundefined.csv.json > files/tests/accuracygenderguesserpartialnoundefinedjsonf1score-$(date "+%Y-%m-%d-%H").txt

if ! cmp files/tests/accuracygenderguesserpartialnoundefinedjsonf1score.txt files/tests/accuracygenderguesserpartialnoundefinedjsonf1score-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
	echo -e  "accuracypartialf1scoregenderguesser test is ${RED}failing${NC}"
else
	echo -e  "accuracypartialf1scoregenderguesser test is ${GREEN}ok${NC}"
fi

python3 accuracy.py --api="genderguesser" --measure="recall" --csv=files/names/partialnoundefined.csv --jsondownloaded=files/names/partialnoundefined.csv.json > files/tests/accuracypartialrecallgenderguesser-$(date "+%Y-%m-%d-%H").txt

if ! cmp files/tests/accuracypartialrecallgenderguesser.txt files/tests/accuracypartialrecallgenderguesser-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
	echo -e  "accuracypartialrecallgenderguesser test is ${RED}failing${NC}"
else
	echo -e  "accuracypartialrecallgenderguesser test is ${GREEN}ok${NC}"
fi

python3 accuracy.py --measure=accuracy --csv=files/names/partialnoundefined.csv --jsondownloaded=files/names/partialnoundefined.csv.json --api="damegender" > files/tests/accuracypartialnound-$(date "+%Y-%m-%d-%H").txt

if ! cmp files/tests/accuracypartialnound.txt files/tests/accuracypartialnound-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
	echo -e  "accuracypartialdamegender test is ${RED}failing${NC}"
else
	echo -e  "accuracypartialdamegender test is ${GREEN}ok${NC}"
fi


python3 confusion.py --api="damegender" --dimensions=2x3 --csv=files/names/min.csv --jsondownloaded=files/names/min.csv.json > files/tests/confusiondamegender-$(date "+%Y-%m-%d-%H").txt

if ! cmp files/tests/confusiondamegender.txt files/tests/confusiondamegender-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
	echo -e  "confusiondamegender test is ${RED}failing${NC}"
else
	echo -e  "confusiondamegender test is ${GREEN}ok${NC}"
fi

python3 confusion.py --api="genderguesser" --dimensions=2x3 --csv=files/names/min.csv --jsondownloaded=files/names/min.csv.json > files/tests/confusiongenderguesser-$(date "+%Y-%m-%d-%H").txt

if ! cmp files/tests/confusiongenderguesser.txt files/tests/confusiongenderguesser-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
	echo -e  "confusiongenderguesser test is ${RED}failing${NC}"
else
	echo -e  "confusiongenderguesser test is ${GREEN}ok${NC}"
fi

python3 confusion.py --csv=files/names/min.csv --jsondownloaded=files/names/namsorfiles_names_min.csv.json --api=namsor > files/tests/confusionnamsorjson-$(date "+%Y-%m-%d-%H").txt

if ! cmp files/tests/confusionnamsorjson.txt files/tests/confusionnamsorjson-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
	echo -e  "confusion namsor test is ${RED}failing${NC}"
else
	echo -e  "confusion namsor test is ${GREEN}ok${NC}"
fi


python3 confusion.py --csv=files/names/min.csv --jsondownloaded=files/names/genderizefiles_names_min.csv.json --api=genderize > files/tests/confusiongenderizejson-$(date "+%Y-%m-%d-%H").txt

if ! cmp files/tests/confusiongenderizejson.txt files/tests/confusiongenderizejson-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
	echo -e  "confusion genderize test is ${RED}failing${NC}"
else
	echo -e  "confusion genderize test is ${GREEN}ok${NC}"
fi

python3 errors.py --csv="files/names/partial.csv" --api="genderguesser" > files/tests/errorsgenderguesser-$(date "+%Y-%m-%d-%H").txt

if ! cmp files/tests/errorsgenderguesser.txt files/tests/errorsgenderguesser-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
	echo -e  "errorsgenderguesser test is ${RED}failing${NC}"
else
	echo -e  "errorsgenderguesser test is ${GREEN}ok${NC}"
fi

rm -rf /tmp/clonedir
echo -e  "cleaning temporary files"
rm files/tests/*$(date "+%Y")*.txt

echo -e  "cleaning temporary files"
rm files/tests/*$(date "+%Y")*.txt

echo -e  "restoring the config"
cp config.cfg.backup config.cfg
rm config.cfg.backup
