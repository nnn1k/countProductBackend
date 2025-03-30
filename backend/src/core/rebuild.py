def rebuild_schemas():
    from backend.src.core.users.schemas import UserSchemaRel, UserSchema
    from backend.src.core.storages.schemas import StorageSchemaRel, StorageSchema
    UserSchemaRel.model_rebuild()
    StorageSchemaRel.model_rebuild()
