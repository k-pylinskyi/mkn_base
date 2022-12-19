from RunReport.runner import Runner
from Services.UpdateRate.UpdateRate import rate_update_manager
from Services.PriceListInvent.PriceInventV2 import vyManager
from RunReport.FTPChecker import parse_ftp

if __name__ == '__main__':
    # Runner.run()
    rate_update_manager()
    # vyManager()
