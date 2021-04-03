
# FUTURE TODO: Reconsider how is the user agent string actually generated - what if we want
# to limit the number of user agents in the file that gets generated?
# What if we want to include only user agents that satisfy specific conditions?
# -> Good points to reiterate on before pushing out the final version.
class Python():
    def __init__(self):
        print("Init from Python generator.")
        self.user_agents = []
        self.file_extension = "py"

    def set_user_agents(self, user_agents):
        self.user_agents = user_agents

    def get_extension(self):
        return self.file_extension

    def generate_user_agent_list_string(self):
        """
        Returns single line - a variable `user_agent_list` with all the user
        agents enumerated right after.
        """
        output_string = "user_agent_list = [\""
        output_string += "\", \"".join(self.user_agents)
        output_string += "\"]"

        return output_string

    def generate_user_agent_list_string_pretty(self):
        # user_agents_list_pretty (list with new-lined (if allowed) user-agents list)
        """
        Returns multiple lines with somewhat prettified user agent list inside 
        one variable - `user_agent_list_pretty`
        """ 
        output_string = "user_agent_list_pretty = ["
        i = 0
        for ua in self.user_agents:
            output_string += f"\t\"{ua}\""
            if (i != len(self.user_agents) - 1):
                output_string += ",\n"
            i += 1
        
        output_string += "]"
        return output_string

