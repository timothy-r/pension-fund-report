import sys
from dependency_injector.wiring import Provide, inject

from aviva_pensions.container import Container
from aviva_pensions.services.pdf_extractor_service import PDFExtractorService
from aviva_pensions.services.report_writer import ReportWriter
from aviva_pensions.services.post_processor_service import PostProcessorService

@inject
def main(
    dir:str, 
    pdf_extractor: PDFExtractorService = Provide[Container.pdf_extractor_service],
    post_processor: PostProcessorService = Provide[Container.post_processor_service],
    report_writer: ReportWriter = Provide[Container.report_writer]
) -> None:
    
    # read all pdfs from directory
    for result in pdf_extractor.read_directory(dir):
    
        # post-process results - generate insights
        result = post_processor.process(data=result)
        
        # print out the report
        report_writer.write_data(data=result)


if __name__ == "__main__":
    
    container = Container()
    # override config.report.outfile with argv[2] if set
    
    if len(sys.argv) > 2:
        outfile = sys.argv[2]
        
        container.config.report.outfile.from_value(outfile)
        
    container.init_resources()
    container.wire(modules=[__name__])

    main(sys.argv[1])