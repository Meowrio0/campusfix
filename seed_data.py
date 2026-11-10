"""Seeds the SQLite database with initial English NTPU campus reports."""
from database import reset_and_seed, get_reports

if __name__ == '__main__':
    reset_and_seed()
    reports = get_reports()
    print(f"Successfully seeded database with {len(reports)} campus reports:")
    for r in reports:
        print(f"  [{r['report_id']}] {r['title']} | Status: {r['status']} | Location: {r['location']}")
