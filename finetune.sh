export TORCH_LOGS="+dynamo,recompiles,graph_breaks"
export TORCHDYNAMO_VERBOSE=1
export WANDB_MODE="offline"
export NCCL_P2P_DISABLE=1
export TORCH_NCCL_ENABLE_MONITORING=0
export TOKENIZERS_PARALLELISM=false

##############
# GPU config #
##############
## if single GPU available
GPU_IDS="0"
ACCELERATE_CONFIG_FILE="accelerate_configs/uncompiled_1.yaml"

## if two GPUs available
# GPU_IDS="0,1"
# ACCELERATE_CONFIG_FILE="accelerate_configs/uncompiled_2.yaml"

## if four GPUs available
# GPU_IDS="0,1,2,3"
# ACCELERATE_CONFIG_FILE="accelerate_configs/uncompiled_4.yaml"

## if eight GPUs available
# GPU_IDS="0,1,2,3,4,5,6,7"
# ACCELERATE_CONFIG_FILE="accelerate_configs/uncompiled_8.yaml"


# Training Configurations
learning_rate="1e-4"
lr_schedule="constant"
optimizer="adamw"
steps="400"


# Absolute path to where the data is located.
DATA_ROOT="."
CAPTION_COLUMN="training-configs/frog/prompts.txt"                        ## CHANGE THIS ACCORDINGLY
VIDEO_COLUMN="training-configs/frog/videos.txt"                           ## CHANGE THIS ACCORDINGLY
MASK_COLUMN="training-configs/frog/masks.txt"                             ## CHANGE THIS ACCORDINGLY
VALIDATION_IMAGES_DIR="training-configs/frog/input_images_for_validation" ## CHANGE THIS ACCORDINGLY
output_dir="results/frog"                                                 ## CHANGE THIS ACCORDINGLY



#########################################################################
# if 40 GB GPU, --gradient_checkpointing should be contained as below.
# if 80 GB GPU, remove the --gradient_checkpointing argument,
# which makes the gradient backprop signficantly slower.
#########################################################################

cmd="accelerate launch --config_file $ACCELERATE_CONFIG_FILE --gpu_ids $GPU_IDS training/cogvideox/train_cogvideox_image_to_video_lora_dcc.py \
  --pretrained_model_name_or_path THUDM/CogVideoX-5b-I2V \
  --data_root $DATA_ROOT \
  --caption_column $CAPTION_COLUMN \
  --video_column $VIDEO_COLUMN \
  --mask_column $MASK_COLUMN \
  --height_buckets 480 \
  --width_buckets 720 \
  --frame_buckets 49 \
  --dataloader_num_workers 8 \
  --pin_memory \
  --validation_prompt \"a brown frog is sitting on a rock\" \
  --validation_images_dir $VALIDATION_IMAGES_DIR \
  --validation_prompt_separator ::: \
  --num_validation_videos 1 \
  --validation_steps 200 \
  --seed 42 \
  --rank 128 \
  --lora_alpha 128 \
  --mixed_precision bf16 \
  --output_dir $output_dir \
  --max_num_frames 49 \
  --train_batch_size 1 \
  --max_train_steps $steps \
  --checkpointing_steps 100 \
  --gradient_accumulation_steps 1 \
  --gradient_checkpointing \
  --learning_rate $learning_rate \
  --lr_scheduler $lr_schedule \
  --lr_warmup_steps 0 \
  --lr_num_cycles 1 \
  --enable_slicing \
  --enable_tiling \
  --noised_image_dropout 0.05 \
  --optimizer $optimizer \
  --beta1 0.9 \
  --beta2 0.95 \
  --weight_decay 0.001 \
  --max_grad_norm 1.0 \
  --allow_tf32 \
  --report_to wandb \
  --nccl_timeout 10000"

echo "Running command: $cmd"
eval $cmd
echo -ne "-------------------- Finished executing script --------------------\n\n"
