#=================================

make -C ./lora-comm/dragino_lora_app/

echo
echo "START OF THE RECEIVING"
echo

cd ./lora-comm/dragino_lora_app
./dragino_lora_app rec

#=================================