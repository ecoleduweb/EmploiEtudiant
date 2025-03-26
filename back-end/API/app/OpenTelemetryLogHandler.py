from opentelemetry.sdk._logs.export import ConsoleLogExporter, OTLPLogExporter
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.semconv.resource import ResourceAttributes
import logging

# Create a custom logging handler that uses OpenTelemetry
class OpenTelemetryLogHandler(logging.Handler):
    def __init__(self, endpoint="http://143.110.223.189:4318/v1/logs"):
        super().__init__()
        resource = Resource(attributes={    
            ResourceAttributes.SERVICE_NAME: "EMPLOI_ETUDIANT_DEV",
            ResourceAttributes.SERVICE_VERSION: "1.0.0",
            ResourceAttributes.DEPLOYMENT_ENVIRONMENT: "development"
        })
        self.logger_provider = LoggerProvider(resource=resource)
        exporter = OTLPLogExporter(endpoint=endpoint, timeout=5)
        self.processor = BatchLogRecordProcessor(exporter)
        self.logger_provider.add_log_record_processor(self.processor)
        set_logger_provider(self.logger_provider)
        
    def emit(self, record):
        self.logger_provider.get_logger(record.name).emit(record)
        
    def flush(self):
        self.processor.force_flush()