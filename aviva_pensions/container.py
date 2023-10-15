from dependency_injector import containers, providers


from aviva_pensions.services.pdf_extractor_service import PDFExtractorService
from aviva_pensions.services.plumber import Plumber
from aviva_pensions.services.report_writer import ReportWriter
from aviva_pensions.services.post_processor_service import PostProcessorService

from aviva_pensions.parsers.risk_parser import RiskParser
from aviva_pensions.parsers.risks_parser import RisksParser
from aviva_pensions.parsers.basic_table_parser import BasicTableParser
from aviva_pensions.parsers.name_parser import NameParser
from aviva_pensions.parsers.performance_table_parser import PerformanceTableParser
from aviva_pensions.parsers.performance_matrix import PerformanceMatrix
from aviva_pensions.parsers.performance_matrix_row import PerformanceMatrixRow
from aviva_pensions.parsers.report_date_parser import ReportDateParser

from aviva_pensions.processors.performance_post_processor import PerformancePostProcessor
from aviva_pensions.processors.add_columns_post_processor import AddColumnsPostProcessor
from aviva_pensions.processors.add_prices_charges_post_processor import AddPricesChargesPostProcessor

from aviva_pensions.readers.csv_dict_reader import CSVDictReader
from aviva_pensions.readers.list_to_dict_data_provider import ListToDictDataProvider
from aviva_pensions.readers.extract_prices_charges_data_provider import ExtractPricesChargesDataProvider

class Container(containers.DeclarativeContainer):

    config = providers.Configuration(yaml_files=["./config.yml"])

    name_parser = providers.Factory(
        NameParser
    )

    # define the plugins so that each plumber instance gets new plugin instances
    risk_parser = providers.Factory(
        RiskParser
    )

    risks_parser = providers.Factory(
        RisksParser,
        names=config.risks.names
    )

    basic_table_parser = providers.Factory(
        BasicTableParser,
        name_parser=name_parser
    )

    report_date_parser = providers.Factory(
        ReportDateParser
    )

    perf_matrix_row_factory = providers.Factory(
        PerformanceMatrixRow,
        year_cols=config.post_processor.performance.columns
    )

    perf_matrix_factory = providers.Factory(
        PerformanceMatrix
    )

    perf_table_parser = providers.Factory(
        PerformanceTableParser,
        name_parser=name_parser,
        perf_matrix_factory=perf_matrix_factory.provider,
        perf_matrix_row_factory=perf_matrix_row_factory.provider
    )

    perf_post_processor = providers.Factory(
        PerformancePostProcessor,
        columns=config.post_processor.performance.columns
    )

    add_columns_reader = providers.Factory(
        CSVDictReader,
        config.post_processor.add_columns.file,
        config.post_processor.add_columns.delim,
        config.post_processor.add_columns.encoding
    )

    add_columns_data_provider = providers.Factory(
        ListToDictDataProvider,
        key=config.post_processor.add_columns.key,
        reader=add_columns_reader
    )

    add_prices_reader = providers.Factory(
        CSVDictReader,
        config.post_processor.add_prices.file,
        config.post_processor.add_prices.delim,
        config.post_processor.add_prices.encoding
    )

    add_prices_data_provider = providers.Factory(
        ExtractPricesChargesDataProvider,
        reader=add_prices_reader,
        name_parser=name_parser
    )

    add_cols_post_processor = providers.Factory(
        AddColumnsPostProcessor,
        key=config.post_processor.add_columns.key,
        columns=config.post_processor.add_columns.columns,
        data_provider=add_columns_data_provider
    )

    add_prices_post_processor = providers.Factory(
        AddPricesChargesPostProcessor,
        key=config.post_processor.add_prices.key,
        columns=config.post_processor.add_prices.columns,
        data_provider=add_prices_data_provider
    )

    char_stream_parsers=providers.List(
        risk_parser
    )

    text_parsers = providers.List(
        risks_parser,
        report_date_parser
    )

    table_parsers = providers.List(
        basic_table_parser,
        perf_table_parser
    )

    post_processors = providers.List(
        perf_post_processor,
        add_cols_post_processor,
        add_prices_post_processor
    )

    plumber = providers.Factory(
        Plumber,
        char_stream_parsers = char_stream_parsers,
        text_parsers = text_parsers,
        table_parsers = table_parsers,
        file_name_parser = name_parser
    )

    report_writer = providers.Singleton(
        ReportWriter,
        columns=config.report.columns,
        outfile=config.report.outfile
    )

    pdf_extractor_service = providers.Singleton(
        PDFExtractorService,
        plumber.provider
    )

    post_processor_service = providers.Singleton(
        PostProcessorService,
        post_processors = post_processors
    )
