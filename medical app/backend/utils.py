import logging

# Utility function for logging errors
def log_error(message):
    logging.error(message)

# Utility function for handling errors
def handle_error(error_message):
    log_error(error_message)
    return jsonify({"error": error_message}), 500
