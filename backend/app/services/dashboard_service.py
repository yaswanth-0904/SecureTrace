from app.models.dna_record import DNARecord


def get_dashboard_stats(db):
    total_dna_records = db.query(DNARecord).count()

    flagged_records = db.query(DNARecord).filter(
        DNARecord.is_flagged == 1
    ).count()

    frozen_records = db.query(DNARecord).filter(
        DNARecord.is_frozen == 1
    ).count()

    recovered_records = db.query(DNARecord).filter(
        DNARecord.recovered_amount > 0
    ).count()

    total_recovered_amount = 0

    records = db.query(DNARecord).all()

    for record in records:
        total_recovered_amount += record.recovered_amount

    return {
        "total_dna_records": total_dna_records,
        "flagged_records": flagged_records,
        "frozen_records": frozen_records,
        "recovered_records": recovered_records,
        "total_recovered_amount": total_recovered_amount
    }