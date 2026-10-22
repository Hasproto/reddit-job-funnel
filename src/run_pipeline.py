# run_pipeline.py

# Order: extract -> transform -> load
 
import subprocess   
import sys         
import time        # to measure how long each step takes

STEPS = [
    "src/extract.py",
    "src/transform.py",
    "src/load.py",
]

for step in STEPS:
    print(f"\n===== Running {step} =====")
    
    start = time.time()

    # Run the step; stop everything if it fails.
    subprocess.run([sys.executable, step], check=True)

    seconds = time.time() - start
    print(f"Finished {step} in {seconds:.1f} seconds")

print("\nPipeline finished! To see the results, run:")
print("    streamlit run src/dashboard.py")