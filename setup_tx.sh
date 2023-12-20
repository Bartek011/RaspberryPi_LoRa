#=================================

echo
echo "START OF THE APP"
echo

python3 app.py

sleep 2

make -C ./lora-comm/dragino_lora_app/


cd ./lora-comm/dragino_lora_app
./dragino_lora_app sender

#=================================