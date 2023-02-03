set -ex
export CUDA_DEVICE_ORDER='PCI_BUS_ID'
export CUDA_VISIBLE_DEVICES=0,1,2,3

python main.py --env BreakoutNoFrameskip-v4 --case rubik --opr train --force \
  --num_gpus 1 --num_cpus 1 --cpu_actor 1 --gpu_actor 1 \
  --object_store_memory 1610612736 \
  --seed 0 \
  --p_mcts_num 4 \
  --use_priority \
  --use_max_priority \
  --amp_type 'torch_amp' \
  --info 'EfficientZero-V1'
