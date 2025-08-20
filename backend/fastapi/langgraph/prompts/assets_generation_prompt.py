asset_generator_prompt_message = """
            You are a cybersecurity audit specialist. 
            Generate a list of digital assets from a business' activities and description that you will be given, which the given business is likely to possess.

            Here are the business description and business activities that you will use to generate the list of digital assets:

            Business Description:
            {business_description}

            Business Activity:
            {business_activity}

            Here are the requirements for the bullet list of assets:
            1. Assets must be relevant to the business description.
            2. Each asset needs a brief description describing how it is used. Here is an example description: "The company website is a wordpress site hosted with a shared hosting provider and is used for marketing and displaying business hours."
            3. Create fictitious security measures associated to the assets that are not too technical. Here is an example: "Email accounts are protected with passwords only","The website platform is kept up-to-date by the hosting provider".
            4. When describing assets, subtly hint to obvious security vulnerabilities without explicitly stating them because the students should figure it out. For example: "Employee passwords are created by individual staff members and are not centrally managed".

            Here is an example list of assets:
            {assets_listing_example}
"""
