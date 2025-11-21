from sqlalchemy.orm import Session

from app.models.calculation import Calculation, CalculationType as ModelCalcType
from app.schemas.calculation import CalculationCreate, CalculationType
from app.services.calculation_factory import CalculationFactory


def create_calculation(db: Session, calc_in: CalculationCreate, user_id: int | None = None) -> Calculation:
    """
    Create a Calculation row in the database.

    user_id is kept in the signature for future use, but the current model
    does not have a user_id column, so it is ignored here.
    """
    # Use factory to compute result
    strategy = CalculationFactory.get_strategy(calc_in.type)
    result = strategy.calculate(calc_in.a, calc_in.b)

    # Convert schema enum to model enum for the DB column
    calc_type_model = ModelCalcType(calc_in.type.value)

    db_obj = Calculation(
        a=calc_in.a,
        b=calc_in.b,
        type=calc_type_model,
        result=result,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
