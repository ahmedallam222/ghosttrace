from ghosttrace.ghost_writer import GhostWriter
import json
import os
import sys

def mock_evaluate(decision, context):
    return {"status": "rejected", "reason": "Test rejection for PyPI verification"}

def run_verification():
    print("🔍 Starting GhostTrace Verification...")
    
    output_dir = "."
    ghost_file = os.path.join(output_dir, ".ghost.json")
    
    # Clean up previous test file if exists
    if os.path.exists(ghost_file):
        os.remove(ghost_file)
        
    try:
        writer = GhostWriter(output_dir=output_dir)
        
        # Test evaluate_and_record
        print("🧪 Testing evaluate_and_record...")
        writer.evaluate_and_record(
            decision="Deploy to PyPI",
            evaluate_fn=mock_evaluate,
            context={"version": "0.3.0"},
            input_tokens=1000,
            output_tokens=500,
            model="gpt-4"
        )
        
        # Check if .ghost.json exists and contains the expected data
        if os.path.exists(ghost_file):
            with open(ghost_file, "r") as f:
                data = json.load(f)
                
                if "phantom_branches" in data and len(data["phantom_branches"]) > 0:
                    branch = data["phantom_branches"][0]
                    if "tracking" in branch:
                        tracking = branch["tracking"]
                        required_fields = ["tokens_used", "latency_ms", "estimated_cost_usd"]
                        
                        if all(field in tracking for field in tracking):
                            print(f"📊 Metrics: {tracking}")
                            print("\n✅ Test Passed: All tracking fields are present and working correctly.")
                            return True
                        else:
                            print("\n❌ Test Failed: Missing tracking fields.")
                    else:
                        print("\n❌ Test Failed: 'tracking' field not found in branch.")
                else:
                    print("\n❌ Test Failed: 'phantom_branches' not found or empty.")
        else:
            print("\n❌ Test Failed: .ghost.json not created.")
            
    except Exception as e:
        print(f"\n❌ Test Failed with error: {str(e)}")
        
    return False

if __name__ == "__main__":
    success = run_verification()
    if not success:
        sys.exit(1)
