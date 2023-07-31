from dependency_injector import containers, providers


from aviva_pensions.services.pdf_reporter import PDFReporter
from aviva_pensions.services.plumber import Plumber

from aviva_pensions.parsers.risk_parser import RiskParser
from aviva_pensions.parsers.risks_parser import RisksParser
from aviva_pensions.parsers.basic_table_parser import BasicTableParser

class Container(containers.DeclarativeContainer):
    
    config = providers.Configuration()
    
    # define the plugins so that each plumber instance gets new plugin instances
    risk_parser = providers.Factory(
        RiskParser
    )

    risks_parser = providers.Factory(
        RisksParser
    )
    
    basic_table_parser = providers.Factory(
        BasicTableParser
    )
    
    char_stream_parsers=providers.List(
        risk_parser
    )
    
    text_parsers = providers.List(
        risks_parser
    )
    
    table_parsers = providers.List(
        basic_table_parser
    )
    
    plumber = providers.Factory(
        Plumber,
        char_stream_parsers = char_stream_parsers,
        text_parsers = text_parsers,
        table_parsers = table_parsers
    )
    
    pdf_reporter = providers.Singleton(
        PDFReporter,
        plumber.provider
    )
    