import robocorp.log as logger
from RPA.Robocorp.WorkItems import WorkItems, State


class WorkItemProcessor:
    def __init__(self):
        self.library = WorkItems()

    def retrieve_work_item(self, variable: str) -> str:
        """
        Retrieve the work item from the user.

        Args:
            variable (str): Variable name to retrieve.

        Returns:
            str: Retrieved work item.

        Raises:
            KeyError: If the specified variable is not found in the work item variables.
            Exception: If any other unexpected error occurs during retrieval.
        """
        try:
            self.library = WorkItems()
            self.library.get_input_work_item()
            variables = self.library.get_work_item_variables()
            item = variables[variable]
            logger.info("Successfully retrieved work item")
            return item
        except KeyError:
            logger.exception(f"Variable '{variable}' not found in work item variables")
            raise Exception(f"Variable '{variable}' not found in work item variables")
        except Exception as e:
            logger.exception(f"Error retrieving work item: {e}")
            raise Exception(f"Error retrieving work item: {e}")

    def create_output_work_item(self, payload):
        """
        Create the output work item.

        Args:
            payload (dict): Dictionary containing the work item payload.
        """
        self.library.create_output_work_item()
        self.library.set_work_item_variables(payload)
        self.library.save_work_item()

    def release_input_work_item_as_done(self):
        """
        Release the input work item as done.
        """
        # Mark the lastly retrieved input work item as processed successfully
        self.library.release_input_work_item(State.DONE)





