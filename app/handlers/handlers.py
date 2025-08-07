import logging
from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException, NotFound, InternalServerError
from ..exceptions.base import BaseAppException
from ..constans import get_error_message

def setup_error_handlers(app: Flask):
    """Configura todos los manejadores de errores para la aplicación"""
    error_logger = logging.getLogger('app.errors')
    
    @app.errorhandler(BaseAppException)
    def handle_app_exception(error: BaseAppException):
        """Maneja todas las excepciones personalizadas de la aplicación"""
        context = {
            "request_endpoint": request.endpoint,
            "request_method": request.method,
            "request_url": request.url,
            "client_ip": request.remote_addr,
            "user_agent_header": request.headers.get('User-Agent')
        }
        
        error.log_error(error_logger, context)
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response
    
    @app.errorhandler(404)
    def handle_not_found(error):
        """Maneja errores 404 personalizados"""
        error_logger.warning(f"404 Not Found: {request.url}", extra={
            "endpoint": request.endpoint,
            "method": request.method,
            "url": request.url,
            "remote_addr": request.remote_addr
        })
        
        return jsonify({
            "error": get_error_message('NOT_FOUND'),
            "message": get_error_message('NOT_FOUND_ENDPOINT', method=request.method, path=request.path),
            "status_code": 404
        }), 404
    
    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        """Maneja errores 405 (método no permitido)"""
        error_logger.warning(f"405 Method Not Allowed: {request.method} {request.url}")
        
        return jsonify({
            "error": get_error_message('METHOD_NOT_ALLOWED', method=request.method),
            "message": get_error_message('METHOD_NOT_ALLOWED', method=request.method),
            "status_code": 405
        }), 405
    
    @app.errorhandler(500)
    def handle_internal_error(error):
        """Maneja errores internos del servidor"""
        error_logger.error(f"500 Internal Server Error: {str(error)}", extra={
            "endpoint": request.endpoint,
            "method": request.method,
            "url": request.url,
            "remote_addr": request.remote_addr,
            "error_details": str(error)
        })
        
        return jsonify({
            "error": get_error_message('INTERNAL_SERVER_ERROR'),
            "message": get_error_message('INTERNAL_SERVER_ERROR'),
            "status_code": 500
        }), 500
    
    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        """Maneja cualquier excepción no capturada"""
        error_logger.critical(f"Unexpected error: {str(error)}", extra={
            "endpoint": request.endpoint,
            "method": request.method,
            "url": request.url,
            "remote_addr": request.remote_addr,
            "error_type": type(error).__name__,
            "error_details": str(error)
        }, exc_info=True)
        
        return jsonify({
            "error": get_error_message('UNEXPECTED_ERROR'),
            "message": get_error_message('UNEXPECTED_ERROR'),
            "status_code": 500
        }), 500