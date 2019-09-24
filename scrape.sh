myip="$(dig +short myip.opendns.com @resolver1.opendns.com)"
/Users/localadmin/Documents/clash_royale/venv/bin/python update_df.py ${myip}