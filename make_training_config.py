import os
import sys
import argparse
import logging
import shutil

try:
    import cv2
except ImportError:
    sys.exit("Error: OpenCV is not installed. Please try `pip install opencv-python`.")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate training configurations for fine-tuning CogVideoX-I2V."
    )
    parser.add_argument(
        '--training_data_dir',
        type=str,
        required=True,
        help='Path to the directory containing your training data (warped videos and masks).'
    )
    parser.add_argument(
        '--original_data_dir',
        type=str,
        required=True,
        help='Path to the directory containing the input video (the original video clip).'
    )
    parser.add_argument(
        '--original_prompt',
        type=str,
        required=True,
        help='The text prompt describing the input video.'
    )
    parser.add_argument(
        '--training_config_dir',
        type=str,
        required=True,
        help='Directory where generated training configuration files will be saved.'
    )
    return parser.parse_args()


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def generate_original_video(original_data_dir, fps=7):
    """
    Check for a 'video' subdirectory in original_data_dir and compile all images into original.mp4.
    """
    video_folder = os.path.join(original_data_dir, 'video')
    if not os.path.isdir(video_folder):
        logging.error(f"'video' folder not found in {original_data_dir}")
        sys.exit(1)

    exts = ('.jpg', '.jpeg', '.png')
    image_files = sorted(
        [f for f in os.listdir(video_folder) if f.lower().endswith(exts)]
    )
    if not image_files:
        logging.error(f"No image files found in {video_folder}")
        sys.exit(1)

    first_path = os.path.join(video_folder, image_files[0])
    frame = cv2.imread(first_path)
    if frame is None:
        logging.error(f"Cannot read image file: {first_path}")
        sys.exit(1)
    height, width = frame.shape[:2]

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_path = os.path.join(original_data_dir, 'original.mp4')
    writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    for fname in image_files:
        img_path = os.path.join(video_folder, fname)
        img = cv2.imread(img_path)
        if img is None:
            logging.warning(f"Skipping unreadable image: {img_path}")
            continue
        if img.shape[:2] != (height, width):
            img = cv2.resize(img, (width, height))
        writer.write(img)
    writer.release()
    logging.info(f"Generated video: {output_path}")


def get_valid_folders(training_data_dir):
    """
    Returns a sorted list of subfolders containing both 'warped.mp4' and a 'mask' directory.
    """
    valid = []
    for name in sorted(os.listdir(training_data_dir)):
        folder = os.path.join(training_data_dir, name)
        if os.path.isdir(folder) and \
           os.path.isfile(os.path.join(folder, 'warped.mp4')) and \
           os.path.isdir(os.path.join(folder, 'mask')):
            valid.append(name)
    return valid


def write_videos_txt(valid_folders, original_data_dir, training_data_dir, config_dir):
    path = os.path.join(config_dir, 'videos.txt')
    lines = [os.path.join(original_data_dir, 'original.mp4')]
    lines += [os.path.join(training_data_dir, name, 'warped.mp4') for name in valid_folders]
    with open(path, 'w') as f:
        f.write('\n'.join(lines))
    logging.info(f"Wrote videos.txt with {len(lines)} entries to {path}")


def write_masks_txt(valid_folders, original_data_dir, training_data_dir, config_dir):
    path = os.path.join(config_dir, 'masks.txt')
    lines = [os.path.join(original_data_dir, 'mask')]
    lines += [os.path.join(training_data_dir, name, 'mask') for name in valid_folders]
    with open(path, 'w') as f:
        f.write('\n'.join(lines))
    logging.info(f"Wrote masks.txt with {len(lines)} entries to {path}")


def write_prompts_txt(valid_folders, original_prompt, config_dir):
    path = os.path.join(config_dir, 'prompts.txt')
    mapping = {
        'down':    ('CAMERA_ORBIT_DOWN',  'Camera movement orbit down,'),
        'up':      ('CAMERA_ORBIT_UP',    'Camera movement orbit up,'),
        'left':    ('CAMERA_ORBIT_LEFT',  'Camera movement orbit left,'),
        'right':   ('CAMERA_ORBIT_RIGHT', 'Camera movement orbit right,'),
        'zoomin':  ('CAMERA_ZOOM_IN',     'Camera movement zoom in,'),
        'zoomout': ('CAMERA_ZOOM_OUT',    'Camera movement zoom out,'),
    }
    lines = [original_prompt]
    for name in valid_folders:
        token, text = None, None
        for key, (tk, tx) in mapping.items():
            if name.startswith(key):
                token, text = tk, tx
                break
        if token:
            lines.append(f"{token} {text} {original_prompt}")
        else:
            logging.warning(f"No camera mapping for folder '{name}', using original prompt.")
            lines.append(original_prompt)
    with open(path, 'w') as f:
        f.write('\n'.join(lines))
    logging.info(f"Wrote prompts.txt with {len(lines)} entries to {path}")


def generate_validation_images(valid_folders, original_data_dir, training_data_dir, config_dir):
    """
    Copy the first frame from original and each warped folder into a validation images folder.
    """
    src_folder = os.path.join(original_data_dir, 'video')
    exts = ('.jpg', '.jpeg', '.png')
    all_imgs = sorted([f for f in os.listdir(src_folder) if f.lower().endswith(exts)])
    if not all_imgs:
        logging.error(f"No images found in {src_folder} for validation sampling.")
        sys.exit(1)
    first_img = all_imgs[0]
    val_dir = os.path.join(config_dir, 'input_images_for_validation')
    os.makedirs(val_dir, exist_ok=True)

    # Copy original first image
    src_path = os.path.join(src_folder, first_img)
    ext = os.path.splitext(first_img)[1]
    dst_path = os.path.join(val_dir, f"original{ext}")
    shutil.copyfile(src_path, dst_path)
    logging.info(f"Copied validation image: {dst_path}")

    # Copy first warped image from each valid folder
    for name in valid_folders:
        warped_folder = os.path.join(training_data_dir, name, 'warped')
        imgs = sorted([f for f in os.listdir(warped_folder) if f.lower().endswith(exts)])
        if not imgs:
            logging.warning(f"No images in warped folder: {warped_folder}")
            continue
        first = imgs[0]
        src_w = os.path.join(warped_folder, first)
        # prefix = name.split('_')[0]
        # dst_w = os.path.join(val_dir, f"{prefix}{os.path.splitext(first)[1]}")
        dst_w = os.path.join(val_dir, f"{name}{os.path.splitext(first)[1]}")
        shutil.copyfile(src_w, dst_w)
        logging.info(f"Copied validation image: {dst_w}")


def main():
    args = parse_args()
    setup_logging()

    logging.info(f"Training data directory: {args.training_data_dir}")
    logging.info(f"Original data directory: {args.original_data_dir}")
    logging.info(f"Original prompt: {args.original_prompt}")
    logging.info(f"Output config directory: {args.training_config_dir}")

    os.makedirs(args.training_config_dir, exist_ok=True)

    generate_original_video(args.original_data_dir)

    valid = get_valid_folders(args.training_data_dir)
    if not valid:
        logging.error(f"No valid folders with warped.mp4 and mask/ found in {args.training_data_dir}")
        sys.exit(1)
    logging.info(f"Found {len(valid)} valid folders: {valid}")

    write_videos_txt(valid, args.original_data_dir, args.training_data_dir, args.training_config_dir)
    write_masks_txt(valid, args.original_data_dir, args.training_data_dir, args.training_config_dir)
    write_prompts_txt(valid, args.original_prompt, args.training_config_dir)
    generate_validation_images(valid, args.original_data_dir, args.training_data_dir, args.training_config_dir)

    logging.info("Configuration files and validation images generation complete.")


if __name__ == '__main__':
    main()
