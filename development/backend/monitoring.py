import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from prometheus_flask_exporter import PrometheusMetrics
import flask_monitoringdashboard as dashboard
import psutil
import logging
from datetime import datetime
import os

class Monitoring:
    def __init__(self, app):
        self.app = app
        self.setup_sentry()
        self.setup_prometheus()
        self.setup_dashboard()
        self.setup_custom_logging()
        self.setup_system_monitoring()

    def setup_sentry(self):
        """Setup Sentry for error tracking"""
        sentry_sdk.init(
            dsn=os.getenv('SENTRY_DSN'),
            integrations=[FlaskIntegration()],
            traces_sample_rate=1.0,
            environment=os.getenv('FLASK_ENV', 'production')
        )

    def setup_prometheus(self):
        """Setup Prometheus metrics"""
        metrics = PrometheusMetrics(self.app)
        
        # Custom metrics
        metrics.info('app_info', 'Application info', version='1.0.0')
        metrics.register_default(
            metrics.counter(
                'by_path_counter', 'Request count by request paths',
                labels={'path': lambda: request.path}
            )
        )

    def setup_dashboard(self):
        """Setup Flask Monitoring Dashboard"""
        dashboard.config.init_from(file='dashboard.config')
        dashboard.bind(self.app)

    def setup_custom_logging(self):
        """Setup custom logging for form submissions and errors"""
        logging.basicConfig(
            filename=f'logs/app_{datetime.now().strftime("%Y%m%d")}.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

        # Email submission logging
        self.email_logger = logging.getLogger('email_submissions')
        email_handler = logging.FileHandler('logs/email_submissions.log')
        email_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - From: %(email)s - Status: %(status)s'
        ))
        self.email_logger.addHandler(email_handler)

    def setup_system_monitoring(self):
        """Setup system resource monitoring"""
        @self.app.before_request
        def log_system_stats():
            stats = {
                'cpu_percent': psutil.cpu_percent(),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_usage': psutil.disk_usage('/').percent
            }
            if stats['cpu_percent'] > 80 or stats['memory_percent'] > 80:
                logging.warning(f'High resource usage detected: {stats}')

    def log_email_submission(self, email, status):
        """Log email submission details"""
        self.email_logger.info('Email submission', extra={
            'email': email,
            'status': status
        })

    def get_system_health(self):
        """Get system health metrics"""
        return {
            'cpu_usage': psutil.cpu_percent(),
            'memory_usage': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent,
            'network_connections': len(psutil.net_connections()),
            'timestamp': datetime.now().isoformat()
        } 