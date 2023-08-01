import sys
from dependency_injector.wiring import Provide, inject

from aviva_pensions.container import Container
from aviva_pensions.services.pdf_extractor_service import PDFExtractorService
from aviva_pensions.services.report_writer import ReportWriter


@inject
def main(
    dir:str, 
    outfile:str,
    pdf_extractor: PDFExtractorService = Provide[Container.pdf_extractor_service],
    report_writer: ReportWriter = Provide[Container.report_writer]
) -> None:
    
    # read all pdfs from directory
    results = pdf_extractor.read_directory(dir)
    
    # post-process results - generate insights
    
    # filter data into format for writing the report
    
    # print out the report
    report_writer.write_data(outfile=outfile, data=results)
    
if __name__ == "__main__":
    
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])

    main(*sys.argv[1:])