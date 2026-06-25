from fastapi import APIRouter
from fastapi import Depends
from app.models.audit_log import AuditLog
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.models.transaction import Transaction
from app.models.dna_record import DNARecord
from app.models.user import User
from app.models.dna_record import DNARecord
from app.schemas.transaction_schema import TransactionCreate
from app.schemas.dna_split_schema import DNASplitRequest
from app.schemas.login_schema import LoginRequest

from app.services.dashboard_service import get_dashboard_stats
from app.services.token_service import generate_token
from app.services.risk_service import calculate_risk_score
from app.services.dna_service import generate_dna_code
from app.services.lineage_service import generate_child_dna
from app.services.family_tree_service import build_tree
from app.services.auth_validator import validate_token

router = APIRouter()


@router.post("/create-transaction")
def create_transaction(
    payload: TransactionCreate,
    db: Session = Depends(get_db)
):
    transaction = Transaction(
        sender_account_id=payload.sender_account_id,
        receiver_account_id=payload.receiver_account_id,
        amount=payload.amount
    )

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    dna_code = generate_dna_code(transaction.id)

    risk_score = calculate_risk_score(
        payload.amount
    )

    is_flagged = 0
    is_frozen = 0

    if risk_score >= 90:
        is_flagged = 1
        is_frozen = 1

    dna_record = DNARecord(
        dna_code=dna_code,
        transaction_id=transaction.id,
        amount=payload.amount,
        remaining_amount=payload.amount,
        risk_score=risk_score,
        is_flagged=is_flagged,
        is_frozen=is_frozen,
    )

    db.add(dna_record)
    db.commit()

    return {

        "transaction_id": transaction.id,
        "dna_code": dna_code
    }


@router.get("/trace/{dna_code}")
def trace_dna(
    dna_code: str,
    db: Session = Depends(get_db)
):
    dna_record = db.query(DNARecord).filter(
        DNARecord.dna_code == dna_code
    ).first()

    if not dna_record:
        return {
            "message": "DNA Record Not Found"
        }

    return {
    "dna_code": dna_record.dna_code,
    "transaction_id": dna_record.transaction_id,
    "amount": dna_record.amount,
    "remaining_amount": dna_record.remaining_amount,
    "status": dna_record.status,
    "child_count": dna_record.child_count,
    "is_flagged": dna_record.is_flagged,
    "is_frozen": dna_record.is_frozen,
    "recovered_amount": dna_record.recovered_amount,
    "risk_score": dna_record.risk_score,
    
}


@router.post("/split-dna")
def split_dna(
    payload: DNASplitRequest,
    db: Session = Depends(get_db)
):
    parent = db.query(DNARecord).filter(
        DNARecord.dna_code == payload.parent_dna
    ).first()

    if not parent:
        return {
            "message": "Parent DNA Not Found"
        }
    
    if parent.is_frozen == 1:
        return {
        "message": "DNA Is Frozen"
    }

    if payload.split_amount > parent.remaining_amount:
        return {
            "message": "Insufficient DNA Amount"
        }

    parent.child_count += 1
    parent.remaining_amount -= payload.split_amount

    child_dna = generate_child_dna(
        parent.dna_code,
        parent.child_count
    )

    child_record = DNARecord(
        dna_code=child_dna,
        parent_dna=parent.dna_code,
        amount=payload.split_amount,
        remaining_amount=payload.split_amount,
        risk_score=parent.risk_score,
        is_flagged=parent.is_flagged,
        is_frozen=parent.is_frozen
)

    db.add(child_record)
    db.commit()

    return {
        "parent_dna": parent.dna_code,
        "child_dna": child_dna,
        "parent_remaining": parent.remaining_amount
    }


@router.get("/trace-family/{dna_code}")
def trace_family(
    dna_code: str,
    db: Session = Depends(get_db)
):
    parent = db.query(DNARecord).filter(
        DNARecord.dna_code == dna_code
    ).first()

    if not parent:
        return {
            "message": "DNA Not Found"
        }

    children = db.query(DNARecord).filter(        DNARecord.parent_dna == dna_code
    ).all()

    child_list = []

    for child in children:
        child_list.append(
            {
                "dna_code": child.dna_code,
                "amount": child.amount,
                "remaining_amount": child.remaining_amount,
                "status": child.status,
                "is_flagged": child.is_flagged
            }
        )

    return {
        "parent_dna": parent.dna_code,
        "parent_amount": parent.amount,
        "parent_remaining": parent.remaining_amount,
        "status": parent.status,
        "child_count": parent.child_count,
        "is_flagged": parent.is_flagged,
        "children": child_list
    }
@router.post("/flag-dna/{dna_code}")
def flag_dna(
    dna_code: str,
    db: Session = Depends(get_db)
):
    dna_record = db.query(DNARecord).filter(
        DNARecord.dna_code == dna_code
    ).first()

    if not dna_record:
        return {    
            "message": "DNA Not Found"
        }

    dna_record.is_flagged = 1

    db.commit()

    return {
        "dna_code": dna_record.dna_code,
        "status": "Threat Assets"
    }

@router.get("/fraud-queue")
def fraud_queue(
    token: str,
    db: Session = Depends(get_db)
):
    user = validate_token(
        token,
        db
    )

    if not user:
        return {
            "message": "Invalid Token"
        }

    if user.role not in ["ADMIN", "INVESTIGATOR"]:
        return {
            "message": "Access Denied"
        }

    records = db.query(DNARecord).filter(
    DNARecord.is_flagged == 1,
    DNARecord.parent_dna.is_(None)
    ).all()

    result = []

    for record in records:
        child_count = db.query(DNARecord).filter(
        DNARecord.parent_dna == record.dna_code
        ).count()

        result.append(
        {
            "dna_code": record.dna_code,
            "amount": record.amount,
            "risk_score": record.risk_score,
            "status": record.status,
            "child_count": child_count
        }
    )
    return result

@router.get("/trace-full-family/{dna_code}")
def trace_full_family(
    dna_code: str,
    db: Session = Depends(get_db)
):
    parent = db.query(DNARecord).filter(
        DNARecord.dna_code == dna_code
    ).first()

    if not parent:
        return {
            "message": "DNA Not Found"
        }

    records = db.query(DNARecord).all()

    return {
        "root_dna": dna_code,
        "family_tree": build_tree(
            dna_code,
            records
        )
    }
@router.post("/freeze-dna/{dna_code}")
def freeze_dna(
    dna_code: str,
    token: str,
    db: Session = Depends(get_db)
):
    user = validate_token(
        token,
        db
    )

    if not user:
        return {
            "message": "User Not Found"
        }

    if user.role not in ["ADMIN", "INVESTIGATOR"]:
        return {
            "message": "Access Denied"
        }

    dna_record = db.query(DNARecord).filter(
        DNARecord.dna_code == dna_code
    ).first()

    if not dna_record:
        return {
            "message": "DNA Not Found"
        }

    dna_record.is_frozen = 1

    audit_log = AuditLog(
        action="freeze",
        dna_code=dna_record.dna_code,
        performed_by=user.email
    )

    db.add(audit_log)

    db.commit()

    return {
        "dna_code": dna_record.dna_code,
        "status": "FROZEN"
    }

@router.post("/recover-dna/{dna_code}")
def recover_dna(
    dna_code: str,
    token: str,
    db: Session = Depends(get_db)
):
    user = validate_token(
        token,
        db
    )

    if not user:
        return {
            "message": "User Not Found"
        }

    if user.role not in ["ADMIN", "INVESTIGATOR"]:
        return {
            "message": "Access Denied"
        }

    dna_record = db.query(DNARecord).filter(
        DNARecord.dna_code == dna_code
    ).first()

    if not dna_record:
        return {
            "message": "DNA Not Found"
        }

    dna_record.status = "RECOVERED"
    dna_record.is_frozen = 0
    dna_record.recovered_amount = dna_record.amount

    audit_log = AuditLog(
        action="RECOVER",
        dna_code=dna_record.dna_code,
        performed_by=user.email
    )

    db.add(audit_log)

    db.commit()

    return {
        "dna_code": dna_record.dna_code,
        "status": "RECOVERED",
        "recovered_amount": dna_record.recovered_amount
    }
@router.post("/login")
def login(
    payload: LoginRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == payload.email
    ).first()

    if not user:
        return {
            "message": "Invalid User"
        }

    token = generate_token()
    user.auth_token = token
    db.commit()
    return {
        "token": token,
        "user_id": user.id,
        "role": user.role
    }

@router.get("/users")
def get_users(
    db: Session = Depends(get_db)
):
    users = db.query(User).all()

    result = []

    for user in users:
        result.append(
            {
                "id": user.id,
                "name": user.full_name,
                "email": user.email,
                "role": user.role
            }
        )

    return result
@router.get("/dashboard")
def dashboard(
    token: str,
    db: Session = Depends(get_db)
):
    user = validate_token(
        token,
        db
    )

    if not user:
        return {
            "message": "Invalid Token"
        }

    if user.role not in ["ADMIN", "INVESTIGATOR"]:
        return {
            "message": "Access Denied"
        }

    return get_dashboard_stats(db)

@router.get("/dna-details/{dna_code}")
def dna_details(
    dna_code: str,
    token: str,
    db: Session = Depends(get_db)
):
    user = validate_token(
        token,
        db
    )

    if not user:
        return {
            "message": "Invalid Token"
        }

    dna = db.query(
        DNARecord
    ).filter(
        DNARecord.dna_code == dna_code
    ).first()

    if not dna:
        return {
            "message": "DNA Not Found"
        }

    return {
        "dna_code": dna.dna_code,
        "amount": dna.amount,
        "status": dna.status,
        "risk_score": dna.risk_score,
        "parent_dna": dna.parent_dna,
        "remaining_amount": dna.remaining_amount,
        "is_flagged": dna.is_flagged,
        "is_frozen": dna.is_frozen,
        "recovered_amount": dna.recovered_amount
    }
@router.get("/all-assets")
def all_assets(db: Session = Depends(get_db)):

    records = db.query(DNARecord).all()

    return [
        {
            "dna_code": r.dna_code,
            "parent_dna": r.parent_dna,
            "is_flagged": r.is_flagged,
            "status": r.status
        }
        for r in records
    ]