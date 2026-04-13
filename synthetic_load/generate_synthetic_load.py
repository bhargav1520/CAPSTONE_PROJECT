"""
Generate Synthetic Hourly Load Profile for a Month

This script uses pre-trained K-Means and Markov models to generate
synthetic hourly electricity consumption data scaled to match a target
monthly consumption value.

Usage:
    python generate_synthetic_load.py <monthly_kwh> [--days DAYS] [--seed SEED]

Example:
    python generate_synthetic_load.py 350
    python generate_synthetic_load.py 450 --days 31 --seed 42
"""

import numpy as np
import pandas as pd
import os
import sys
import joblib
import argparse
from datetime import datetime, timedelta

# =========================================================
# PATH SETUP
# =========================================================
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

KMEANS_PATH = os.path.join(os.path.dirname(__file__), "kmeans_model.pkl")
MARKOV_PATH = os.path.join(os.path.dirname(__file__), "markov_transition.npy")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "outputs")

# =========================================================
# VALIDATE MODELS EXIST
# =========================================================
def validate_models():
    """Check if trained models exist"""
    if not os.path.exists(KMEANS_PATH):
        print("❌ ERROR: kmeans_model.pkl not found!")
        print("   Please run: python train_kmeans.py")
        sys.exit(1)
    
    if not os.path.exists(MARKOV_PATH):
        print("❌ ERROR: markov_transition.npy not found!")
        print("   Please run: python markov_model.py")
        sys.exit(1)

# =========================================================
# GENERATE SYNTHETIC LOAD
# =========================================================
def generate_synthetic_load(monthly_kwh, days=30, random_seed=None):
    """
    Generate synthetic hourly load profile using Markov model
    
    Args:
        monthly_kwh (float): Target monthly consumption in kWh
        days (int): Number of days to generate (default 30)
        random_seed (int): Random seed for reproducibility
        
    Returns:
        numpy.array: Hourly load values (length = days * 24)
    """
    if random_seed is not None:
        np.random.seed(random_seed)
    
    # Load models
    kmeans = joblib.load(KMEANS_PATH)
    transition = np.load(MARKOV_PATH)
    
    K = kmeans.n_clusters
    states = 24 * K
    hours = days * 24
    
    print(f"\n Model Info:")
    print(f"   Clusters: {K}")
   # print(f"   States: {states} (24 hours × {K} clusters)")
    print(f"   Generating: {hours} hours ({days} days) ")
    
    # =========================================================
    # MARKOV CHAIN SIMULATION
    # =========================================================
    synthetic = []
    
    # Random initial state
    cluster = np.random.randint(K)
    hour = 0
    state = hour * K + cluster
    
    for t in range(hours):
        hour = t % 24
        cluster = state % K
        
        # Get load value from cluster center for this hour
        value = kmeans.cluster_centers_[cluster][hour]
        synthetic.append(value)
        
        # Transition to next state
        state = np.random.choice(states, p=transition[state])
    
    synthetic = np.array(synthetic)
    
    # =========================================================
    # SCALE TO TARGET MONTHLY CONSUMPTION
    # =========================================================
    current_total = synthetic.sum()
    scale_factor = monthly_kwh / current_total
    synthetic_scaled = synthetic * scale_factor
    
    # print(f"\n⚡ Energy Scaling:")
    # print(f"   Before scaling: {current_total:.2f} kWh")
    # print(f"   Target: {monthly_kwh:.2f} kWh")
    # print(f"   Scale factor: {scale_factor:.4f}")
    # print(f"   After scaling: {synthetic_scaled.sum():.2f} kWh")
    
    return synthetic_scaled

# =========================================================
# SAVE TO CSV
# =========================================================
def save_to_csv(load_data, monthly_kwh, days):
    """
    Save synthetic load to CSV with timestamps
    
    Args:
        load_data (numpy.array): Hourly load values
        monthly_kwh (float): Target monthly consumption
        days (int): Number of days
    """
    # Create timestamps starting from today
    start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    timestamps = [start_date + timedelta(hours=i) for i in range(len(load_data))]
    
    # Create DataFrame
    # Use column name compatible with LoadModel (t_kWh)
    df = pd.DataFrame({
        'Timestamp': timestamps,
        't_kWh': load_data
    })
    
    # Generate filename
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filename = f"monthly_synthetic_{int(monthly_kwh)}kWh_{days}days.csv"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    # Save
    df.to_csv(filepath, index=False)
    
    print(f"\n Synthetic load saved to:")
    print(f"   {filepath}")
    print(f"\n Statistics:")
    print(f"   Total hours: {len(load_data)}")
    print(f"   Mean hourly: {load_data.mean():.3f} kWh")
    print(f"   Max hourly: {load_data.max():.3f} kWh")
    print(f"   Min hourly: {load_data.min():.3f} kWh")
    print(f"   Std dev: {load_data.std():.3f} kWh")
    
    return filepath

# =========================================================
# MAIN FUNCTION
# =========================================================
def main():
    parser = argparse.ArgumentParser(
        description='Generate synthetic hourly load profile for a month',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_synthetic_load.py 350
  python generate_synthetic_load.py 450 --days 31
  python generate_synthetic_load.py 300 --days 28 --seed 42
        """
    )
    
    parser.add_argument(
        'monthly_kwh',
        type=float,
        help='Target monthly consumption in kWh (e.g., 350)'
    )
    
    parser.add_argument(
        '--days',
        type=int,
        default=30,
        help='Number of days to generate (default: 30)'
    )
    
    parser.add_argument(
        '--seed',
        type=int,
        default=None,
        help='Random seed for reproducibility (optional)'
    )
    
    args = parser.parse_args()
    
    # Validate inputs
    if args.monthly_kwh <= 0:
        print(" ERROR: monthly_kwh must be positive")
        sys.exit(1)
    
    if args.days <= 0 or args.days > 365:
        print(" ERROR: days must be between 1 and 365")
        sys.exit(1)
    
    print("="*60)
    print(" SYNTHETIC LOAD GENERATOR")
    print("="*60)
    print(f"Target Monthly Consumption: {args.monthly_kwh} kWh")
    print(f"Generation Period: {args.days} days")
    if args.seed is not None:
        print(f"Random Seed: {args.seed}")
    
    # Validate models exist
    validate_models()
    
    # Generate synthetic load
    synthetic_load = generate_synthetic_load(
        monthly_kwh=args.monthly_kwh,
        days=args.days,
        random_seed=args.seed
    )
    
    # Save to CSV
    save_to_csv(synthetic_load, args.monthly_kwh, args.days)
    
    print("\n" + "="*60)
    print(" GENERATION COMPLETE!")
    print("="*60)

if __name__ == "__main__":
    main()
