#!/usr/bin/env python3
"""
Script to download pre-trained pose estimation models
Run this before starting the web app
"""

import os
import urllib.request
import sys
from pathlib import Path

# Model URLs
MODELS = {
    'coco': {
        'prototxt': {
            'url': 'https://raw.githubusercontent.com/CMU-Perceptual-Computing-Lab/openpose/master/models/pose/coco/pose_deploy_linevec.prototxt',
            'filename': 'models/coco/pose_deploy_linevec.prototxt'
        },
        'weights': {
            'url': 'http://posefs1.perception.cs.cmu.edu/OpenPose/models/pose/coco/pose_iter_440000.caffemodel',
            'filename': 'models/coco/pose_iter_440000.caffemodel',
            'size': '200MB'
        }
    },
    'mpii': {
        'prototxt': {
            'url': 'https://raw.githubusercontent.com/CMU-Perceptual-Computing-Lab/openpose/master/models/pose/mpi/pose_deploy_linevec_faster_4_stages.prototxt',
            'filename': 'models/mpi/pose_deploy_linevec_faster_4_stages.prototxt'
        },
        'weights': {
            'url': 'http://posefs1.perception.cs.cmu.edu/OpenPose/models/pose/mpi/pose_iter_160000.caffemodel',
            'filename': 'models/mpi/pose_iter_160000.caffemodel',
            'size': '200MB'
        }
    }
}


def create_directories():
    """Create necessary model directories"""
    for model_type in MODELS.keys():
        os.makedirs(f'models/{model_type}', exist_ok=True)
    print("✓ Created model directories")


def download_file(url, filepath, description):
    """Download a file with progress indication"""
    print(f"\n📥 Downloading {description}...")
    print(f"   URL: {url}")
    
    # Create parent directory if it doesn't exist
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    try:
        urllib.request.urlretrieve(url, filepath)
        print(f"✓ Downloaded: {filepath}")
        return True
    except Exception as e:
        print(f"✗ Failed to download {description}")
        print(f"  Error: {str(e)}")
        print(f"  Manual download: {url}")
        return False


def check_existing_files():
    """Check which model files already exist"""
    existing = {}
    for model_type, model_data in MODELS.items():
        existing[model_type] = {
            'prototxt': os.path.exists(model_data['prototxt']['filename']),
            'weights': os.path.exists(model_data['weights']['filename'])
        }
    return existing


def print_status(existing):
    """Print status of existing files"""
    print("\n📋 Model Files Status:")
    print("-" * 60)
    for model_type, files in existing.items():
        print(f"\n{model_type.upper()}:")
        proto_status = "✓ Found" if files['prototxt'] else "✗ Missing"
        weights_status = "✓ Found" if files['weights'] else "✗ Missing"
        print(f"  Prototxt: {proto_status}")
        print(f"  Weights:  {weights_status} ({MODELS[model_type]['weights']['size']})")


def main():
    """Main download function"""
    print("=" * 60)
    print("OpenCV Pose Estimation - Model Download Utility")
    print("=" * 60)
    
    # Check existing files
    existing = check_existing_files()
    print_status(existing)
    
    # Create directories
    create_directories()
    
    # Download models
    downloaded_any = False
    for model_type, model_data in MODELS.items():
        print(f"\n\n🔄 Processing {model_type.upper()} model...")
        
        # Download prototxt
        if not existing[model_type]['prototxt']:
            download_file(
                model_data['prototxt']['url'],
                model_data['prototxt']['filename'],
                f"{model_type} prototxt"
            )
            downloaded_any = True
        else:
            print(f"✓ {model_type} prototxt already exists")
        
        # Download weights
        if not existing[model_type]['weights']:
            print(f"\n⚠️  Weights file is ~{model_data['weights']['size']}")
            response = input(f"Download {model_type} weights? (y/n): ").lower()
            if response == 'y':
                download_file(
                    model_data['weights']['url'],
                    model_data['weights']['filename'],
                    f"{model_type} weights"
                )
                downloaded_any = True
            else:
                print(f"Skipped {model_type} weights download")
        else:
            print(f"✓ {model_type} weights already exist")
    
    # Final status
    print("\n" + "=" * 60)
    final_existing = check_existing_files()
    print("📊 Final Status:")
    all_ready = all(
        files['prototxt'] and files['weights'] 
        for files in final_existing.values()
    )
    
    if all_ready:
        print("✓ All models ready! You can start the web app now.")
    else:
        print("⚠️  Some models are missing. Download them first.")
        print("\nTo download missing files, run this script again and select 'y'")
    
    print("=" * 60)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✗ Download cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {str(e)}")
        sys.exit(1)
