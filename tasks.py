from robocorp.tasks import task
from script.browser import GothamistAction
from script.utils import export_data_to_excel
from script.workitem import WorkItemProcessor
from RPA.Browser.Selenium import Selenium


@task
def robot_spare_bin_python():
    selenium = Selenium()
    gotham = GothamistAction(selenium=selenium)
    item =  WorkItemProcessor().retrieve_work_item('news')
    data = gotham.main(item)
    export_data_to_excel(item , data)



