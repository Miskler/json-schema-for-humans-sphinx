#!/usr/bin/env python3
"""
Generate badge data from pytest JSON report
"""

import json
import os
import sys

def main():
    try:
        # Read test report
        with open('test_report.json', 'r') as f:
            data = json.load(f)

        # Calculate statistics
        summary = data.get('summary', {})
        total_tests = summary.get('total', 0)
        passed_tests = summary.get('passed', 0)
        failed_tests = summary.get('failed', 0)
        skipped_tests = summary.get('skipped', 0)
        
        # Handle case where tests weren't collected properly
        if total_tests == 0:
            # Try to get info from tests array
            tests = data.get('tests', [])
            if tests:
                total_tests = len(tests)
                passed_tests = sum(1 for test in tests if test.get('outcome') == 'passed')
                failed_tests = sum(1 for test in tests if test.get('outcome') == 'failed')
                skipped_tests = sum(1 for test in tests if test.get('outcome') == 'skipped')
        
        pass_rate = round((passed_tests / total_tests * 100) if total_tests > 0 else 0, 1)

        # Set environment variables
        with open(os.environ['GITHUB_ENV'], 'a') as f:
            f.write(f'TOTAL_TESTS={total_tests}\n')
            f.write(f'PASSED_TESTS={passed_tests}\n')
            f.write(f'FAILED_TESTS={failed_tests}\n')
            f.write(f'SKIPPED_TESTS={skipped_tests}\n')
            f.write(f'PASS_RATE={pass_rate}\n')
            
            # Determine colors and status
            if total_tests == 0:
                color = 'yellow'
                status = 'no tests'
            elif failed_tests == 0:
                color = 'brightgreen'
                if skipped_tests > 0:
                    status = f'{passed_tests} passed, {skipped_tests} skipped'
                else:
                    status = f'{passed_tests} passed'
            else:
                color = 'red'
                status = f'{failed_tests} failed, {passed_tests} passed'
                
            f.write(f'TEST_STATUS={status}\n')
            f.write(f'TEST_COLOR={color}\n')
            
            # Pass rate color
            if pass_rate >= 90:
                pass_color = 'brightgreen'
            elif pass_rate >= 70:
                pass_color = 'yellow'
            else:
                pass_color = 'red'
            f.write(f'PASS_RATE_COLOR={pass_color}\n')
            
        print(f"Generated badge data: {passed_tests}/{total_tests} tests passed ({pass_rate}%)")
        
    except Exception as e:
        print(f"Error generating badge data: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
