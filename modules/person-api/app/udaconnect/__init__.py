def register_routes(api, app, root="api"):
    from app.udaconnect.controllers import api as udaconnect_person_api

    api.add_namespace(udaconnect_person_api, path=f"/{root}")
