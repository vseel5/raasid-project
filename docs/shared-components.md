# Shared Components Documentation

## Version Information
- **Document Version**: 1.0.0
- **Last Updated**: April 17, 2024
- **Compatible System Version**: 1.0.0

## Related Documentation
- [Security Documentation](security-documentation.md) - For security-related utilities
- [Admin Dashboard](admin-dashboard.md) - For admin interface components
- [Data Strategy](data-strategy.md) - For data handling utilities

## Table of Contents
1. [Common Utilities](#common-utilities)
2. [Security Components](#security-components)
3. [Data Components](#data-components)
4. [Monitoring Components](#monitoring-components)
5. [API Components](#api-components)

## Common Utilities

### Logger
```python
# Common logging utility
class Logger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.setup_logger()

    def setup_logger(self) -> None:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log(self, level: str, message: str, **kwargs) -> None:
        getattr(self.logger, level.lower())(message, **kwargs)
```

### Configuration Manager
```python
# Configuration management
class ConfigManager:
    def __init__(self):
        self.config = self.load_config()

    def load_config(self) -> Dict:
        with open('config.yaml', 'r') as f:
            return yaml.safe_load(f)

    def get(self, key: str, default: Any = None) -> Any:
        return self.config.get(key, default)

    def update(self, key: str, value: Any) -> None:
        self.config[key] = value
        self.save_config()
```

## Security Components

### Token Manager
```python
# JWT token management
class TokenManager:
    def generate_token(self, payload: Dict) -> str:
        return jwt.encode(
            {**payload, 'exp': datetime.now() + timedelta(hours=1)},
            SECRET_KEY,
            algorithm='HS256'
        )

    def validate_token(self, token: str) -> Dict:
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except jwt.InvalidTokenError:
            raise SecurityError("Invalid token")
```

### Access Control
```python
# Common access control
class AccessControl:
    def check_access(self, user: User, resource: str, action: str) -> bool:
        return (
            self.check_permission(user.role, resource, action) and
            self.validate_session(user.session) and
            self.check_ip_restrictions(user.ip)
        )

    def check_permission(self, role: str, resource: str, action: str) -> bool:
        return self.permission_matrix[role][resource].get(action, False)
```

## Data Components

### Data Validator
```python
# Common data validation
class DataValidator:
    def validate_schema(self, data: Dict, schema: Dict) -> bool:
        try:
            jsonschema.validate(data, schema)
            return True
        except jsonschema.exceptions.ValidationError:
            return False

    def sanitize_input(self, data: Dict) -> Dict:
        return {
            k: self.sanitize_value(v)
            for k, v in data.items()
        }
```

### Cache Manager
```python
# Common caching utility
class CacheManager:
    def __init__(self):
        self.cache = {}

    def get(self, key: str) -> Any:
        return self.cache.get(key)

    def set(self, key: str, value: Any, ttl: int = 3600) -> None:
        self.cache[key] = {
            'value': value,
            'expires': time.time() + ttl
        }

    def delete(self, key: str) -> None:
        self.cache.pop(key, None)
```

## Monitoring Components

### Metrics Collector
```python
# Common metrics collection
class MetricsCollector:
    def __init__(self):
        self.metrics = defaultdict(list)

    def record_metric(self, name: str, value: float) -> None:
        self.metrics[name].append({
            'value': value,
            'timestamp': time.time()
        })

    def get_metrics(self, name: str) -> List[Dict]:
        return self.metrics.get(name, [])
```

### Alert Manager
```python
# Common alert management
class AlertManager:
    def check_alerts(self) -> List[Dict]:
        alerts = []
        for metric, threshold in self.thresholds.items():
            if self.metrics_collector.get_latest(metric) > threshold:
                alerts.append({
                    'metric': metric,
                    'value': self.metrics_collector.get_latest(metric),
                    'threshold': threshold
                })
        return alerts
```

## API Components

### Request Handler
```python
# Common API request handling
class RequestHandler:
    def handle_request(self, request: Request) -> Response:
        try:
            self.validate_request(request)
            data = self.process_request(request)
            return self.create_response(data)
        except Exception as e:
            return self.handle_error(e)

    def validate_request(self, request: Request) -> None:
        if not self.validator.validate_schema(request.data, self.schema):
            raise ValidationError("Invalid request data")
```

### Response Formatter
```python
# Common response formatting
class ResponseFormatter:
    def format_response(self, data: Any, status: int = 200) -> Response:
        return {
            'status': status,
            'data': data,
            'timestamp': datetime.now().isoformat()
        }

    def format_error(self, error: Exception) -> Response:
        return {
            'status': getattr(error, 'status_code', 500),
            'error': str(error),
            'timestamp': datetime.now().isoformat()
        }
```

## Best Practices

### Development
1. Use shared components for common functionality
2. Follow consistent naming conventions
3. Document all shared components
4. Maintain backward compatibility
5. Test thoroughly

### Deployment
1. Version shared components
2. Monitor component usage
3. Update documentation
4. Handle deprecation
5. Maintain compatibility

### Maintenance
1. Regular updates
2. Performance monitoring
3. Usage tracking
4. Documentation updates
5. Security patches

## Support
For shared components-related issues:
- Email: components@raasid.com
- Documentation: https://raasid.com/docs/components
- GitHub Issues: https://github.com/vseel5/raasid-project/issues

---

*Last updated: April 17, 2024* 