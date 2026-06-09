SCHEMES = [
    {
        "id": "pm-kisan",
        "name": "PM-KISAN",
        "benefit_amount": "₹6,000/year",
        "eligibility": "Small and marginal farmers with cultivable land",
        "occupations": ["farmer", "kisan"],
        "income_max": 500000,
        "states": ["all"],
        "application_link": "https://pmkisan.gov.in",
        "difficulty": 2,
        "steps": [
            "Visit nearest CSC or pmkisan.gov.in",
            "Provide Aadhaar and land records",
            "Bank account verification",
            "Receive ₹2,000 every 4 months",
        ],
        "estimated_value": 6000,
    },
    {
        "id": "pmjdy",
        "name": "PM Jan Dhan Yojana",
        "benefit_amount": "Zero-balance account + ₹2L insurance",
        "eligibility": "Any Indian citizen without bank account",
        "occupations": ["all"],
        "income_max": 99999999,
        "states": ["all"],
        "application_link": "https://pmjdy.gov.in",
        "difficulty": 1,
        "steps": [
            "Visit any bank branch with Aadhaar",
            "Fill account opening form",
            "Receive RuPay debit card",
        ],
        "estimated_value": 50000,
    },
    {
        "id": "pm-svanidhi",
        "name": "PM SVANidhi",
        "benefit_amount": "₹10,000 collateral-free loan",
        "eligibility": "Street vendors with vending certificate",
        "occupations": ["vendor", "gig worker"],
        "income_max": 300000,
        "states": ["all"],
        "application_link": "https://pmsvanidhi.mohua.gov.in",
        "difficulty": 3,
        "steps": [
            "Get vendor ID from ULB",
            "Apply via CSC or mobile app",
            "Complete digital literacy training",
            "Receive loan in 3 tranches",
        ],
        "estimated_value": 10000,
    },
    {
        "id": "atal-pension",
        "name": "Atal Pension Yojana",
        "benefit_amount": "₹1,000-5,000/month pension at 60",
        "eligibility": "Age 18-40, bank account holder",
        "occupations": ["all"],
        "income_max": 500000,
        "states": ["all"],
        "application_link": "https://npscra.nsdl.co.in",
        "difficulty": 2,
        "steps": [
            "Visit bank with Aadhaar",
            "Choose pension amount",
            "Auto-debit contribution monthly",
        ],
        "estimated_value": 36000,
    },
    {
        "id": "pmay",
        "name": "PMAY - Housing for All",
        "benefit_amount": "Up to ₹2.67 lakh subsidy",
        "eligibility": "EWS/LIG families, no pucca house",
        "occupations": ["all"],
        "income_max": 600000,
        "states": ["all"],
        "application_link": "https://pmaymis.gov.in",
        "difficulty": 4,
        "steps": [
            "Check eligibility on PMAY portal",
            "Apply through bank or CSC",
            "Submit income and property documents",
            "Receive interest subsidy on home loan",
        ],
        "estimated_value": 267000,
    },
    {
        "id": "kcc",
        "name": "Kisan Credit Card",
        "benefit_amount": "Credit up to ₹3 lakh at 4% interest",
        "eligibility": "Farmers, tenant farmers, SHG members",
        "occupations": ["farmer", "kisan"],
        "income_max": 800000,
        "states": ["all"],
        "application_link": "https://www.india.gov.in",
        "difficulty": 3,
        "steps": [
            "Visit cooperative or commercial bank",
            "Submit land records and crop details",
            "Bank assesses credit limit",
            "Use card for agricultural inputs",
        ],
        "estimated_value": 50000,
    },
    {
        "id": "nsp",
        "name": "National Scholarship Portal",
        "benefit_amount": "₹10,000-50,000/year",
        "eligibility": "Students from economically weaker sections",
        "occupations": ["teacher", "all"],
        "income_max": 800000,
        "states": ["all"],
        "application_link": "https://scholarships.gov.in",
        "difficulty": 2,
        "steps": [
            "Register on scholarships.gov.in",
            "Fill application with income certificate",
            "Upload documents",
            "Track status online",
        ],
        "estimated_value": 25000,
    },
    {
        "id": "disability-pension",
        "name": "Disability Pension (NSAP)",
        "benefit_amount": "₹500-1,000/month",
        "eligibility": "Persons with 40%+ disability, BPL",
        "occupations": ["all"],
        "income_max": 200000,
        "states": ["all"],
        "application_link": "https://nsap.nic.in",
        "difficulty": 2,
        "steps": [
            "Get disability certificate from medical board",
            "Apply at Block Development Office",
            "Submit BPL card and bank details",
        ],
        "estimated_value": 12000,
        "requires_disability": True,
    },
    {
        "id": "pmfby",
        "name": "PM Fasal Bima Yojana",
        "benefit_amount": "Crop loss compensation",
        "eligibility": "All farmers growing notified crops",
        "occupations": ["farmer", "kisan"],
        "income_max": 99999999,
        "states": ["all"],
        "application_link": "https://pmfby.gov.in",
        "difficulty": 2,
        "steps": [
            "Enroll before sowing season",
            "Pay 2% premium (Kharif) or 1.5% (Rabi)",
            "Report crop loss within 72 hours",
            "Receive claim in bank account",
        ],
        "estimated_value": 30000,
    },
    {
        "id": "mudra",
        "name": "MUDRA Loan",
        "benefit_amount": "Up to ₹10 lakh",
        "eligibility": "Micro enterprises, small business owners",
        "occupations": ["gig worker", "vendor", "all"],
        "income_max": 500000,
        "states": ["all"],
        "application_link": "https://www.mudra.org.in",
        "difficulty": 3,
        "steps": [
            "Prepare business plan",
            "Visit bank with Aadhaar and PAN",
            "Choose Shishu/Kishore/Tarun category",
            "Receive loan without collateral (up to ₹50K)",
        ],
        "estimated_value": 50000,
    },
]


def get_eligible_schemes(twin) -> list[dict]:
    results = []
    avg_income = (twin.income.range_min + twin.income.range_max) / 2
    occupation = twin.context.occupation.lower()
    has_disability = bool(twin.context.disability_flags)

    for scheme in SCHEMES:
        if scheme.get("requires_disability") and not has_disability:
            continue
        if avg_income > scheme["income_max"]:
            continue
        occ_match = (
            "all" in scheme["occupations"]
            or any(o in occupation for o in scheme["occupations"])
            or (twin.persona_id and twin.persona_id.value in scheme["occupations"])
        )
        if occ_match:
            results.append(scheme)
    return results[:8]
