import sys
from dependency_injector.wiring import Provide, inject

from content_download.container import Container

@inject
def main(source:str, target:str) -> None:
    
    print("Extract urls from {} download to {}".format(source, target))
    
    # open the source file & read the contents
    pass

if __name__ == "__main__":
    
    container = Container()
    
    container.init_resources()
    container.wire(modules=[__name__])

    main(sys.argv[1], sys.argv[2])
    