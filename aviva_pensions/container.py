from dependency_injector import containers, providers


from aviva_pensions.services.pdf_extractor_service import PDFExtractorService
from aviva_pensions.services.plumber import Plumber

from aviva_pensions.parsers.risk_parser import RiskParser
from aviva_pensions.parsers.risks_parser import RisksParser
from aviva_pensions.parsers.basic_table_parser import BasicTableParser
from aviva_pensions.parsers.file_name_parser import FileNameParser
from aviva_pensions.parsers.performance_table_parser import PerformanceTableParser
from aviva_pensions.parsers.table_cell_label_parser import TableCellLabelParser

class Container(containers.DeclarativeContainer):
    
    config = providers.Configuration()
    
    table_cell_label_parser = providers.Factory(
        TableCellLabelParser
    )
        
    # define the plugins so that each plumber instance gets new plugin instances
    risk_parser = providers.Factory(
        RiskParser
    )

    risks_parser = providers.Factory(
        RisksParser
    )
    
    basic_table_parser = providers.Factory(
        BasicTableParser,
        table_cell_label_parser
    )
    
    file_name_parser = providers.Factory(
        FileNameParser
    )
    
    perf_table_parser = providers.Factory(
        PerformanceTableParser,
        table_cell_label_parser
    )
    

    
    char_stream_parsers=providers.List(
        risk_parser
    )
    
    text_parsers = providers.List(
        risks_parser
    )
    
    table_parsers = providers.List(
        basic_table_parser,
        perf_table_parser
    )
    
    plumber = providers.Factory(
        Plumber,
        char_stream_parsers = char_stream_parsers,
        text_parsers = text_parsers,
        table_parsers = table_parsers,
        file_name_parser = file_name_parser
    )
    
    pdf_extractor_service = providers.Singleton(
        PDFExtractorService,
        plumber.provider
    )
    