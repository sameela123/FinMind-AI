import unittest
import sys
import os
import time

def run_finmind_test_suite():
    # Set stdout encoding if needed
    if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass

    print("=" * 70)
    print("  FINMIND AI - MILESTONE 5: USER TESTING & EDGE CASE VALIDATION  ")
    print("  GCP Project ID: velvety-mason-417105 | Dataset: finmind_analytics")
    print("=" * 70)
    print()

    start_time = time.time()
    
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir="tests", pattern="test_*.py")

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    elapsed_time = round(time.time() - start_time, 3)

    print()
    print("=" * 70)
    print("                    TEST EXECUTION SUMMARY                       ")
    print("=" * 70)
    print(f"  Total Tests Executed : {result.testsRun}")
    print(f"  Successful Tests     : {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"  Failures             : {len(result.failures)}")
    print(f"  Errors               : {len(result.errors)}")
    print(f"  Elapsed Time         : {elapsed_time} seconds")
    print("=" * 70)

    if result.wasSuccessful():
        print("  Status: [PASS] ALL TESTS PASSED - MILESTONE 5 VALIDATED SUCCESSFULLY!")
    else:
        print("  Status: [FAIL] TEST SUITE FAILURE - Issues detected during validation.")
    print("=" * 70)

    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_finmind_test_suite()
    sys.exit(0 if success else 1)
