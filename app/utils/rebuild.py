
def rebuild_schemas():
    from app.domains.users.schemas import UserSchemaRel
    from app.domains.users.schemas import UserSchema
    from app.domains.storages.schemas import StorageSchemaRel, StorageSchema
    from app.domains.categories.schemas import CategorySchema
    UserSchemaRel.model_rebuild()
    StorageSchemaRel.model_rebuild()
