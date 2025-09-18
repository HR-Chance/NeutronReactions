from finalCalc_API_fcn import alloyCalculation
import sys

def main():
    alloy = "Fe74C4Mn8Co4Zn10"  # Example alloy formula
    trans, ac = alloyCalculation(alloy)
    print(f"Total Percentage Transmuted:", f"{trans:.3e}", "%")
    print(f"Total Activity:", f"{ac*2.7e-11:.3e}", "Ci")  # Convert Bq to Ci

if __name__ == "__main__":
    main()