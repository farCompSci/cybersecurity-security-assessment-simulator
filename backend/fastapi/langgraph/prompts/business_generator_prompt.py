business_generation_prompt_message = """
        You are an expert at coming up with new business ideas. 
        Your task is to generate a fictitious small business (5–15 employees) in a relatable industry. 

        Use this example as a guide to generate a new business:
        {example}

        Follow this structure exactly when generating your business. Do not include any additional sections:
        
        - Business Name
        - Business Description: 
            * Contact Info (make up an email address and phone number)
            * Location (keep it to cities within the United States)
            * Products or Services Offered 
            * Digital Footprint (e.g. basic website, email communication, customer database, crm)

        Pause to reason through the prompt step-by-step until the requirements are clear. Only after this step, generate the business:

        Generated Business:
        """
