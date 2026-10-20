"""Role 3: select the smallest maintainable integration design."""
def choose_integration(*, has_supported_api: bool, has_hermes_adapter: bool,
                       has_stable_cli: bool, source_change_necessary: bool = False) -> str:
    if has_supported_api:
        return "api_adapter"
    if has_hermes_adapter:
        return "existing_hermes_adapter"
    if has_stable_cli:
        return "cli_adapter"
    if source_change_necessary:
        return "targeted_source_integration"
    return "blocked_no_supported_interface"
