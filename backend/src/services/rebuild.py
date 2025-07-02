
def rebuild_schemas():
    from backend.src.services.users.schemas import UserSchemaRel
    from backend.src.services.users.schemas import UserSchema
    from backend.src.services.storages.schemas import StorageSchemaRel, StorageSchema
    from backend.src.services.categories.schemas import CategorySchema
    UserSchemaRel.model_rebuild()
    StorageSchemaRel.model_rebuild()
