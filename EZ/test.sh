set -ex
export CUDA_DEVICE_ORDER='PCI_BUS_ID'
export CUDA_VISIBLE_DEVICES=0

python main.py --env BreakoutNoFrameskip-v4 --case rubik --opr test --seed 0 --num_gpus 1 --num_cpus 1 --force \
  --test_episodes 32 \
  --load_model \
  --amp_type 'torch_amp' \
  --model_path 'model.p' \
  --info 'Test'