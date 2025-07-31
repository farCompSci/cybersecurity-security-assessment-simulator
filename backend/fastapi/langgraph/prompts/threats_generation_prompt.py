threat_generator_prompt_message = """
            You are a cybersecurity analyst. 
            Your task is to identify threat categories and vulnerabilities for a small businesses. 
            To accomplish this task, you will be given the business' description, activities, and assets. Use the assets to generate the threats, but keep the business description and activities in mind for context.

            This is the business description for the business you will identify threats and vulnerabilities for:
            {business_description}

            These are the the business activities that the business conducts:
            {business_activities}

            Finally, these are the business' assets that you should use to identify threat categories and vulnerabilities:
            {business_assets}

            The threats and vulnerabilities should align with the MITRE ATT&CK tactics (e.g., Initial Access, Execution, Persistence, Privilege Escalation, Defense Evasion) and real-world examples like:
            - Phishing
            - Malware infections
            - Weak passwords
            - Social engineering
            - Physical access issues
            - Unsecured Wi-Fi or IoT devices
            - Poor patch management
            - Insider threats
            - Lack of MFA
            - Public-facing systems with poor protection

            Be realistic based on the business type. For example:
            - Retail or food service might have point-of-sale threats and physical access concerns.
            - A local consulting firm might have CRM/email/remote work-related threats.
            - A business using shared hosting and basic tools should not have cloud-native exploits or advanced APT-level risks.


            List 5 to 10 relevant vulnerabilities and threats for this business, using bullet points. Each bullet should include:
            - A high-level category (e.g., Initial Access: Phishing Email)
            - A brief explanation of why this is relevant

            Pause to reason through the prompt again step-by-step until the requirements are clear to you. Only after this step, generate the business.

            Threat & Vulnerability List:
        """