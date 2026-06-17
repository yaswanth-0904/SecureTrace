from app.services.family_tree_service import build_tree

sample = []

print(
    build_tree(
        "DNA-000001",
        sample
    )
)