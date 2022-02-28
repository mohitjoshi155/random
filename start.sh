
pip install wheel
pip install -r requirements.txt

if [[ -n $CONFIG_URL ]]; then
	wget -q $CONFIG_URL -O config.env
fi



if [[ -n $ACCOUNTS_ZIP_URL ]]; then
	wget -q $ACCOUNTS_ZIP_URL -O accounts.zip
	unzip -q -o accounts.zip
	rm accounts.zip
fi

./aria.sh; ./flaresolverr.sh; python3 -m bot; python3 clever.py 
