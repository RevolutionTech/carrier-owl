def generate_customized_message(event, user):
    return f"Hey {user.first_name},\n\n{event.description}"
